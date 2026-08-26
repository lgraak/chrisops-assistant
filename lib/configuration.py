from __future__ import annotations

import json
from pathlib import Path

import yaml

from chrisops_state.inference_persistence import InferenceRunStore

from lib.assistant_adapter import AssistantAdapter
from lib.provider_factory import get_provider


class AssistantConfigurationError(ValueError):
    pass


def load_adapter(configuration_path: str | Path) -> AssistantAdapter:
    try:
        document = yaml.safe_load(Path(configuration_path).read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise AssistantConfigurationError(
            "assistant configuration could not be loaded"
        ) from exc
    if not isinstance(document, dict):
        raise AssistantConfigurationError("assistant configuration must be a mapping")

    provider_config = document.get("provider")
    telemetry_config = document.get("telemetry", {"persistence_enabled": False})
    runtime_config = document.get("runtime", {"workflow_enabled": True})
    if (
        not isinstance(provider_config, dict)
        or not isinstance(telemetry_config, dict)
        or not isinstance(runtime_config, dict)
    ):
        raise AssistantConfigurationError("assistant configuration sections are invalid")
    workflow_enabled = runtime_config.get("workflow_enabled", True)
    if not isinstance(workflow_enabled, bool):
        raise AssistantConfigurationError("workflow_enabled must be boolean")
    if not workflow_enabled:
        raise AssistantConfigurationError("assistant inference workflow is disabled")

    provider_type = provider_config.get("type", "deterministic")
    schema = None
    authorization_token = None
    if provider_type == "openvino":
        schema_path = _required_path(provider_config, "schema_path")
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise AssistantConfigurationError(
                "inference schema could not be loaded"
            ) from exc
        credential_file = provider_config.get("credential_file")
        if credential_file is not None:
            if not isinstance(credential_file, str) or not credential_file:
                raise AssistantConfigurationError("credential_file must be a path")
            try:
                authorization_token = Path(credential_file).read_text(
                    encoding="utf-8"
                ).strip()
            except OSError as exc:
                raise AssistantConfigurationError(
                    "provider credential could not be loaded"
                ) from exc
            if not authorization_token:
                raise AssistantConfigurationError("provider credential is empty")

    enabled = telemetry_config.get("persistence_enabled", False)
    if not isinstance(enabled, bool):
        raise AssistantConfigurationError("persistence_enabled must be boolean")
    if enabled and provider_type != "openvino":
        raise AssistantConfigurationError(
            "telemetry persistence requires an instrumented provider"
        )

    try:
        provider = get_provider(
            provider_config,
            schema=schema,
            authorization_token=authorization_token,
        )
    except (TypeError, ValueError) as exc:
        raise AssistantConfigurationError("provider configuration is invalid") from exc

    store = None
    if enabled:
        database_path = _required_path(telemetry_config, "database_path")
        store = InferenceRunStore(
            database_path=database_path,
            schema=schema,
            require_existing=True,
        )
    return AssistantAdapter(
        provider, persistence_enabled=enabled, store=store
    )


def _required_path(mapping: dict, name: str) -> Path:
    value = mapping.get(name)
    if not isinstance(value, str) or not value:
        raise AssistantConfigurationError(f"{name} must be a path")
    return Path(value)
