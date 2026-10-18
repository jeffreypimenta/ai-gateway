"""Generate a local .env with unique credentials without overwriting an existing one."""
from pathlib import Path
import secrets

ROOT = Path(__file__).resolve().parents[1]
target = ROOT / ".env"
# if target.exists():
#     raise SystemExit(".env already exists. Keeping existing credentials; edit it instead.")

contents = (ROOT / ".env").read_text(encoding="utf-8")
contents = contents.replace(
    "LITELLM_MASTER_KEY=sk-CHANGE_ME",
    f"LITELLM_MASTER_KEY=sk-{secrets.token_hex(32)}",
)
contents = contents.replace(
    "LITELLM_SALT_KEY=sk-CHANGE_ME",
    f"LITELLM_SALT_KEY=sk-{secrets.token_hex(32)}",
)
contents = contents.replace(
    "POSTGRES_PASSWORD=CHANGE_ME",
    f"POSTGRES_PASSWORD={secrets.token_hex(24)}",
)
with target.open("w+", encoding="utf-8") as handle:
    handle.write(contents)
target.chmod(0o600)
print("Created .env with randomized master key, salt, and database password.")
print("Edit .env to set OPENAI_API_KEY and ANTHROPIC_API_KEY before starting Docker.")
print("Keep LITELLM_SALT_KEY unchanged while reusing this database volume.")
