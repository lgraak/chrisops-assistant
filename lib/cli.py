from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Sequence

from lib.assistant_adapter import AssistantInferenceError, TelemetryPersistenceError
from lib.configuration import AssistantConfigurationError, load_adapter


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate one ChrisOps assistant response.")
    parser.add_argument("fixture", type=Path)
    parser.add_argument(
        "--config",
        type=Path,
        default=os.environ.get("CHRISOPS_ASSISTANT_CONFIG"),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    if arguments.config is None:
        print(json.dumps({"status": "error", "error": "configuration_required"}))
        return 2
    try:
        context = json.loads(arguments.fixture.read_text(encoding="utf-8"))
        adapter = load_adapter(arguments.config)
        response = adapter.generate(context)
    except (OSError, json.JSONDecodeError, AssistantConfigurationError, ValueError):
        print(json.dumps({"status": "error", "error": "configuration_invalid"}))
        return 2
    except TelemetryPersistenceError as exc:
        print(
            json.dumps(
                {
                    "status": "partial",
                    "response": exc.response,
                    "telemetry": {"persistence_status": "failed"},
                },
                indent=2,
            )
        )
        return 1
    except AssistantInferenceError as exc:
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": "assistant_inference_failed",
                    "provider_error_category": exc.category,
                    "telemetry": {
                        "persistence_status": exc.persistence_status,
                    },
                },
                indent=2,
            )
        )
        return 1

    print(json.dumps(response, indent=2))
    return 0
