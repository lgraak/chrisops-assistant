#!/usr/bin/env python3

from pathlib import Path

from lib.model_provider import ModelProvider


class OpenVINOProvider(ModelProvider):
    """
    OpenVINO-backed model provider.

    Initial implementation:
    - validates configuration
    - preserves provider interface
    - provides clear runtime boundary

    Actual inference will be added after the provider
    contract is proven.
    """

    def __init__(
        self,
        model_path=None,
        device="CPU",
    ):
        self.model_path = (
            Path(model_path)
            if model_path
            else None
        )

        self.device = device

    def validate_configuration(self):
        if self.model_path is None:
            raise ValueError(
                "OpenVINO model path is required"
            )

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"OpenVINO model not found: {self.model_path}"
            )

    def generate(self, context):
        self.validate_configuration()

        raise NotImplementedError(
            "OpenVINO inference implementation pending"
        )
