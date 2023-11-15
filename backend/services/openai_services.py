import openai
import os

def chat_with_openai(messages):
    openai.api_key = os.getenv('OPENAI_API_KEY')

    completion = openai.ChatCompletion.create(
        model=os.getenv('OPENAI_CHATCOMPLETION_MODEL'),
        messages=messages
    )

    return completion.choices[0].message["content"]
