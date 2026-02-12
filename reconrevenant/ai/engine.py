import subprocess
from typing import Optional


def run_local_model(prompt: str, model: str, timeout: int) -> Optional[str]:
    """
    Execute a local Ollama model in non-interactive mode.
    Returns stripped stdout text or None.
    """
    try:
        proc = subprocess.run(
            ["ollama", "run", model, prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=timeout,
            text=True,
        )

        output = proc.stdout.strip()
        return output if output else None

    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None

