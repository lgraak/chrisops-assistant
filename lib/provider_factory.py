#!/usr/bin/env python3

from lib.providers.deterministic import DeterministicProvider


def get_provider(config):
    provider_type = config.get(
        "type",
        "deterministic",
    )

    if provider_type == "deterministic":
        return DeterministicProvider()

    raise ValueError(
        f"unsupported provider type: {provider_type}"
    )

