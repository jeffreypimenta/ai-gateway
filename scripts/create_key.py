"""Create a constrained LiteLLM API key via the proxy admin endpoint."""
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
master_key = os.getenv("LITELLM_MASTER_KEY")
base_url = os.getenv("LITELLM_BASE_URL", "http://127.0.0.1:4000").rstrip("/")
if not master_key:
    raise SystemExit("Missing LITELLM_MASTER_KEY. Run scripts/init_env.py first.")

payload = {
    "key_alias": "local-demo-client",
    "models": ["assistant", "assistant-backup"],
    "max_budget": 1.00,   # $1.00 per 30-day window
    "budget_duration": "30d",
    "rpm_limit": 10,
    "tpm_limit": 10_000,
}
request = Request(
    url=f"{base_url}/key/generate",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Authorization": f"Bearer {master_key}", "Content-Type": "application/json"},
    method="POST",
)
try:
    with urlopen(request, timeout=30) as response:
        result = json.load(response)
except HTTPError as exc:
    raise SystemExit(f"LiteLLM returned HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')}") from exc
except URLError as exc:
    raise SystemExit(f"Cannot reach LiteLLM at {base_url}: {exc}") from exc

key = result.get("key")
if not key:
    raise SystemExit(f"LiteLLM did not return a key: {result}")
print("Created a virtual key with a $1 / 30-day budget and 10 RPM limit.")
print("Store the following key securely; it is shown only at creation:")
print(key)
print("\nPaste it into the LITELLM_VIRTUAL_KEY= field in .env and rerun client.py.")
