from ai.llm import ChatModel
from google import genai
from google.genai import types
from helpers import EnvHelper
class GeminiModel(ChatModel):
    def __init__(self):
        super().__init__()
        self.API_KEY = EnvHelper().GEMINI_API_KEY
        self.client = genai.Client(api_key=self.API_KEY)

    def answer(self, prompt: str):
        print(f'prompt: {prompt}')
        model = "gemini-2.0-flash-lite"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt),
                ],
            ),
        ]

        generate_content_config = types.GenerateContentConfig(
            temperature=2,
            response_mime_type="text/plain",
        )

        result = ""

        for chunk in self.client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            result += chunk.text
            print(chunk.text, end="")
        
        return result