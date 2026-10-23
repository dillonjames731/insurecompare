from fpdf import FPDF


def write_pdf(path, lines):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 6, "\n".join(lines))
    pdf.output(path)


CURRENT_DEC_PAGE = [
    "EVERGREEN MUTUAL INSURANCE COMPANY",
    "Auto Policy Declarations",
    "",
    "Named Insured: Jordan Sample",
    "Policy Number: EM-000-1234",
    "Policy Period: 01/15/2026 to 07/15/2026",
    "Policy Term: 6 Months",
    "",
    "Vehicle 1: 2019 Example Sedan",
    "",
    "COVERAGE    LIMITS    DEDUCTIBLE    PREMIUM",
    "Bodily Injury Liability    $50,000 each person / $100,000 each accident    $318.00",
    "Property Damage Liability    $50,000 each accident    $142.00",
    "Uninsured Motorist Bodily Injury    $50,000 each person / $100,000 each accident    $64.00",
    "Personal Injury Protection    $10,000 each person    $55.00",
    "Medical Payments    $5,000 each person    $22.00",
    "Collision    Actual Cash Value    $500    $356.00",
    "Comprehensive    Actual Cash Value    $250    $98.00",
    "Rental Reimbursement    $30 per day / $900 maximum    $18.00",
    "",
    "TOTAL $1,073.00",
]

write_pdf("samples/evergreen_current_dec.pdf", CURRENT_DEC_PAGE)

NEW_QUOTE = [
    "SUMMIT AUTO INSURANCE",
    "Auto Insurance Quote",
    "",
    "Quote Prepared For: Jordan Sample",
    "Proposed Policy Period: 01/15/2026 to 01/15/2027",
    "Term: 12 Months",
    "Bodily Injury: $100,000 each person / $300,000 each accident",
    "Property Damage: $100,000 each accident",
    "Uninsured/Underinsured Motorist Bodily Injury: $100,000 each person / $300,000 each accident",
    "Uninsured/Underinsured Motorist Property Damage: $100,000",
    "PIP: $10,000 each person",
    "Medical Payments: $5,000 each person",
    "Comprehensive Deductible: $500",
    "Collision Deductible: $1,000",
    "Towing and Roadside: Included",
    "Total Premium: $2,050.00"









]

write_pdf("samples/summit_quote.pdf", NEW_QUOTE)