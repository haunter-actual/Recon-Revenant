def generate_mermaid(chain):
    lines = ["```mermaid", "graph TD"]
    for i in range(len(chain) - 1):
        lines.append(f'  A{i}["{chain[i]}"] --> A{i+1}["{chain[i+1]}"]')
    lines.append("```")
    return "\n".join(lines)

BANNER = """
______                      ______                                 _
| ___ \                     | ___ \                               | |
| |_/ /___  ___ ___  _ __   | |_/ /_____   _____ _ __   __ _ _ __ | |_
|    // _ \/ __/ _ \| '_ \  |    // _ \ \ / / _ \ '_ \ / _` | '_ \| __|
| |\ \  __/ (_| (_) | | | | | |\ \  __/\ V /  __/ | | | (_| | | | | |_
\_| \_\___|\___\___/|_| |_| \_| \_\___| \_/ \___|_| |_|\__,_|_| |_|\__|


Recon Revenant — Offline Recon Deterministic & Local AI Reasoning Engine
Author: haunter-actual
Website: https://haunter-actual.github.io
LinkedIn: gsmaciel
"""


def generate_report(signals, chain, missed):
    lines = []

    lines.append("```\n" + BANNER.strip() + "\n```\n")
    lines.append("# Recon Revenant Report\n")

    lines.append("## Attack Chain")
    for i, step in enumerate(chain, 1):
        lines.append(f"{i}. {step}")

    lines.append("\n## Enumeration Signals")
    lines.append(f"- OS: {signals.os_family or 'unknown'}")
    lines.append(f"- Services: {', '.join(signals.services) or 'None'}")
    lines.append(f"- Filesystem: {', '.join(signals.filesystem_issues) or 'None'}")
    lines.append(f"- PrivEsc: {', '.join(signals.privilege_vectors) or 'None'}")
    lines.append(f"- Tokens: {', '.join(signals.token_capabilities) or 'None'}")
    lines.append(f"- Services Misconfig: {', '.join(signals.service_misconfigs) or 'None'}")

    lines.append("\n## Likely Missed Enumeration")
    for m in missed:
        lines.append(f"- {m}")

    lines.append("\n## Attack Flow Diagram")
    lines.append(generate_mermaid(chain))

    lines.append("\n## Exam Takeaways")
    lines.append("- Follow signals, not guesswork")
    lines.append("- Privilege mechanics matter more than exploits")
    lines.append("- Enumeration depth determines success")

    return "\n".join(lines)
