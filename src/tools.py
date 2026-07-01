from pathlib import Path


POLICY_MAP = {
    "billing": "billing.md",
    "security": "security.md",
    "privacy": "privacy.md",
    "account_access": "account_access.md",
    "technical_bug": "technical_bug.md",
    "feature_request": "feature_request.md",
    "general": "general.md",
}


def policy_lookup(category: str) -> str:
    """Return the policy text for a support category."""
    filename = POLICY_MAP.get(category, "general.md")
    path = Path("policies") / filename

    if not path.exists():
        fallback = Path("policies") / "general.md"
        if fallback.exists():
            return fallback.read_text(encoding="utf-8")
        return "No policy found. Use general support best practices."

    return path.read_text(encoding="utf-8")


def list_available_policies() -> list[str]:
    """Return the available support policy categories."""
    return sorted(POLICY_MAP.keys())
