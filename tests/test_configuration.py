from __future__ import annotations

import json

import pytest
import yaml

from lib.configuration import AssistantConfigurationError, load_adapter


def _write(path, document):
    path.write_text(yaml.safe_dump(document), encoding="utf-8")
    return path


def test_deterministic_configuration_defaults_persistence_off(tmp_path):
    adapter = load_adapter(
        _write(
            tmp_path / "assistant.yml",
            {
                "provider": {"type": "deterministic"},
                "telemetry": {"persistence_enabled": False},
            },
        )
    )

    assert adapter.persistence_enabled is False
    assert adapter.store is None


def test_openvino_configuration_builds_strict_existing_store_without_opening_it(
    tmp_path,
):
    schema = tmp_path / "schema.json"
    schema.write_text(
        json.dumps(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
            }
        ),
        encoding="utf-8",
    )
    database = tmp_path / "missing.sqlite3"
    adapter = load_adapter(
        _write(
            tmp_path / "assistant.yml",
            {
                "provider": {
                    "type": "openvino",
                    "endpoint": "https://a60.example.invalid/v1/chat/completions",
                    "endpoint_alias": "a60-private",
                    "model": "qwen3-8b-openvino-gpu",
                    "workload_id": "chrisops-assistant",
                    "hardware_alias": "intel-arc-pro-a60",
                    "serving_engine": "openvino",
                    "schema_path": str(schema),
                },
                "telemetry": {
                    "persistence_enabled": True,
                    "database_path": str(database),
                },
            },
        )
    )

    assert adapter.persistence_enabled is True
    assert adapter.store.require_existing is True
    assert not database.exists()


def test_disabled_workflow_fails_before_provider_or_persistence_setup(tmp_path):
    with pytest.raises(AssistantConfigurationError, match="workflow is disabled"):
        load_adapter(
            _write(
                tmp_path / "assistant.yml",
                {
                    "runtime": {"workflow_enabled": False},
                    "provider": {"type": "openvino"},
                    "telemetry": {"persistence_enabled": False},
                },
            )
        )


@pytest.mark.parametrize(
    "document",
    [
        {"provider": {"type": "deterministic"}, "telemetry": {"persistence_enabled": "yes"}},
        {"provider": {"type": "deterministic"}, "telemetry": {"persistence_enabled": True}},
        {"provider": {"type": "openvino"}, "telemetry": {"persistence_enabled": False}},
    ],
)
def test_malformed_or_unsafe_configuration_fails_closed(tmp_path, document):
    with pytest.raises(AssistantConfigurationError):
        load_adapter(_write(tmp_path / "assistant.yml", document))
