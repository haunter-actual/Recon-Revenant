import subprocess
import shutil
from typing import Optional


def _ollama_cmd() -> Optional[str]:
    """Locate Ollama executable cross-platform."""
    return shutil.which("ollama") or shutil.which("ollama.exe")


def run_local_model(prompt: str, model: str, timeout: int | None) -> Optional[str]:
    """
    Execute Ollama locally with explicit UTF-8 decoding.

    Fixes Windows cp1252 UnicodeDecodeError.
    """

    cmd = _ollama_cmd()
    if not cmd:
        return None

    try:
        proc = subprocess.run(
            [cmd, "run", model, prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",          # ← CRITICAL FIX
            errors="replace",          # ← prevents crashes
            timeout=timeout if timeout and timeout > 0 else None,
        )

        output = proc.stdout.strip()
        return output if output else None

    except subprocess.TimeoutExpired:
        print("[WARN] AI inference exceeded user timeout.")
        return None

    except KeyboardInterrupt:
        print("\n[INFO] AI cancelled by user.")
        return None

    except Exception as e:
        print(f"[DEBUG] Ollama execution error: {e}")
        return None

