import re


FORBIDDEN_PATTERNS = [
    r"/", r"\\", r":", r"@",          # paths / usernames
    r"\b\d{1,3}(\.\d{1,3}){3}\b",     # IP addresses
    r"\.com\b|\.(local|lan)\b",        # domains
]


def prompt_is_safe(text: str) -> bool:
    return not any(re.search(p, text, re.I) for p in FORBIDDEN_PATTERNS)


UNSAFE_OUTPUT_PATTERNS = [
    r"\bexploit\b",
    r"\bpayload\b",
    r"\bcurl\b|\bwget\b",
    r"```",  # code blocks
]


def output_is_safe(text: str) -> bool:
    return not any(re.search(p, text, re.I) for p in UNSAFE_OUTPUT_PATTERNS)

