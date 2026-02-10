import re


def parse_enum(text: str) -> dict:
    sigs = {
        "filesystem_issues": set(),
        "privilege_vectors": set(),
        "credential_artifacts": set(),
        "token_capabilities": set(),
        "service_misconfigs": set(),
        "kernel_age": None,
        "domain_context": None,
    }

    # ---------- Linux ----------
    if re.search(r"/var/www|writable.*www", text, re.I):
        sigs["filesystem_issues"].add("web_writable_dir")

    if re.search(r"SUID.*env", text):
        sigs["privilege_vectors"].add("suid_env")

    if re.search(r"sudo.*NOPASSWD", text, re.I):
        sigs["privilege_vectors"].add("sudo_nopasswd")

    if re.search(r"linux kernel 4\.", text, re.I):
        sigs["kernel_age"] = "old"

    # ---------- Windows tokens ----------
    if re.search(r"SeImpersonatePrivilege\s+Enabled", text):
        sigs["token_capabilities"].add("se_impersonate")

    if re.search(r"SeAssignPrimaryTokenPrivilege\s+Enabled", text):
        sigs["token_capabilities"].add("se_assign_primary")

    # ---------- Windows services ----------
    if re.search(r"unquoted service path", text, re.I):
        sigs["service_misconfigs"].add("unquoted_service_path")

    if re.search(r"WRITE_DAC|WRITE_OWNER", text):
        sigs["service_misconfigs"].add("weak_service_permissions")

    # ---------- Credentials ----------
    if re.search(r"AutoLogon", text, re.I):
        sigs["credential_artifacts"].add("registry_autologon")

    if re.search(r"password|credential|cleartext", text, re.I):
        sigs["credential_artifacts"].add("possible_creds")

    # ---------- Domain context ----------
    if re.search(r"Domain:\s+\S+", text):
        sigs["domain_context"] = "domain"
    else:
        sigs["domain_context"] = "standalone"

    return sigs

