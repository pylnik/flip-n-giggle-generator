# Cut-Book PDF Generator

A standalone Python script that builds printable cut-book PDFs. Each phrase is split into three strips (A / B / C) so you can cut and flip them independently.

## Features

- 1, 2, or 4 phrases per page
- Big, centered text with per-line sizing
- Optional cut guides (internal, box, or both)
- Case control: normal, upper, lower, sentence
- Windows-friendly font auto-detection (C:\\Windows\\Fonts)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Prepare a text file with phrases in one of these formats:

- One phrase per line, delimited: `A / B / C` (also `|` or `;`)
- Blocks of 3 lines separated by a blank line

Then run:

```bash
python make_cutbook_pdf.py --input phrases.txt --output output.pdf
```

Common options:

```bash
python make_cutbook_pdf.py --input .\phrases\phrases_en.txt --output output_de.pdf --case upper --max-font 30 --phrases-per-page 4 --cut-guides all
```
Example page: ![alt text](images\image_4phrases.png)

Change text case:

```bash
python make_cutbook_pdf.py --input phrases.txt --output output.pdf --case upper
```

If Cyrillic does not render, specify a font file:

```bash
python make_cutbook_pdf.py --input phrases.txt --output output.pdf --font-file "C:\\Windows\\Fonts\\arial.ttf"
```

## Arguments

- `--input` Input text file with phrases (default: `phrases.txt`)
- `--output` Output PDF path (default: `cutbook.pdf`)
- `--encoding` Input file encoding (default: `utf-8-sig`)
- `--pagesize` Page size: `A4` or `LETTER` (default: `A4`)
- `--font-file` Path to a TTF font file (optional)
- `--font-name` Internal font name when registering a TTF (default: `CutBookFont`)
- `--max-font` Max font size in points (default: `110`)
- `--min-font` Min font size in points (default: `26`)
- `--margin` Outer page margin in points (default: `48`)
- `--padding` Inner padding inside each phrase box in points (default: `18`)
- `--leading-mult` Line spacing multiplier (default: `2.15`)
- `--extra-gap` Extra points added to line spacing (default: `10.0`)
- `--phrases-per-page` Phrases per page: `1`, `2`, or `4` (default: `1`)
- `--gutter` Gap between phrase boxes in points (default: `18.0`)
- `--cut-guides` Guide lines: `none`, `internal`, `box`, `all` (default: `internal`)
- `--case` Text case: `none`, `upper`, `lower`, `sentence` (default: `none`)

## Example Phrase Files

The `phrases/` folder contains sample input files in `A / B / C` format:

- `phrases/phrases_en.txt`
- `phrases/phrases_ru.txt`
- `phrases/phrases_de.txt`

## Requirements

- Python 3.8 or higher
- reportlab
