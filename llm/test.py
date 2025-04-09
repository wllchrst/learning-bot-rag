import base64
import os
from google import genai
from google.genai import types

def generate():
    client = genai.Client(
        api_key="AIzaSyAMgwjltJTkN79duoAX2uNCmnVjGOrMxD4",
    )

    model = "gemini-2.0-flash-lite"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Give me code for game using canvas in javascript"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=2,
        response_mime_type="text/plain",
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")