---
name: pdf
description: Generate blog-style PDF documents with tables and charts on a given topic
user_invocable: true
arguments: topic or description of the PDF to generate
---

# PDF Builder Skill

Generate a blog-style PDF document on the requested topic. The PDF should be informative, visually appealing, and include tables and charts where appropriate.

## Dependencies

- `fpdf2` for PDF generation
- `matplotlib` for charts (already installed)
- `numpy` / `pandas` for data (already installed)

Install if missing: `pip3 install fpdf2`

## Output Location

Save generated PDFs to: `pdfs/` directory in the project root. Create the directory if it doesn't exist.

Name the file based on the topic using snake_case (e.g., `pdfs/machine_learning_basics.pdf`).

## PDF Structure

Every PDF must follow this structure:

1. **Title page** — large title, subtitle with date, and a short abstract/summary
2. **Introduction** — 2-3 paragraphs introducing the topic
3. **Body sections** — 2-4 sections with:
   - Section headings
   - Explanatory paragraphs
   - At least one **table** with relevant data
   - At least one **chart** (bar, line, pie, or scatter) visualizing data
4. **Conclusion** — key takeaways as a summary

## Styling Guidelines

- **Page size:** A4
- **Title:** 24pt, bold, dark blue (`#1a3c6e`)
- **Section headings:** 16pt, bold, dark blue
- **Body text:** 11pt, black, with 1.5 line spacing
- **Tables:** alternating row colors (white and light gray `#f0f0f0`), header row in dark blue with white text
- **Margins:** 20mm all sides
- **Footer:** page number centered on every page

## Code Pattern

Use this pattern for generating the PDF:

```python
import os
import tempfile
from datetime import date
from fpdf import FPDF
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

class BlogPDF(FPDF):
    """Custom PDF class with header/footer."""

    def __init__(self, title: str):
        super().__init__()
        self.doc_title = title
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, self.doc_title, align="C")
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def add_title_page(self, title: str, subtitle: str, abstract: str):
        self.add_page()
        self.ln(60)
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(26, 60, 110)
        self.multi_cell(0, 12, title, align="C")
        self.ln(8)
        self.set_font("Helvetica", "", 14)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, subtitle, align="C")
        self.ln(20)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 6, abstract, align="C")

    def add_section(self, heading: str):
        self.ln(8)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(26, 60, 110)
        self.cell(0, 10, heading)
        self.ln(10)

    def add_paragraph(self, text: str):
        self.set_font("Helvetica", "", 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 7, text)
        self.ln(4)

    def add_table(self, headers: list[str], rows: list[list[str]]):
        col_width = (self.w - 40) / len(headers)
        # Header row
        self.set_font("Helvetica", "B", 10)
        self.set_fill_color(26, 60, 110)
        self.set_text_color(255, 255, 255)
        for h in headers:
            self.cell(col_width, 8, h, border=1, fill=True, align="C")
        self.ln()
        # Data rows
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0, 0, 0)
        for i, row in enumerate(rows):
            if i % 2 == 0:
                self.set_fill_color(240, 240, 240)
            else:
                self.set_fill_color(255, 255, 255)
            for val in row:
                self.cell(col_width, 8, str(val), border=1, fill=True, align="C")
            self.ln()
        self.ln(6)

    def add_chart(self, chart_path: str, width: int = 160):
        self.image(chart_path, x=(self.w - width) / 2, w=width)
        self.ln(8)


def create_chart(fig, ax, filepath: str):
    """Save a matplotlib chart to a temp file for embedding."""
    fig.tight_layout()
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
```

## Important Rules

- Always use `matplotlib.use("Agg")` before importing pyplot (no GUI backend)
- Save chart images to a temp directory, embed them, then clean up
- Use `tempfile.mkdtemp()` for temporary chart images
- All data in tables and charts should be realistic and relevant to the topic
- Write the PDF using `pdf.output(output_path)`
- Print the full output path when done so the user can find the file
- Use `python3` to run the script (never `python`)
