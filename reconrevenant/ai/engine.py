import subprocess
from typing import Optional


def run_local_model(prompt: str, model: str, timeout: int) -> Optional[str]:
    """
    Runs an Ollama model and returns stdout.
    Also prints debug info if output is empty.
    """
    try:
        proc = subprocess.run(
            ["ollama", "run", model, prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
        )

        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()

        # ---- DEBUG VISIBILITY ----
        if not stdout:
            print("[DEBUG] Ollama returned EMPTY stdout")
            if stderr:
                print("[DEBUG] Ollama stderr:")
                print(stderr)

        return stdout if stdout else None

    except subprocess.TimeoutExpired:
        print("[DEBUG] Ollama timed out")
        return None

    except Exception as e:
        print(f"[DEBUG] Ollama execution error: {e}")
        return None

