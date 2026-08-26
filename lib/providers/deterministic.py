#!/usr/bin/env python3

from lib.model_provider import ModelProvider, ProviderInvocation


class DeterministicProvider(ModelProvider):
    def invoke(self, context):
        classification = context["expected"]["classification"]

        summaries = {
            "active-finding":
                "A finding exists and requires review.",

            "insufficient-observation":
                "Current state cannot be confirmed due to insufficient observation data.",

            "observation-overdue":
                "Observation data delayed.",

            "notification-policy":
                "A finding exists, but notification policy must be evaluated separately.",
        }

        return ProviderInvocation(
            response={
                "classification": classification,
                "summary": summaries.get(
                    classification,
                    "The condition requires review.",
                ),
                "explanation": context.get(
                    "description",
                    "Evidence was provided by ChrisOps.",
                ),
                "confidence": "bounded",
            }
        )
