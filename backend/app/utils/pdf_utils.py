from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import os


def generate_searchable_pdf(text: str, output_dir: str, base_name: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{base_name}.pdf")
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    x = 2 * cm
    y = height - 2 * cm
    for line in text.split("\n"):
        c.drawString(x, y, line[:1000])
        y -= 14
        if y < 2 * cm:
            c.showPage()
            y = height - 2 * cm
    c.save()
    return path

