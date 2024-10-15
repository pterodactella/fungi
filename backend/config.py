import getpass
import os
from dotenv import load_dotenv
from openai import OpenAI


def load_env_variables():
    load_dotenv()
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")


load_env_variables()
# Initialize the OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def chat_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
