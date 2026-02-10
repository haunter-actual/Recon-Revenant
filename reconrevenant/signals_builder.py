from .signals import Signals


def build_signals(nmap_sigs: dict, enum_sigs: dict) -> Signals:
    s = Signals()

    s.services = sorted(nmap_sigs.get("services", []))
    s.os_family = nmap_sigs.get("os_family")

    s.filesystem_issues = sorted(enum_sigs.get("filesystem_issues", []))
    s.privilege_vectors = sorted(enum_sigs.get("privilege_vectors", []))
    s.credential_artifacts = sorted(enum_sigs.get("credential_artifacts", []))

    s.token_capabilities = sorted(enum_sigs.get("token_capabilities", []))
    s.service_misconfigs = sorted(enum_sigs.get("service_misconfigs", []))

    s.kernel_age = enum_sigs.get("kernel_age")
    s.domain_context = enum_sigs.get("domain_context")

    return s

