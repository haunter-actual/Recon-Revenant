def infer_attack_chain(signals):
    chain = []

    # ---------- Windows ----------
    if signals.os_family == "windows":
        chain.append("Initial foothold as low-privileged user")

        if signals.credential_artifacts:
            chain.append("Credential-based privilege escalation")

        if signals.token_capabilities:
            chain.append("Token manipulation privilege escalation")

        if signals.service_misconfigs:
            chain.append("Service configuration abuse")

        if len(chain) == 1:
            chain.append("Insufficient Windows privilege escalation signals")

        return chain

    # ---------- Linux ----------
    if "http" in signals.services:
        chain.append("Web service enumeration")

        if "web_writable_dir" in signals.filesystem_issues:
            chain.append("File upload or writable web path abuse")

    if signals.credential_artifacts:
        chain.append("Credential reuse or privilege escalation")

    if signals.privilege_vectors:
        chain.append("Local privilege escalation")

    if not chain:
        chain.append("Insufficient signals for confident chain")

    return chain


def infer_missed_enum(signals):
    missed = []

    if signals.os_family == "windows":
        if not signals.token_capabilities:
            missed.append("Privilege token enumeration")

        if not signals.service_misconfigs:
            missed.append("Service permission and path checks")

        if signals.domain_context == "domain" and not signals.credential_artifacts:
            missed.append("Domain credential and policy enumeration")

        return missed

    # Linux
    if "http" in signals.services and "web_writable_dir" not in signals.filesystem_issues:
        missed.append("Deeper web content enumeration")

    if signals.kernel_age == "old" and not signals.privilege_vectors:
        missed.append("Kernel privilege escalation checks")

    if "ssh" in signals.services and not signals.credential_artifacts:
        missed.append("Credential discovery for SSH access")

    return missed

