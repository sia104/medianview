from pathlib import Path


def test_adlc_scaffold_exists() -> None:
    root = Path(__file__).resolve().parents[1]

    assert (root / "AGENTS.md").is_file()
    assert (root / ".codex" / "skills" / "spec-it" / "SKILL.md").is_file()
    assert (root / ".codex" / "skills" / "implement-it" / "SKILL.md").is_file()
    assert (root / "specs").is_dir()
