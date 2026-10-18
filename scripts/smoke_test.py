"""Check the gateway and routing. The optional chat call uses paid provider tokens."""
import argparse
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
base_url = os.getenv("LITELLM_BASE_URL", "http://127.0.0.1:4000").rstrip("/")
key = os.getenv("LITELLM_VIRTUAL_KEY") or os.getenv("LITELLM_MASTER_KEY")

parser = argparse.ArgumentParser(description="Check LiteLLM model visibility and optional inference")
parser.add_argument("--chat", action="store_true", help="Also perform a real (billable) inference call")
args = parser.parse_args()
if not key:
    raise SystemExit("Missing LiteLLM virtual or master key in .env")


def call(path: str, body: dict | None = None) -> dict:
    headers = {"Authorization": f"Bearer {key}"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = Request(
        base_url + path,
        data=json.dumps(body).encode("utf-8") if body is not None else None,
        headers=headers,
        method="POST" if body is not None else "GET",
    )
    try:
        with urlopen(req, timeout=60) as response:
            return json.load(response)
    except HTTPError as exc:
        raise SystemExit(f"HTTP {exc.code} at {path}: {exc.read().decode('utf-8', 'replace')}") from exc
    except URLError as exc:
        raise SystemExit(f"Cannot connect to gateway at {base_url}: {exc}") from exc


models = call("/v1/models")
visible = {m["id"] for m in models.get("data", [])}
assert {"assistant", "assistant-backup"} <= visible, f"Missing model groups: {visible}"
print(f"PASS: Both model groups visible via {base_url}/v1/models")

if args.chat:
    output = call("/v1/chat/completions", {
        "model": "assistant",
        "messages": [{"role": "user", "content": "Say only: gateway works"}],
        "max_tokens": 20,
    })
    assert output.get("choices"), output
    print("PASS: Inference succeeded:", output["choices"][0]["message"].get("content"))
