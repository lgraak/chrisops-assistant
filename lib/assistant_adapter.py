#!/usr/bin/env python3


class AssistantAdapter:
    """
    Assistant orchestration layer.

    The adapter does not generate responses itself.
    It delegates generation to a model provider.
    """

    def __init__(self, provider):
        self.provider = provider

    def generate(self, context):
        return self.provider.generate(context)
