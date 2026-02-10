import re


def parse_nmap(text: str) -> dict:
    sigs = {
        "services": set(),
        "os_family": None,
    }

    if re.search(r"\b22/tcp\s+open", text):
        sigs["services"].add("ssh")

    if re.search(r"\b80/tcp\s+open", text):
        sigs["services"].add("http")

    if re.search(r"\b445/tcp\s+open", text):
        sigs["services"].add("smb")

    lower = text.lower()
    if "windows" in lower:
        sigs["os_family"] = "windows"
    elif "linux" in lower:
        sigs["os_family"] = "linux"

    return sigs

