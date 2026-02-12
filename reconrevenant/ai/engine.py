import subprocess
from typing import Optional


def run_local_model(prompt: str, model: str, timeout: int | None) -> Optional[str]:
    """
    Execute Ollama in fully blocking mode.

    Rationale:
    - Local LLM first-token latency is unpredictable.
    - Hard timeouts break legitimate slow inference.
    - User can cancel safely with Ctrl-C.

    Therefore:
    → No enforced timeout by default.
    """

    try:
        proc = subprocess.run(
            ["ollama", "run", model, prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
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

