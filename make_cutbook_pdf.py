#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
make_cutbook_pdf.py

Generate a printable "cut-book" PDF:
- Each phrase is 3 lines (A / B / C)
- Can place 1, 2 or 4 phrases per page
- Big font, centered
- Optional cut guides:
    - internal: 2 horizontal lines at exactly 1/3 and 2/3 of each phrase block
    - box: frame around each block
    - all: internal + box
- Windows-first Cyrillic font auto-detection (C:\\Windows\\Fonts)
"""

import argparse
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Optional

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, LETTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# -------------------- Data --------------------

@dataclass
class Phrase:
    a: str
    b: str
    c: str

    def lines(self) -> List[str]:
        return [self.a, self.b, self.c]


# -------------------- Fonts (Windows-first) --------------------

def _win_fonts_dir() -> Optional[Path]:
    windir = os.environ.get("WINDIR") or os.environ.get("SystemRoot")
    if not windir:
        return None
    p = Path(windir) / "Fonts"
    return p if p.exists() else None


def try_register_font(font_name: str, font_file: Optional[str]) -> str:
    """
    Register a TTF font to support Cyrillic.
    Windows-first: tries C:\\Windows\\Fonts\\ (Arial/Calibri/Times/Verdana/Tahoma).
    Returns font name for canvas.setFont().
    """
    if font_file:
        ff = Path(font_file)
        if not ff.is_file():
            raise FileNotFoundError(f"Font file not found: {font_file}")
        pdfmetrics.registerFont(TTFont(font_name, str(ff)))
        return font_name

    win_dir = _win_fonts_dir()
    if win_dir:
        candidates = [
            win_dir / "arial.ttf",
            win_dir / "calibri.ttf",
            win_dir / "times.ttf",
            win_dir / "verdana.ttf",
            win_dir / "tahoma.ttf",
        ]
        for p in candidates:
            if p.is_file():
                pdfmetrics.registerFont(TTFont(font_name, str(p)))
                return font_name

    # Non-Windows fallback (optional)
    candidates = [
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/TTF/DejaVuSans.ttf"),
        Path("/usr/local/share/fonts/DejaVuSans.ttf"),
    ]
    for p in candidates:
        if p.is_file():
            pdfmetrics.registerFont(TTFont(font_name, str(p)))
            return font_name

    # Fallback (may not render Cyrillic)
    return "Helvetica"


# -------------------- Input parsing --------------------

def split_delimited(line: str) -> Optional[Tuple[str, str, str]]:
    for delim in [" / ", " | ", " ; ", "/", "|", ";"]:
        if delim in line:
            parts = [p.strip() for p in line.split(delim) if p.strip() != ""]
            if len(parts) == 3:
                return parts[0], parts[1], parts[2]
    return None


def parse_phrases(path: str, encoding: str) -> List[Phrase]:
    """
    Supported formats:
      A) one line: "A / B / C" (also | or ;)
      B) blocks of 3 lines, phrases separated by blank line
    Lines starting with # are ignored.
    """
    with open(path, "r", encoding=encoding) as f:
        raw_lines = [ln.rstrip("\n") for ln in f]

    phrases: List[Phrase] = []
    block: List[str] = []

    def flush_block():
        nonlocal block, phrases
        blk = [x.strip() for x in block if x.strip() != ""]
        if not blk:
            block = []
            return
        if len(blk) != 3:
            raise ValueError(f"Expected 3 lines in block phrase, got {len(blk)}: {blk}")
        phrases.append(Phrase(blk[0], blk[1], blk[2]))
        block = []

    for ln in raw_lines:
        s = ln.strip()
        if not s:
            flush_block()
            continue
        if s.startswith("#"):
            continue

        one = split_delimited(s)
        if one and not block:
            phrases.append(Phrase(*one))
            continue

        block.append(s)
        if len([x for x in block if x.strip()]) == 3:
            flush_block()

    flush_block()

    if not phrases:
        raise ValueError("No phrases found. Check input format.")
    return phrases


# -------------------- Layout helpers --------------------

def fit_font_size_line(
    font_name: str,
    text: str,
    max_size: int,
    min_size: int,
    max_w: float,
    max_h: float
) -> int:
    """
    Fit a single line into a rectangular box (max_w x max_h).
    """
    size = max_size
    while size >= min_size:
        line_w = pdfmetrics.stringWidth(text, font_name, size)
        if line_w <= max_w and size <= max_h:
            return size
        size -= 1
    return min_size


def make_slots(
    page_w: float,
    page_h: float,
    margin: float,
    phrases_per_page: int,
    gutter: float
) -> List[Tuple[float, float, float, float]]:
    """
    Returns list of slots as (x, y, w, h) in PDF coords (bottom-left origin).
    """
    usable_w = page_w - 2 * margin
    usable_h = page_h - 2 * margin
    if usable_w <= 0 or usable_h <= 0:
        raise ValueError("Margins too large for the selected page size.")

    slots: List[Tuple[float, float, float, float]] = []

    if phrases_per_page == 1:
        slots.append((margin, margin, usable_w, usable_h))

    elif phrases_per_page == 2:
        slot_h = (usable_h - gutter) / 2.0
        if slot_h <= 0:
            raise ValueError("Gutter too large.")
        # top then bottom
        slots.append((margin, margin + slot_h + gutter, usable_w, slot_h))
        slots.append((margin, margin, usable_w, slot_h))

    elif phrases_per_page == 4:
        slot_w = (usable_w - gutter) / 2.0
        slot_h = (usable_h - gutter) / 2.0
        if slot_w <= 0 or slot_h <= 0:
            raise ValueError("Gutter too large.")
        left_x = margin
        right_x = margin + slot_w + gutter
        bottom_y = margin
        top_y = margin + slot_h + gutter
        slots.extend([
            (left_x,  top_y,    slot_w, slot_h),
            (right_x, top_y,    slot_w, slot_h),
            (left_x,  bottom_y, slot_w, slot_h),
            (right_x, bottom_y, slot_w, slot_h),
        ])

    else:
        raise ValueError("phrases_per_page must be 1, 2, or 4")

    return slots


def draw_guides(c: canvas.Canvas, mode: str, x: float, y: float, w: float, h: float):
    """
    mode: none|internal|box|all
    Internal guides are EXACTLY at 1/3 and 2/3 of the phrase box height,
    so strips are always equal height.
    """
    if mode == "none":
        return

    c.saveState()
    c.setLineWidth(0.5)
    c.setStrokeGray(0.75)

    if mode in ("box", "all"):
        c.rect(x, y, w, h, stroke=1, fill=0)

    if mode in ("internal", "all"):
        y_top_cut = y + h * (2.0 / 3.0)
        y_bot_cut = y + h * (1.0 / 3.0)
        c.line(x, y_top_cut, x + w, y_top_cut)
        c.line(x, y_bot_cut, x + w, y_bot_cut)

    c.restoreState()


# -------------------- Text drawing --------------------

def draw_centered_scaled(
    c: canvas.Canvas,
    text: str,
    cx: float,
    cy: float,
    font_name: str,
    font_size: int,
    max_width: float
):
    line_w = pdfmetrics.stringWidth(text, font_name, font_size)
    if line_w <= max_width:
        c.drawCentredString(cx, cy, text)
        return

    scale_x = max_width / max(1.0, line_w)
    c.saveState()
    c.translate(cx, cy)
    c.scale(scale_x, 1.0)
    c.drawCentredString(0, 0, text)
    c.restoreState()


# -------------------- PDF rendering --------------------

def render_pdf(
    phrases: List[Phrase],
    out_pdf: str,
    *,
    pagesize_name: str,
    font_name: str,
    max_font: int,
    min_font: int,
    margin: float,
    padding: float,
    leading_mult: float,
    extra_gap: float,
    phrases_per_page: int,
    gutter: float,
    cut_guides: str,
    case_mode: str
):
    pagesize = A4 if pagesize_name.upper() == "A4" else LETTER
    page_w, page_h = pagesize

    c = canvas.Canvas(out_pdf, pagesize=pagesize)
    slots = make_slots(page_w, page_h, margin, phrases_per_page, gutter)

    idx = 0
    total = len(phrases)

    while idx < total:
        for (x, y, w, h) in slots:
            if idx >= total:
                break

            ph = phrases[idx]
            lines = [apply_case(line, case_mode) for line in ph.lines()]

            inner_x = x + padding
            inner_y = y + padding
            inner_w = max(1.0, w - 2 * padding)
            inner_h = max(1.0, h - 2 * padding)
            third_h = inner_h / 3.0

            cx = inner_x + inner_w / 2.0
            y_top = inner_y + inner_h - third_h / 2.0
            y_mid = inner_y + inner_h / 2.0
            y_bot = inner_y + third_h / 2.0

            # Fit each line independently to its third.
            sizes = [
                fit_font_size_line(font_name, lines[0], max_font, min_font, inner_w, third_h),
                fit_font_size_line(font_name, lines[1], max_font, min_font, inner_w, third_h),
                fit_font_size_line(font_name, lines[2], max_font, min_font, inner_w, third_h),
            ]

            for text, size, cy in [(lines[0], sizes[0], y_top),
                                   (lines[1], sizes[1], y_mid),
                                   (lines[2], sizes[2], y_bot)]:
                c.setFont(font_name, size)
                draw_centered_scaled(c, text, cx, cy, font_name, size, inner_w)

            # Cut guides (equal strip height: 1/3 and 2/3 of block)
            draw_guides(c, cut_guides, x, y, w, h)

            idx += 1

        c.showPage()

    c.save()


# -------------------- CLI --------------------

def apply_case(text: str, mode: str) -> str:
    if mode == "upper":
        return text.upper()
    if mode == "lower":
        return text.lower()
    if mode == "sentence":
        return text[:1].upper() + text[1:].lower() if text else text
    return text


def main():
    ap = argparse.ArgumentParser(
        description="Generate cut-phrases PDF: 3 lines per phrase, big font, equal-height cut strips, Windows-friendly."
    )
    ap.add_argument("--input", help="Input text file with phrases",default="phrases.txt")
    ap.add_argument("--output", help="Output PDF path", default="cutbook.pdf")

    ap.add_argument("--encoding", default="utf-8-sig",
                    help="Input file encoding (default: utf-8-sig). Use cp1251 if needed.")
    ap.add_argument("--pagesize", choices=["A4", "LETTER"], default="A4")

    ap.add_argument("--font-file", default=None,
                    help="Path to TTF font file (optional). If omitted, tries Windows fonts in C:\\Windows\\Fonts.")
    ap.add_argument("--font-name", default="CutBookFont",
                    help="Internal font name (used when registering a TTF).")

    ap.add_argument("--max-font", type=int, default=110, help="Max font size (pt)")
    ap.add_argument("--min-font", type=int, default=26, help="Min font size (pt)")

    ap.add_argument("--margin", type=float, default=48, help="Outer page margin (pt)")
    ap.add_argument("--padding", type=float, default=18, help="Inner padding inside each phrase box (pt)")

    # Bigger vertical spacing by default (for easier cutting/leafing)
    ap.add_argument("--leading-mult", type=float, default=2.15,
                    help="Line spacing multiplier (leading = font_size*leading_mult + extra_gap)")
    ap.add_argument("--extra-gap", type=float, default=10.0,
                    help="Extra points added to leading (default: 10pt)")

    ap.add_argument("--phrases-per-page", type=int, choices=[1, 2, 4], default=1,
                    help="How many phrases per page (1, 2, or 4)")
    ap.add_argument("--gutter", type=float, default=18.0,
                    help="Gap between phrase boxes when phrases-per-page > 1 (pt)")

    ap.add_argument("--cut-guides", choices=["none", "internal", "box", "all"], default="internal",
                    help="Cut guides: none | internal (1/3 & 2/3) | box (frame) | all")
    ap.add_argument("--case", dest="case_mode",
                    choices=["none", "upper", "lower", "sentence"], default="none",
                    help="Text case: none | upper | lower | sentence")

    args = ap.parse_args()

    phrases = parse_phrases(args.input, args.encoding)
    font_to_use = try_register_font(args.font_name, args.font_file)

    render_pdf(
        phrases=phrases,
        out_pdf=args.output,
        pagesize_name=args.pagesize,
        font_name=font_to_use,
        max_font=args.max_font,
        min_font=args.min_font,
        margin=args.margin,
        padding=args.padding,
        leading_mult=args.leading_mult,
        extra_gap=args.extra_gap,
        phrases_per_page=args.phrases_per_page,
        gutter=args.gutter,
        cut_guides=args.cut_guides,
        case_mode=args.case_mode,
    )

    print(f"OK: {len(phrases)} phrases -> {args.output}")
    if font_to_use == "Helvetica":
        print("WARNING: Helvetica may not render Cyrillic. Use --font-file, e.g.:")
        print(r'  --font-file "C:\Windows\Fonts\arial.ttf"')


if __name__ == "__main__":
    main()
