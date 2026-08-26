#!/usr/bin/env python3

from dataclasses import dataclass

from chrisops_state.inference import InferenceResult


@dataclass(frozen=True)
class ProviderInvocation:
    response: dict | None
    telemetry_result: InferenceResult | None = None
    error_category: str | None = None


class ModelProvider:
    """
    Abstract model provider interface.

    Providers generate response candidates.
    Acceptance validation determines whether those responses are valid.
    """

    def invoke(self, context):
        raise NotImplementedError(
            "Model providers must implement invoke()"
        )
