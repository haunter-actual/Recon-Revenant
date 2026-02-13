#!/usr/bin/env python3
"""
Recon Revenant CLI

Offline reconnaissance reasoning engine supporting:

• Deterministic attack-path inference
• Optional local-only AI reasoning (Ollama)
• Flexible input: Nmap, PEAS, or both
• Zero telemetry, zero cloud, NDA-safe execution
"""

import argparse
import shutil

from reconrevenant.parser_nmap import parse_nmap
from reconrevenant.parser_enum import parse_enum
from reconrevenant.signals_builder import build_signals
from reconrevenant.reasoner import infer_attack_chain, infer_missed_enum
from reconrevenant.report import generate_report

from reconrevenant.ai.prompt import build_prompt
from reconrevenant.ai.engine import run_local_model
from reconrevenant.ai.merge import merge_ai_insights
from reconrevenant.ai.safety import prompt_is_safe, output_is_safe


BANNER = r"""
______                      ______                                 _
| ___ \                     | ___ \                               | |
| |_/ /___  ___ ___  _ __   | |_/ /_____   _____ _ __   __ _ _ __ | |_
|    // _ \/ __/ _ \| '_ \  |    // _ \ \ / / _ \ '_ \ / _` | '_ \| __|
| |\ \  __/ (_| (_) | | | | | |\ \  __/\ V /  __/ | | | (_| | | | | |_
\_| \_\___|\___\___/|_| |_| \_| \_\___| \_/ \___|_| |_|\__,_|_| |_|\__|

Recon Revenant — Offline Recon Deterministic & Local AI Reasoning Engine
Author: haunter-actual
https://haunter-actual.github.io
"""

def ollama_available() -> bool:
    return shutil.which("ollama") is not None or shutil.which("ollama.exe") is not None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Recon Revenant — Offline deterministic & local-AI recon reasoning engine"
    )

    # Flexible inputs
    parser.add_argument("--nmap", help="Path to Nmap output file")
    parser.add_argument("--enum", help="Path to LinPEAS/WinPEAS output file")
    parser.add_argument("--out", default="report.md", help="Output Markdown report file")

    # Local AI (optional)
    parser.add_argument("--ai", action="store_true", help="Enable local AI reasoning via Ollama")
    parser.add_argument("--model", default="llama3", help="Local Ollama model name")
    parser.add_argument(
        "--ai-timeout",
        type=int,
        default=0,
        help="AI timeout seconds (0 = wait indefinitely)",
    )

    args = parser.parse_args()

    print(BANNER)

    # Require at least one data source
    if not args.nmap and not args.enum:
        parser.error("Provide --nmap, --enum, or both.")

    nmap_sigs = {}
    enum_sigs = {}

    if args.nmap:
        from pathlib import Path
        with Path(args.nmap).open("r", encoding="utf-8", errors="ignore") as f:
            nmap_sigs = parse_nmap(f.read())

    if args.enum:
        from pathlib import Path
        with Path(args.enum).open("r", encoding="utf-8", errors="ignore") as f:
            enum_sigs = parse_enum(f.read())

    signals = build_signals(nmap_sigs, enum_sigs)

    # Deterministic reasoning always runs
    chain = infer_attack_chain(signals)
    missed = infer_missed_enum(signals)

    # Optional local AI reasoning
    if args.ai:
        if not ollama_available():
            print("[WARN] Ollama not installed — AI reasoning skipped.")
            print("Install from: https://ollama.com")
            print("Then run: ollama pull llama3")
        else:
            prompt = build_prompt(signals)

            if not prompt_is_safe(prompt):
                print("[WARN] Prompt failed safety validation — skipping AI.")
            else:
                ai_out = run_local_model(prompt, args.model, args.ai_timeout)

                if ai_out and output_is_safe(ai_out):
                    chain = merge_ai_insights(chain, ai_out)
                else:
                    print("[WARN] AI output unsafe or empty — ignored.")

    report = generate_report(signals, chain, missed)

    if args.ai and ollama_available():
        report += "\n\n---\nGenerated using local offline AI reasoning.\n"

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"[+] Report written to {args.out}")

