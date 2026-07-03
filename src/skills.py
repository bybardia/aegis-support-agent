from pathlib import Path

# Maps a triage category to the agent skill that should guide the response.
SKILL_MAP = {
    "billing": "refund_verification",
    "security": "security_incident_response",
    "privacy": "security_incident_response",
}


def load_skill(category: str) -> str | None:
    """Return the SKILL.md guidance for a category, or None if no skill applies."""
    name = SKILL_MAP.get(category)
    if not name:
        return None
    path = Path("skills") / name / "SKILL.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return None


def list_skills() -> list[str]:
    """Return the names of all available agent skills."""
    root = Path("skills")
    if not root.exists():
        return []
    return sorted(p.name for p in root.iterdir() if (p / "SKILL.md").exists())