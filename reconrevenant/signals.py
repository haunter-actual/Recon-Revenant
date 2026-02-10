from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Signals:
    os_family: Optional[str] = None  # linux | windows

    services: List[str] = field(default_factory=list)

    filesystem_issues: List[str] = field(default_factory=list)
    credential_artifacts: List[str] = field(default_factory=list)

    privilege_vectors: List[str] = field(default_factory=list)
    token_capabilities: List[str] = field(default_factory=list)
    service_misconfigs: List[str] = field(default_factory=list)

    kernel_age: Optional[str] = None
    domain_context: Optional[str] = None

    confidence_notes: Dict[str, str] = field(default_factory=dict)

