import argparse
import os
from pathlib import Path
import sys

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).with_name(".env"))


def main() -> None:
    parser = argparse.ArgumentParser(description="LiteLLM demo client")
    parser.add_argument("prompt", nargs="?", default="Explain what an AI gateway does in one sentence.")
    parser.add_argument("--model", choices=["assistant", "assistant-backup"], default="assistant")
    args = parser.parse_args()

    key = os.getenv("LITELLM_VIRTUAL_KEY") or os.getenv("LITELLM_MASTER_KEY")
    if not key:
        raise SystemExit("Missing LITELLM_VIRTUAL_KEY or LITELLM_MASTER_KEY in .env")
    if not os.getenv("LITELLM_VIRTUAL_KEY"):
        print("Using admin master key for this first test. Create a virtual key for regular use.", file=sys.stderr)

    client = OpenAI(
        api_key=key,
        base_url=os.getenv("LITELLM_BASE_URL", "http://127.0.0.1:4000").rstrip("/") + "/v1",
        timeout=45,
        max_retries=0,
    )
    try:
        response = client.chat.completions.create(
            model=args.model,
            messages=[{"role": "user", "content": args.prompt}],
            max_tokens=150,
        )
    except Exception as exc:
        raise SystemExit(f"Gateway request failed: {exc}") from exc

    print(f"Requested model group: {args.model}")
    print(f"Backend model reported: {response.model}")
    print(f"Response: {response.choices[0].message.content}")


if __name__ == "__main__":
    main()
