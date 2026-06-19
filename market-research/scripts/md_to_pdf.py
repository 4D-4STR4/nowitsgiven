#!/usr/bin/env python3
"""Convert the ONDS research markdown into phone-friendly PDFs.

Usage:
    pip install markdown weasyprint
    python3 market-research/scripts/md_to_pdf.py

Produces individual PDFs plus one combined PDF in market-research/ONDS/pdf/.
"""
import pathlib
import markdown
from weasyprint import HTML

ROOT = pathlib.Path(__file__).resolve().parents[1] / "ONDS"
OUT = ROOT / "pdf"
OUT.mkdir(exist_ok=True)

# Reading order: cheat-sheet, master dossier, then the 7 sections.
FILES = [
    ("STUDY-GUIDE.md", "ONDS — Study Cheat-Sheet"),
    ("DOSSIER.md", "ONDS — Master Dossier"),
    ("sections/01-financials-sec.md", "1. Financials & SEC Filings"),
    ("sections/02-business-and-technology.md", "2. Business & Technology"),
    ("sections/03-tam-market-sizing.md", "3. TAM & Market Sizing"),
    ("sections/04-competition.md", "4. Competitive Landscape"),
    ("sections/05-execution-management.md", "5. Execution & Management"),
    ("sections/06-catalysts-ma-contracts.md", "6. Catalysts, M&A & Events"),
    ("sections/07-industry-regulatory-macro.md", "7. Industry, Regulatory & Macro"),
]

# Mobile-friendly CSS: generous line-height, wrapping tables, readable sizes.
CSS = """
@page { size: A4; margin: 1.4cm 1.2cm; }
* { -weasy-hyphens: auto; }
body {
  font-family: 'DejaVu Sans', 'Noto Color Emoji', sans-serif;
  font-size: 12.5px; line-height: 1.5; color: #1a1a1a;
}
h1 { font-size: 22px; color: #0b3d5c; border-bottom: 3px solid #0b3d5c;
     padding-bottom: 6px; margin-top: 0; }
h2 { font-size: 18px; color: #0b3d5c; margin-top: 1.2em;
     border-bottom: 1px solid #cdd9e0; padding-bottom: 3px; }
h3 { font-size: 15px; color: #114b6b; margin-top: 1em; }
h4 { font-size: 13.5px; color: #333; }
a { color: #1565c0; text-decoration: none; word-break: break-all; }
code { background: #f2f4f6; padding: 1px 4px; border-radius: 3px;
       font-family: 'DejaVu Sans Mono', monospace; font-size: 0.85em; }
pre { background: #f2f4f6; padding: 8px; border-radius: 5px;
      white-space: pre-wrap; word-break: break-word; font-size: 0.82em; }
blockquote { border-left: 4px solid #f0a500; background: #fff8e6;
             margin: 0.8em 0; padding: 6px 12px; }
table { width: 100%; border-collapse: collapse; margin: 0.8em 0;
        font-size: 10.2px; table-layout: fixed; }
th, td { border: 1px solid #cdd9e0; padding: 4px 6px; text-align: left;
         vertical-align: top; word-break: break-word; overflow-wrap: anywhere; }
th { background: #0b3d5c; color: #fff; }
tr:nth-child(even) td { background: #f6f9fb; }
hr { border: none; border-top: 1px solid #cdd9e0; margin: 1.2em 0; }
ul, ol { padding-left: 1.3em; }
.cover { page-break-after: always; text-align: center; padding-top: 30%; }
.cover h1 { border: none; font-size: 30px; }
.cover p { color: #555; }
.section { page-break-before: always; }
"""

EXTS = ["tables", "fenced_code", "sane_lists", "attr_list", "nl2br"]


def md_to_html_body(path: pathlib.Path) -> str:
    text = path.read_text(encoding="utf-8")
    return markdown.markdown(text, extensions=EXTS)


def wrap(body: str) -> str:
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"


def build_individual():
    for rel, title in FILES:
        src = ROOT / rel
        if not src.exists():
            print(f"  skip (missing): {rel}")
            continue
        html = wrap(md_to_html_body(src))
        out = OUT / (pathlib.Path(rel).stem + ".pdf")
        HTML(string=html, base_url=str(src.parent)).write_pdf(str(out))
        print(f"  wrote {out.name}")


def build_combined():
    cover = (
        "<div class='cover'><h1>🛰️ ONDS</h1>"
        "<h2 style='border:none'>Ondas Inc. — Full Research Dossier</h2>"
        "<p>NASDAQ: ONDS &middot; snapshot 2026-06-19</p>"
        "<p><em>Informational research only — not financial advice.</em></p></div>"
    )
    parts = [cover]
    for rel, _title in FILES:
        src = ROOT / rel
        if not src.exists():
            continue
        parts.append(f"<div class='section'>{md_to_html_body(src)}</div>")
    html = wrap("".join(parts))
    out = OUT / "ONDS-Full-Dossier.pdf"
    HTML(string=html, base_url=str(ROOT)).write_pdf(str(out))
    print(f"  wrote {out.name}")


if __name__ == "__main__":
    print("Building individual PDFs:")
    build_individual()
    print("Building combined PDF:")
    build_combined()
    print(f"Done → {OUT}")
