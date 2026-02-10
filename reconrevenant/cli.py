#!/usr/bin/env python3
import argparse

from reconrevenant.parser_nmap import parse_nmap
from reconrevenant.parser_enum import parse_enum
from reconrevenant.signals_builder import build_signals
from reconrevenant.reasoner import infer_attack_chain, infer_missed_enum
from reconrevenant.report import generate_report

# AI imports
from reconrevenant.ai.prompt import build_prompt
from reconrevenant.ai.engine import run_local_model
from reconrevenant.ai.merge import merge_ai_insights
from reconrevenant.ai.safety import prompt_is_safe, output_is_safe


def main():
    parser = argparse.ArgumentParser(description="Recon Revenant")

    parser.add_argument("--nmap", required=True)
    parser.add_argument("--enum", required=True)
    parser.add_argument("--out", default="report.md")

    # AI flags
    parser.add_argument("--ai", action="store_true", help="Enable local AI reasoning")
    parser.add_argument("--model", default="llama3")
    parser.add_argument("--ai-timeout", type=int, default=10)

    args = parser.parse_args()

    print("[INFO] Recon Revenant")
    print("[INFO] Offline mode enforced")
    print("[INFO] No data leaves this machine")
    print("[INFO] Linux + Windows supported")

    with open(args.nmap) as f:
        nmap_txt = f.read()

    with open(args.enum) as f:
        enum_txt = f.read()

    signals = build_signals(parse_nmap(nmap_txt), parse_enum(enum_txt))

    baseline_chain = infer_attack_chain(signals)
    missed = infer_missed_enum(signals)

    # ---------- Optional AI ----------
    if args.ai:
        print("[INFO] Local AI reasoning enabled")

        prompt = build_prompt(signals)

        if not prompt_is_safe(prompt):
            print("[WARN] Prompt failed safety check — skipping AI")
        else:
            ai_output = run_local_model(prompt, args.model, args.ai_timeout)

            if ai_output and output_is_safe(ai_output):
                baseline_chain = merge_ai_insights(baseline_chain, ai_output)
            else:
                print("[WARN] AI output unsafe or empty — ignored")

    report = generate_report(signals, baseline_chain, missed)

    if args.ai:
        report += "\n\n---\nGenerated using **local offline AI**. No data left the system.\n"

    with open(args.out, "w") as f:
        f.write(report)

    print(f"[+] Report written to {args.out}")

