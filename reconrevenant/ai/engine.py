import subprocess
from typing import Optional


def run_local_model(prompt: str, model: str, timeout: int) -> Optional[str]:
    """
    Calls Ollama locally.
    Returns text or None on failure.
    """

    try:
        proc = subprocess.run(
            ["ollama", "run", model],
            input=prompt.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=timeout,
        )
        return proc.stdout.decode().strip() or None

    except Exception:
        return None

