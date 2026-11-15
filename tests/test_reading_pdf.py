from fpdf import FPDF
from app.services.extraction_service import extract_text_from_pdf


def make_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 6, text)
    return bytes(pdf.output())


def test_extract_text_from_real_pdf_bytes():
    pdf_bytes = make_pdf("Total Premium: $2,050.00")
    assert "Total Premium: $2,050.00" in extract_text_from_pdf(pdf_bytes)