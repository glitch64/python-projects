import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

def create_overlay(dob, ssn, width, height):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=(width, height))
    
    # Add a white rectangle to cover the old DOB value
    can.setFillColorRGB(1, 1, 1)  # Set fill color to white
    can.rect(349, height - 95, 50, 12, fill=1, stroke=0)  # Draw white rectangle (adjust dimensions as needed)

    # Add DOB and SSN to specific positions
    can.setFillColorRGB(0, 0, 0)  # Set fill color back to black
    can.setFont("Helvetica", 8)
    can.drawString(690, height - 90, f"SSN:   {ssn}")  # Adjust position as needed for SSN
    can.setFont("Helvetica", 8)
    can.drawString(351, height - 90, dob)  # Adjust position as needed for DOB

    can.save()
    packet.seek(0)
    overlay_pdf = fitz.open("pdf", packet.read())
    return overlay_pdf

def update_pdf(input_pdf, output_pdf, dob, ssn):
    doc = fitz.open(input_pdf)
    width, height = doc[0].rect.width, doc[0].rect.height

    # Create overlay with new DOB and SSN
    overlay_pdf = create_overlay(dob, ssn, width, height)
    overlay_page = overlay_pdf[0]

    # Iterate through all pages
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        if page_num == 0:  # Apply overlay only to the first page
            page.show_pdf_page(page.rect, overlay_pdf, 0)
        doc.save(output_pdf)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print("Usage: pdfchange.py <input_pdf_path> <output_pdf_path> <ssn> <dob>")
        sys.exit(1)

    input_pdf_path = sys.argv[1]
    output_pdf_path = sys.argv[2]
    ssn = sys.argv[3]
    dob = sys.argv[4]

    update_pdf(input_pdf_path, output_pdf_path, dob, ssn)
    print(f"Updated PDF saved to {output_pdf_path}")
