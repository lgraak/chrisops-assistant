#!/usr/bin/env python3

from chrisops_state.inference_persistence import (
    DuplicateInferenceRunError,
    InferencePersistenceError,
)


class AssistantInferenceError(RuntimeError):
    def __init__(self, category, persistence_status):
        super().__init__("assistant inference provider request failed")
        self.category = category
        self.persistence_status = persistence_status


class TelemetryPersistenceError(RuntimeError):
    def __init__(self, response):
        super().__init__("assistant inference succeeded but telemetry persistence failed")
        self.response = response
        self.persistence_status = "failed"


class AssistantAdapter:
    """
    Assistant orchestration layer.

    The adapter does not generate responses itself.
    It delegates generation to a model provider.
    """

    def __init__(self, provider, *, persistence_enabled=False, store=None):
        if not isinstance(persistence_enabled, bool):
            raise ValueError("persistence_enabled must be boolean")
        if persistence_enabled and store is None:
            raise ValueError("persistence store is required when persistence is enabled")
        self.provider = provider
        self.persistence_enabled = persistence_enabled
        self.store = store

    def generate(self, context):
        invocation = self.provider.invoke(context)
        persistence_status = "disabled"

        if invocation.telemetry_result is not None and self.persistence_enabled:
            try:
                inserted = self.store.write_run(invocation.telemetry_result.run)
                persistence_status = "persisted" if inserted else "replayed"
            except DuplicateInferenceRunError:
                if invocation.error_category is not None:
                    raise AssistantInferenceError(
                        invocation.error_category, "failed"
                    ) from None
                raise
            except InferencePersistenceError:
                if invocation.error_category is not None:
                    raise AssistantInferenceError(
                        invocation.error_category, "failed"
                    ) from None
                raise TelemetryPersistenceError(invocation.response) from None

        if invocation.error_category is not None:
            raise AssistantInferenceError(
                invocation.error_category, persistence_status
            )
        if invocation.response is None:
            raise AssistantInferenceError("response_protocol", persistence_status)
        return invocation.response
