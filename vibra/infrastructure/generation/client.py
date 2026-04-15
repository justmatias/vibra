from functools import cached_property

import stamina
from openai import AsyncOpenAI
from pydantic import BaseModel

from vibra.utils import LogLevel, Settings, log

from .config import RETRY_ON


class LLMClient(BaseModel):
    @cached_property
    def client(self) -> AsyncOpenAI:
        return AsyncOpenAI(base_url=Settings.LLM_BASE_URL, api_key=Settings.LLM_API_KEY)

    @stamina.retry(on=RETRY_ON, attempts=3)
    async def generate(self, prompt: str) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=Settings.LLM_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=Settings.TEMPERATURE,
            )
            return response.choices[0].message.content.strip()  # type: ignore[no-any-return]
        except RETRY_ON:  # pragma: no cover
            raise
        except Exception as e:
            log(f"LLM generation failed: {e}", LogLevel.ERROR)
            raise RuntimeError(f"Failed to generate text: {e}") from e
