import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("GEMINI_API_KEY is not set")

# accept user prompt as command line argument
parser = argparse.ArgumentParser()
parser.add_argument("user_prompt", type=str, help="The user prompt to send to the model")
parser.add_argument("--verbose", action="store_true", help="Whether to print the verbose output")
args = parser.parse_args()

user_prompt = args.user_prompt
verbose = args.verbose

if user_prompt is None:
    raise RuntimeError("Prompt is not set")

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=messages,
)

if response.usage_metadata == None:
    raise RuntimeError("Usage metadata is None")

if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

print(response.text)