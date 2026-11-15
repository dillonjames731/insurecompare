import pdfplumber
import io


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    pages_text = []

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text(x_tolerance=1) or ""
            pages_text.append(text)
    return "\n".join(pages_text).strip()
