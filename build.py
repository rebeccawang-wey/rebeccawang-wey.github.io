"""Build the website from the files in content/ into _site/.

Usage:
    python build.py            # normal build (for GitHub Pages)
    python build.py --preview  # links end in index.html, for opening files directly

Needs: pip install -r requirements.txt
"""

import math
import re
import shutil
import sys
from datetime import date
from pathlib import Path

import markdown
import yaml
from jinja2 import ChainableUndefined, Environment, FileSystemLoader

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
OUT = ROOT / "_site"
PREVIEW = "--preview" in sys.argv

FIELDS = {
    "finance": "Finance",
    "economics": "Economics",
    "metrics": "Econometrics and Statistics",
    "risk": "Risk",
}
FILTER_ORDER = ["finance", "economics", "metrics", "risk"]
NAV = [
    ("Board", ""),
    ("Methods", "methods/"),
    ("Notes", "notes/"),
    ("About", "about/"),
    ("Contact", "contact/"),
]

warnings = []


def warn(msg):
    warnings.append(msg)


# ---------------------------------------------------------------- reading

def read_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def read_md(path):
    text = path.read_text(encoding="utf-8").lstrip("﻿")
    meta, body = {}, text
    if text.startswith("---"):
        parts = re.split(r"^---\s*$", text, maxsplit=2, flags=re.M)
        if len(parts) == 3:
            meta = yaml.safe_load(parts[1]) or {}
            body = parts[2]
    return meta, body.strip()


def md_to_html(text):
    html = markdown.markdown(
        text or "",
        extensions=["tables", "sane_lists", "smarty", "attr_list"],
        output_format="html",
    )
    return html.replace("<table>", '<div class="table-scroll"><table>').replace("</table>", "</table></div>")


def split_at_found(html):
    """Split a detail page body so the visual sits just before 'What I found'."""
    m = re.search(r"<h2[^>]*>\s*What I found", html)
    if not m:
        return html, ""
    return html[: m.start()], html[m.start():]


def is_blank(value):
    return value is None or str(value).strip() == ""


# ---------------------------------------------------------------- content

def load_questions():
    questions = []
    for path in sorted((CONTENT / "questions").glob("*.md")):
        meta, body = read_md(path)
        if meta.get("hidden"):
            continue
        slug = path.stem
        field = str(meta.get("field", "")).strip().lower()
        if field not in FIELDS:
            warn(f"{path.name}: field '{field}' should be one of {', '.join(FIELDS)}")
            field = "metrics"
        if is_blank(meta.get("question")):
            warn(f"{path.name}: has no question")
        before, after = split_at_found(md_to_html(body))
        figure = meta.get("figure") or {}
        files = []
        for item in meta.get("files") or []:
            href = item.get("url") or item.get("file")
            if is_blank(href):
                continue
            if not str(href).startswith(("http://", "https://")):
                href = str(href).lstrip("/")
                if not (CONTENT / href).exists():
                    warn(f"{path.name}: file '{href}' not found in content/")
                    continue
                href = {"local": href}
            files.append({"label": item.get("label") or "Download", "href": href})
        questions.append({
            "slug": slug,
            "question": meta.get("question", ""),
            "field": field,
            "field_name": FIELDS[field],
            "answer": meta.get("answer", ""),
            "method": meta.get("method", ""),
            "status": meta.get("status", ""),
            "date": meta.get("date", ""),
            "kind": meta.get("kind", ""),
            "tools": meta.get("tools", ""),
            "order": meta.get("order", 99),
            "related_slugs": meta.get("related") or [],
            "files": files,
            "figure": figure,
            "body_before": before,
            "body_after": after,
        })
    questions.sort(key=lambda q: (q["order"], q["slug"]))
    by_slug = {q["slug"]: q for q in questions}
    for q in questions:
        related = []
        for s in q["related_slugs"]:
            if s in by_slug and s != q["slug"]:
                related.append(by_slug[s])
            else:
                warn(f"{q['slug']}.md: related question '{s}' not found")
        if len(related) < 2:  # fill up to two from the same field, then any
            pool = [o for o in questions if o is not q and o not in related]
            pool.sort(key=lambda o: o["field"] != q["field"])
            related += pool[: 2 - len(related)]
        q["related"] = related[:2]
    if len(questions) > 6:
        warn(f"{len(questions)} cards on the board — the brief suggests keeping the first board to six")
    return questions


def load_notes():
    notes = []
    for path in sorted((CONTENT / "notes").glob("*.md")):
        meta, body = read_md(path)
        if meta.get("hidden"):
            continue
        d = meta.get("date")
        if isinstance(d, str):
            try:
                d = date.fromisoformat(d)
            except ValueError:
                warn(f"{path.name}: date should look like 2026-11-01")
                d = None
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
        words = len(re.findall(r"\w+", body))
        notes.append({
            "slug": slug,
            "title": meta.get("title", slug),
            "date": d,
            "date_text": f"{d.day} {d:%B %Y}" if d else "",
            "date_iso": d.isoformat() if d else "",
            "summary": meta.get("summary", ""),
            "minutes": max(1, math.ceil(words / 220)),
            "html": md_to_html(body),
        })
    notes.sort(key=lambda n: n["date"] or date.min, reverse=True)
    return notes


# ---------------------------------------------------------------- rendering

def main():
    site = read_yaml(CONTENT / "site.yml")
    questions = load_questions()
    notes = load_notes()
    next_qs = read_yaml(CONTENT / "next.yml") or []
    for n in next_qs:
        n["field"] = str(n.get("field", "")).lower()
        n["field_name"] = FIELDS.get(n["field"], "")
    methods = read_yaml(CONTENT / "methods.yml")
    experience = read_yaml(CONTENT / "experience.yml") or []
    q_by_slug = {q["slug"]: q for q in questions}
    for group in methods.get("groups", []):
        for item in group.get("items", []):
            s = item.get("used_in")
            item["question"] = q_by_slug.get(s) if s else None
            if s and not item["question"]:
                warn(f"methods.yml: '{item.get('name')}' uses question '{s}', which was not found")

    resume = site.get("about", {}).get("resume_file")
    resume_exists = bool(resume) and (CONTENT / resume).exists()

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    if (CONTENT / "files").exists():
        shutil.copytree(CONTENT / "files", OUT / "files")

    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        autoescape=True,
        undefined=ChainableUndefined,  # a missing value shows as blank instead of breaking the build
        trim_blocks=True,
        lstrip_blocks=True,
    )

    def render(template, out_path, absolute=False, **ctx):
        depth = out_path.count("/")
        root = "../" * depth
        if absolute:  # the 404 page can be shown at any address, so it needs absolute links
            root = "/" + str(site.get("base_path") or "").strip("/") + "/"
            root = root.replace("//", "/")

        def url(path=""):
            if isinstance(path, dict):  # a local file
                return root + path["local"]
            if path.startswith(("http://", "https://", "mailto:", "#")):
                return path
            path = path.lstrip("/")  # "/files/x.png" and "files/x.png" mean the same file
            if path.endswith("/") or path == "":
                return root + path + ("index.html" if PREVIEW else ("" if path else "./"))
            return root + path

        html = env.get_template(template).render(
            site=site, nav=NAV, url=url, year=date.today().year,
            fields=FIELDS, filter_order=FILTER_ORDER, **ctx,
        )
        target = OUT / out_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")

    render("board.html", "index.html", page="", questions=questions, next_qs=next_qs[:3])
    for q in questions:
        render("question.html", f"questions/{q['slug']}/index.html", page="", q=q)
    render("methods.html", "methods/index.html", page="methods/", methods=methods)
    render("notes.html", "notes/index.html", page="notes/", notes=notes)
    for n in notes:
        render("note.html", f"notes/{n['slug']}/index.html", page="notes/", n=n)
    render("about.html", "about/index.html", page="about/", experience=experience,
           next_qs=next_qs, resume_exists=resume_exists)
    render("contact.html", "contact/index.html", page="contact/")
    render("404.html", "404.html", absolute=not PREVIEW, page="")

    pages = len(list(OUT.rglob("*.html")))
    print(f"Built {pages} pages into {OUT.name}/ ({'preview' if PREVIEW else 'normal'} links)")
    if warnings:
        print("\nThings to check:")
        for w in warnings:
            print("  -", w)


if __name__ == "__main__":
    main()
