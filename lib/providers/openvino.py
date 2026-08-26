#!/usr/bin/env python3

import json
import uuid

from chrisops_state.inference import InferenceRequest

from lib.model_provider import ModelProvider, ProviderInvocation


SYSTEM_PROMPT = (
    "You are a ChrisOps assistant. "
    "Return only valid JSON. "
    "Do not invent operational facts. "
    "Your response must contain exactly "
    "these fields: classification, summary, "
    "explanation, confidence. "
    "Preserve required contract language "
    "from the evidence. "
    "For insufficient observation scenarios, "
    "explicitly state that current state "
    "cannot be confirmed. "
    "Do not claim systems are failed, "
    "offline, fixed, restarted, or remediated "
    "unless explicitly supported by evidence. "
    "Example: "
    '{"classification":"observation-overdue",'
    '"summary":"Observation data delayed.",'
    '"explanation":"The collector did not '
    'provide fresh evidence.",'
    '"confidence":"bounded"}'
)


class OpenVINOProvider(ModelProvider):
    """
    OpenVINO service-backed model provider.

    This provider communicates with the ai-lab OpenAI-compatible
    chat completion service.

    Responsibilities:
    - build inference requests
    - communicate with inference service
    - normalize model responses

    Not responsible for:
    - ChrisOps state interpretation
    - acceptance decisions
    - operational policy
    """

    def __init__(
        self,
        client,
        endpoint,
        endpoint_alias,
        model,
        workload_id,
        hardware_alias,
        serving_engine,
        serving_version=None,
        authorization_token=None,
        timeout_seconds=30,
    ):
        self.client = client
        self.endpoint = endpoint
        self.endpoint_alias = endpoint_alias
        self.model = model
        self.workload_id = workload_id
        self.hardware_alias = hardware_alias
        self.serving_engine = serving_engine
        self.serving_version = serving_version
        self.authorization_token = authorization_token
        self.timeout_seconds = timeout_seconds

    def validate_configuration(self):
        required = {
            "endpoint": self.endpoint,
            "endpoint_alias": self.endpoint_alias,
            "model": self.model,
            "workload_id": self.workload_id,
            "hardware_alias": self.hardware_alias,
            "serving_engine": self.serving_engine,
        }
        if any(not isinstance(value, str) or not value for value in required.values()):
            raise ValueError("OpenVINO provider configuration is incomplete")
        if (
            not isinstance(self.timeout_seconds, (int, float))
            or isinstance(self.timeout_seconds, bool)
            or not 0 < self.timeout_seconds <= 600
        ):
            raise ValueError("OpenVINO timeout must be in (0, 600] seconds")

    def build_request(self, context):
        serialized_context = json.dumps(context, indent=2)
        return InferenceRequest(
            provider="a60_local",
            endpoint_alias=self.endpoint_alias,
            endpoint_url=self.endpoint,
            model=self.model,
            workload_id=self.workload_id,
            request_mode="streaming",
            prompt=serialized_context,
            authorization_token=self.authorization_token,
            chat_messages=(
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": serialized_context,
                },
            ),
            generation_options={
                "max_tokens": 256,
                "temperature": 0.2,
                "enable_thinking": False,
            },
            hardware_alias=self.hardware_alias,
            serving_engine=self.serving_engine,
            serving_version=self.serving_version,
            correlation_run_id=str(uuid.uuid4()),
            caller="chrisops_assistant",
            boundary_workload="agent",
        )

    def normalize_response(self, parsed):
        classification = parsed["classification"]

        summary = parsed["summary"]
        explanation = parsed["explanation"]

        if classification == "insufficient-observation":
            required_phrase = (
                "current state cannot be confirmed"
            )

            combined = (
                f"{summary} {explanation}"
            ).lower()

            if required_phrase not in combined:
                explanation = (
                    f"{explanation} "
                    "Current state cannot be confirmed "
                    "because valid observation data is unavailable."
                )

        return {
            "classification": classification,
            "summary": summary,
            "explanation": explanation,
            "confidence": parsed.get(
                "confidence",
                "bounded",
            ),
        }

    def parse_response(self, content):
        parsed = json.loads(content)

        required_fields = {
            "classification",
            "summary",
            "explanation",
        }

        missing = required_fields - parsed.keys()

        if missing:
            raise ValueError(
                f"model response missing fields: "
                f"{sorted(missing)}"
            )

        return self.normalize_response(parsed)

    def invoke(self, context):
        self.validate_configuration()
        result = self.client.stream(self.build_request(context))
        outcome = result.run.get("outcome", {})
        if outcome.get("status") != "success":
            return ProviderInvocation(
                response=None,
                telemetry_result=result,
                error_category=outcome.get("error_category") or "unknown_safe",
                boundary_telemetry_owned=True,
            )
        try:
            response = self.parse_response(result.content)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            return ProviderInvocation(
                response=None,
                telemetry_result=result,
                error_category="response_protocol",
                boundary_telemetry_owned=True,
            )
        return ProviderInvocation(
            response=response,
            telemetry_result=result,
            boundary_telemetry_owned=True,
        )
