from mistralai import Mistral
from typing import List, Dict


class MistralAI:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.client = Mistral(api_key=self.api_key)

    async def generate(
        self, messages: List[Dict[str, str]], model: str = "mistral-small-latest"
    ):

        res = await self.client.chat.complete_async(model=model, messages=messages)
        return res
