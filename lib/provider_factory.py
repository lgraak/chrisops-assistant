#!/usr/bin/env python3

from lib.providers.deterministic import DeterministicProvider
from lib.providers.openvino import OpenVINOProvider


def get_provider(config):
    provider_type = config.get(
        "type",
        "deterministic",
    )

    if provider_type == "deterministic":
        return DeterministicProvider()

    if provider_type == "openvino":
        return OpenVINOProvider(
            endpoint=config.get("endpoint"),
            model=config.get("model"),
            timeout_seconds=config.get(
                "timeout_seconds",
                30,
            ),
        )

    raise ValueError(
        f"unsupported provider type: {provider_type}"
    )
