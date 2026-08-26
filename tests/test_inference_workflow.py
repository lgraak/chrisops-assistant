from __future__ import annotations

import copy
import json
from dataclasses import replace

import pytest

from chrisops_state.inference import InferenceResult, InstrumentedA60Client
from chrisops_state.inference_persistence import (
    DuplicateInferenceRunError,
    InferencePersistenceError,
)

from lib.assistant_adapter import (
    AssistantAdapter,
    AssistantInferenceError,
    TelemetryPersistenceError,
)
from lib.model_provider import ProviderInvocation
from lib.providers.openvino import OpenVINOProvider, SYSTEM_PROMPT


RESPONSE = {
    "classification": "observation-overdue",
    "summary": "Observation data delayed.",
    "explanation": "The collector did not provide fresh evidence.",
    "confidence": "bounded",
}


def _run(provider="a60_local", *, status="success", retries=0):
    return {
        "provider": {"name": provider},
        "outcome": {
            "status": status,
            "error_category": None if status == "success" else "provider_unavailable",
            "retries": retries,
        },
        "content_stored": False,
    }


class FakeProvider:
    def __init__(self, invocation):
        self.invocation = invocation
        self.calls = 0

    def invoke(self, context):
        self.calls += 1
        return self.invocation


class RecordingStore:
    def __init__(self, result=True, failure=None):
        self.result = result
        self.failure = failure
        self.runs = []

    def write_run(self, run):
        self.runs.append(copy.deepcopy(run))
        if self.failure is not None:
            raise self.failure
        return self.result


class FakeClient:
    def __init__(self, result):
        self.result = result
        self.requests = []

    def stream(self, request):
        self.requests.append(request)
        return self.result


def _invocation(provider="a60_local", *, status="success", retries=0):
    result = InferenceResult(
        content=json.dumps(RESPONSE),
        run=_run(provider, status=status, retries=retries),
    )
    return ProviderInvocation(
        response=RESPONSE if status == "success" else None,
        telemetry_result=result,
        error_category=None if status == "success" else "provider_unavailable",
    )


def test_successful_assistant_inference_writes_once_and_returns_compatible_response():
    provider = FakeProvider(_invocation())
    store = RecordingStore()

    response = AssistantAdapter(
        provider, persistence_enabled=True, store=store
    ).generate({"bounded": "context"})

    assert response == RESPONSE
    assert provider.calls == 1
    assert len(store.runs) == 1


def test_failed_terminal_inference_writes_once_and_preserves_provider_failure():
    provider = FakeProvider(_invocation(status="failed"))
    store = RecordingStore()

    with pytest.raises(AssistantInferenceError) as captured:
        AssistantAdapter(
            provider, persistence_enabled=True, store=store
        ).generate({"bounded": "context"})

    assert captured.value.category == "provider_unavailable"
    assert captured.value.persistence_status == "persisted"
    assert provider.calls == 1
    assert len(store.runs) == 1


def test_successful_inference_persistence_failure_is_bounded_and_does_not_retry():
    provider = FakeProvider(_invocation())
    store = RecordingStore(failure=InferencePersistenceError("raw path detail"))

    with pytest.raises(TelemetryPersistenceError) as captured:
        AssistantAdapter(
            provider, persistence_enabled=True, store=store
        ).generate({"bounded": "context"})

    assert captured.value.response == RESPONSE
    assert str(captured.value) == (
        "assistant inference succeeded but telemetry persistence failed"
    )
    assert "raw path detail" not in str(captured.value)
    assert provider.calls == 1
    assert len(store.runs) == 1


def test_provider_failure_remains_primary_when_persistence_also_fails():
    provider = FakeProvider(_invocation(status="failed"))
    store = RecordingStore(failure=InferencePersistenceError("raw path detail"))

    with pytest.raises(AssistantInferenceError) as captured:
        AssistantAdapter(
            provider, persistence_enabled=True, store=store
        ).generate({"bounded": "context"})

    assert captured.value.category == "provider_unavailable"
    assert captured.value.persistence_status == "failed"
    assert provider.calls == 1
    assert len(store.runs) == 1


def test_persistence_disabled_keeps_inference_usable_without_a_store():
    provider = FakeProvider(_invocation())

    assert AssistantAdapter(provider).generate({}) == RESPONSE
    assert provider.calls == 1


def test_provider_internal_retry_still_has_one_outer_write():
    provider = FakeProvider(_invocation(retries=2))
    store = RecordingStore()

    AssistantAdapter(provider, persistence_enabled=True, store=store).generate({})

    assert provider.calls == 1
    assert store.runs[0]["outcome"]["retries"] == 2
    assert len(store.runs) == 1


def test_exact_replay_is_accepted_and_conflicting_duplicate_is_deterministic():
    replay_provider = FakeProvider(_invocation())
    replay_store = RecordingStore(result=False)
    assert AssistantAdapter(
        replay_provider, persistence_enabled=True, store=replay_store
    ).generate({}) == RESPONSE

    conflict_provider = FakeProvider(_invocation())
    conflict_store = RecordingStore(
        failure=DuplicateInferenceRunError(
            "run_id already identifies a different finalized inference run"
        )
    )
    with pytest.raises(DuplicateInferenceRunError, match="different finalized"):
        AssistantAdapter(
            conflict_provider, persistence_enabled=True, store=conflict_store
        ).generate({})


@pytest.mark.parametrize("provider_name", ["a60_local", "runpod", "openai"])
def test_persistence_coordinator_is_provider_neutral(provider_name):
    provider = FakeProvider(_invocation(provider_name))
    store = RecordingStore()

    AssistantAdapter(provider, persistence_enabled=True, store=store).generate({})

    assert store.runs[0]["provider"]["name"] == provider_name


def test_openvino_provider_uses_accepted_a60_client_and_preserves_prompt_contract():
    result = InferenceResult(content=json.dumps(RESPONSE), run=_run())
    client = FakeClient(result)
    provider = OpenVINOProvider(
        client=client,
        endpoint="https://a60.example.invalid/v1/chat/completions",
        endpoint_alias="a60-private",
        model="qwen3-8b-openvino-gpu",
        workload_id="chrisops-assistant",
        hardware_alias="intel-arc-pro-a60",
        serving_engine="openvino",
        serving_version="2026.08",
    )

    invocation = provider.invoke({"private": "assistant context"})

    assert invocation.response == RESPONSE
    assert invocation.telemetry_result is result
    assert len(client.requests) == 1
    request = client.requests[0]
    assert request.provider == "a60_local"
    assert request.endpoint_alias == "a60-private"
    assert request.hardware_alias == "intel-arc-pro-a60"
    assert request.serving_engine == "openvino"
    assert request.caller == "chrisops_assistant"
    assert request.boundary_workload == "agent"
    assert len(request.correlation_run_id) == 36
    assert request.chat_messages[0] == {
        "role": "system",
        "content": SYSTEM_PROMPT,
    }
    assert json.loads(request.chat_messages[1]["content"]) == {
        "private": "assistant context"
    }
    assert request.generation_options == {
        "max_tokens": 256,
        "temperature": 0.2,
        "enable_thinking": False,
    }
    encoded_run = json.dumps(result.run)
    assert "assistant context" not in encoded_run
    assert "a60.example.invalid" not in encoded_run


def test_openvino_boundary_ownership_prevents_assistant_duplicate_write():
    result = InferenceResult(content=json.dumps(RESPONSE), run=_run())
    provider = OpenVINOProvider(
        client=FakeClient(result),
        endpoint="https://a60.example.invalid/v1/chat/completions",
        endpoint_alias="a60-private",
        model="qwen3-8b-openvino-gpu",
        workload_id="chrisops-assistant",
        hardware_alias="intel-arc-pro-a60",
        serving_engine="openvino",
    )
    store = RecordingStore()

    response = AssistantAdapter(
        provider, persistence_enabled=True, store=store
    ).generate({"bounded": "context"})

    assert response == RESPONSE
    assert store.runs == []


def test_openvino_provider_returns_safe_failed_terminal_invocation():
    result = InferenceResult(
        content="", run=_run(status="failed")
    )
    provider = OpenVINOProvider(
        client=FakeClient(result),
        endpoint="https://a60.example.invalid/v1/chat/completions",
        endpoint_alias="a60-private",
        model="qwen3-8b-openvino-gpu",
        workload_id="chrisops-assistant",
        hardware_alias="intel-arc-pro-a60",
        serving_engine="openvino",
    )

    invocation = provider.invoke({})

    assert invocation.response is None
    assert invocation.telemetry_result is result
    assert invocation.error_category == "provider_unavailable"


def test_openvino_provider_factory_type_is_the_accepted_product_client():
    schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object"}
    from lib.provider_factory import get_provider

    provider = get_provider(
        {
            "type": "openvino",
            "endpoint": "https://a60.example.invalid/v1/chat/completions",
            "endpoint_alias": "a60-private",
            "model": "qwen3-8b-openvino-gpu",
            "workload_id": "chrisops-assistant",
            "hardware_alias": "intel-arc-pro-a60",
            "serving_engine": "openvino",
        },
        schema=schema,
    )

    assert isinstance(provider.client, InstrumentedA60Client)
