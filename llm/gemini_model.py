from llm import ChatModel
from google import genai
from google.genai import types
from helpers import EnvHelper
class GeminiModel(ChatModel):
    def __init__(self):
        super().__init__()
        self.API_KEY = EnvHelper().GEMINI_API_KEY
        self.client = genai.Client(api_key=self.API_KEY)

    def answer(self, initial_input: str):
        model = "gemini-2.0-flash-lite"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=initial_input),
                ],
            ),
        ]

        generate_content_config = types.GenerateContentConfig(
            temperature=2,
            response_mime_type="text/plain",
        )

        for chunk in self.client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            print(chunk.text, end="")

    def get_data(self, input: str):
        pass