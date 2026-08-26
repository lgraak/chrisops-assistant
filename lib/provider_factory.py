#!/usr/bin/env python3

from lib.providers.deterministic import DeterministicProvider
from lib.providers.openvino import OpenVINOProvider
from chrisops_state.inference import (
    InstrumentedA60Client,
    UrllibOpenAIStreamingTransport,
)


def get_provider(config, *, schema=None, authorization_token=None, client=None):
    provider_type = config.get(
        "type",
        "deterministic",
    )

    if provider_type == "deterministic":
        return DeterministicProvider()

    if provider_type == "openvino":
        if schema is None:
            raise ValueError("OpenVINO provider requires the ChrisOps inference schema")
        timeout_seconds = config.get("timeout_seconds", 30)
        instrumented_client = client or InstrumentedA60Client(
            schema=schema,
            transport=UrllibOpenAIStreamingTransport(
                timeout_seconds=timeout_seconds
            ),
        )
        return OpenVINOProvider(
            client=instrumented_client,
            endpoint=config.get("endpoint"),
            endpoint_alias=config.get("endpoint_alias"),
            model=config.get("model"),
            workload_id=config.get("workload_id"),
            hardware_alias=config.get("hardware_alias"),
            serving_engine=config.get("serving_engine"),
            serving_version=config.get("serving_version"),
            authorization_token=authorization_token,
            timeout_seconds=timeout_seconds,
        )

    raise ValueError(
        f"unsupported provider type: {provider_type}"
    )
