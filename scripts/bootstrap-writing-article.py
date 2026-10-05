#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")


class BootstrapError(RuntimeError):
    pass


def bootstrap_article(root: Path, article_id: str, title: str = "Provisional Title") -> Path:
    if not ARTICLE_ID_RE.fullmatch(article_id) or article_id in {".", ".."}:
        raise BootstrapError("article-id must be a safe non-empty slug")
    article_dir = root / "articles" / article_id
    article_path = article_dir / "index.md"
    if article_path.exists():
        raise BootstrapError(f"article already exists: {article_id}")
    article_dir.mkdir(parents=True, exist_ok=False)
    article_path.write_text(f"# {title.strip() or 'Provisional Title'}\n\n", encoding="utf-8")
    return article_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(ROOT))
    parser.add_argument("--article-id", required=True)
    parser.add_argument("--title", default="Provisional Title")
    args = parser.parse_args()
    try:
        path = bootstrap_article(Path(args.root).resolve(), args.article_id, args.title)
    except BootstrapError as exc:
        print(f"WRITING_BOOTSTRAP_FAIL {exc}")
        return 1
    print(args.article_id)
    print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
