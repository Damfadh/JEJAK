import datetime
import os
from typing import List, Optional

ROOT = os.path.dirname(os.path.abspath(__file__))
PROGRESS_LOG = os.path.join(ROOT, "progress_log.md")
ISSUES_FILE = os.path.join(ROOT, "issues.md")


def _today():
    return datetime.datetime.utcnow().strftime("%Y-%m-%d")


def append_progress_entry(author: str, title: str, status: str, description: str = "", files_changed: Optional[List[str]] = None, next_steps: str = "", notes: str = "") -> str:
    """Append a progress entry to progress_log.md and return the entry string."""
    date = _today()
    files_changed = files_changed or []
    header = f"{date} | @{author} | {title} | status: {status}\n"
    details = []
    if description:
        details.append(f"- Deskripsi: {description}")
    if files_changed:
        details.append(f"- Files changed: {', '.join(files_changed)}")
    if next_steps:
        details.append(f"- Next steps: {next_steps}")
    if notes:
        details.append(f"- Notes: {notes}")

    entry = header + "\n" + "\n".join(details) + "\n\n"

    with open(PROGRESS_LOG, "a", encoding="utf-8") as f:
        f.write(entry)

    return entry


def append_issue_entry(issue_id: str, reporter: str, title: str, status: str, priority: str, description: str, steps: str = "", assigned: str = "", solution: str = "", comments: str = "") -> str:
    """Append an issue entry to issues.md and return the entry string."""
    date = _today()
    lines = [f"ID: {issue_id}", f"Tanggal: {date}", f"Pelapor: @{reporter}", f"Judul: {title}", f"Status: {status}", f"Prioritas: {priority}", f"Deskripsi: {description}"]
    if steps:
        lines.append(f"Langkah reproduksi: {steps}")
    if assigned:
        lines.append(f"Assigned: @{assigned}")
    if solution:
        lines.append(f"Solusi: {solution}")
    if comments:
        lines.append(f"Komentar: {comments}")

    entry = "\n".join(lines) + "\n\n"

    with open(ISSUES_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

    return entry


if __name__ == "__main__":
    # quick manual test / usage example
    print("Log helper ready. Use append_progress_entry() or append_issue_entry().")
