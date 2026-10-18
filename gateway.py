import os, sys
import litellm
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

if openai_key:
    print("OpenAI API key found")
else:
    print("OpenAI API key not found")

messages = [
#    {"role": "user", "content": "Write a simple Python function that adds two numbers"},
   {"role": "user", "content": "Define JavaScript in exactly two sentences"}
]

try:
   response = litellm.completion(
       model="gpt-5",
       messages=messages,
    #    fallbacks=["gpt-5.5"],
    #    num_retries=2,
       stream=True
   )
#    for chunk in response:
#     if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
#        print(f"'{chunk.choices[0].delta.content}'", end=" ")
except Exception as e:
   print(f"API call failed: {e}")


for chunk in response:
    if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content:
       print(f"'{chunk.choices[0].delta.content}'", end=" ")
# print(f"Model used: {response.model}")
# print(f"Response ID: {response.id}")
# print(f"Total tokens: {response.usage.total_tokens}")
