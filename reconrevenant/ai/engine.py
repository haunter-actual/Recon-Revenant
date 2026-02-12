import subprocess
import time
from typing import Optional


def run_local_model(prompt: str, model: str, timeout: int) -> Optional[str]:
    """
    Stream output from Ollama and return the first completed response.
    Prevents killing slow local models prematurely.
    """
    try:
        proc = subprocess.Popen(
            ["ollama", "run", model, prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        start = time.time()
        output_lines = []

        # Read line-by-line until timeout or process ends
        while True:
            if proc.stdout is None:
                break

            line = proc.stdout.readline()

            if line:
                output_lines.append(line.rstrip())

            # Stop if process finished
            if proc.poll() is not None:
                break

            # Stop if timeout exceeded
            if time.time() - start > timeout:
                proc.kill()
                print("[DEBUG] Ollama streaming timeout reached")
                break

        output = "\n".join(output_lines).strip()
        return output if output else None

    except Exception as e:
        print(f"[DEBUG] Ollama execution error: {e}")
        return None

