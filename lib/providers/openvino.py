#!/usr/bin/env python3

import json

import requests

from lib.model_provider import ModelProvider


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
        endpoint,
        model,
        timeout_seconds=30,
    ):
        self.endpoint = endpoint.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds

    def validate_configuration(self):
        if not self.endpoint:
            raise ValueError(
                "OpenVINO endpoint is required"
            )

        if not self.model:
            raise ValueError(
                "OpenVINO model is required"
            )

    def build_request(self, context):
        return {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
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
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        context,
                        indent=2,
                    ),
                },
            ],
            "max_tokens": 256,
            "temperature": 0.2,
            "stream": False,
            "enable_thinking": False,
        }

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

    def parse_response(self, response):
        content = (
            response["choices"][0]
            ["message"]
            ["content"]
        )

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

    def generate(self, context):
        self.validate_configuration()

        request = self.build_request(context)

        response = requests.post(
            f"{self.endpoint}/v1/chat/completions",
            json=request,
            timeout=self.timeout_seconds,
        )

        response.raise_for_status()

        return self.parse_response(
            response.json()
        )
