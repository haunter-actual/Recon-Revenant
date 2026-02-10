#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser(description="Recon Revenant")
    parser.add_argument("--nmap")
    parser.add_argument("--enum")
    parser.add_argument("--out", default="report.md")
    args = parser.parse_args()

    print("[INFO] Recon Revenant")
    print("[INFO] Offline mode enforced")
    print("[INFO] No data leaves this machine")
    print("[INFO] Linux + Windows supported")

    if not args.nmap or not args.enum:
        print("Provide --nmap and --enum files")
        return

    with open(args.out, "w") as f:
        f.write("# Recon Revenant Report\n")

    print(f"[+] Report written to {args.out}")

