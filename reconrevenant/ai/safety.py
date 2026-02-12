import re

# Only block clearly dangerous output content
UNSAFE_OUTPUT_PATTERNS = [
    r"\bexploit\b",
    r"\bpayload\b",
    r"\bcurl\b|\bwget\b",
    r"```",  # code blocks
]


def prompt_is_safe(text: str) -> bool:
    """
    Prompt is safe as long as it does NOT contain:
    - raw file paths
    - IP addresses
    - email addresses
    - domain names
    """
    forbidden = [
        r"\b\d{1,3}(\.\d{1,3}){3}\b",   # IPv4
        r"@[a-zA-Z0-9.-]+",              # email
        r"\b[a-zA-Z0-9.-]+\.(com|net|org|local|lan)\b",  # domains
        r"/[a-zA-Z0-9_/.-]+",            # unix paths
        r"[A-Za-z]:\\",                  # windows paths
    ]

    return not any(re.search(p, text) for p in forbidden)


def output_is_safe(text: str) -> bool:
    """Reject exploit/payload/command-style AI output."""
    return not any(re.search(p, text, re.I) for p in UNSAFE_OUTPUT_PATTERNS)

