class AIResponseError(Exception):
    pass


class AIClient:
    """
    Abstract AI client.
    OpenAI / Claude / Local LLM will implement this later.
    """

    async def generate(self, prompt: str) -> str:
        raise NotImplementedError
