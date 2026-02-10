#!/usr/bin/env python3
import argparse
from reconrevenant.parser_nmap import parse_nmap
from reconrevenant.parser_enum import parse_enum
from reconrevenant.signals_builder import build_signals
from reconrevenant.reasoner import infer_attack_chain, infer_missed_enum
from reconrevenant.report import generate_report


def main():
    parser = argparse.ArgumentParser(description="Recon Revenant")
    parser.add_argument("--nmap", required=True)
    parser.add_argument("--enum", required=True)
    parser.add_argument("--out", default="report.md")
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
    chain = infer_attack_chain(signals)
    missed = infer_missed_enum(signals)

    report = generate_report(signals, chain, missed)

    with open(args.out, "w") as f:
        f.write(report)

    print(f"[+] Report written to {args.out}")

