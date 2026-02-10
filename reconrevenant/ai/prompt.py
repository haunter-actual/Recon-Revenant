import json
from reconrevenant.signals import Signals


def build_prompt(signals: Signals) -> str:
    data = {
        "os_family": signals.os_family,
        "services": signals.services,
        "filesystem_issues": signals.filesystem_issues,
        "credential_artifacts": signals.credential_artifacts,
        "privilege_vectors": signals.privilege_vectors,
        "token_capabilities": signals.token_capabilities,
        "service_misconfigs": signals.service_misconfigs,
        "kernel_age": signals.kernel_age,
        "domain_context": signals.domain_context,
    }

    return f"""
You are assisting with cybersecurity training analysis.

You receive ONLY abstracted enumeration signals in JSON.

Signals:
{json.dumps(data, indent=2)}

Tasks:
- Infer plausible attack phases
- Identify likely missed enumeration
- Provide exam-relevant learning insights

STRICT RULES:
- Do NOT provide commands.
- Do NOT provide exploits or payloads.
- Do NOT guess hidden data.
- Reason only from signals.

Return concise bullet points.
""".strip()

