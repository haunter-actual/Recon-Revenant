from reconrevenant.parser_nmap import parse_nmap
from reconrevenant.parser_enum import parse_enum
from reconrevenant.signals_builder import build_signals

def test_linux_flow():
    nmap = "22/tcp open ssh\n80/tcp open http\nLinux"
    enum = "Writable folder: /var/www/html\nSUID binary: /usr/bin/env\nLinux Kernel 4.15"

    signals = build_signals(parse_nmap(nmap), parse_enum(enum))

    assert signals.os_family == "linux"
    assert "http" in signals.services
    assert "web_writable_dir" in signals.filesystem_issues

