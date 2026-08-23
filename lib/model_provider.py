#!/usr/bin/env python3


class ModelProvider:
    """
    Abstract model provider interface.

    Providers generate response candidates.
    Acceptance validation determines whether those responses are valid.
    """

    def generate(self, context):
        raise NotImplementedError(
            "Model providers must implement generate()"
        )
