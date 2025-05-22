import random
import string
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def generate_random_text_paragraph(length=150):
    """Generate a paragraph of random characters."""
    return ''.join(random.choices(string.ascii_letters + " ", k=length)).strip()

def create_pdf_with_format(file_name, num_paragraphs=5, page_size=A4):
    """Create a PDF with a formatted structure."""
    c = canvas.Canvas(file_name, pagesize=page_size)
    width, height = page_size
    margin = 50

    # Title
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width / 2, height - margin, "Randomly Generated Document")
    
    # Subtitle
    c.setFont("Helvetica", 16)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height - margin - 30, "Generated with Python")
    
    y = height - margin - 80  # Adjust y-coordinate for content
    
    for i in range(1, num_paragraphs + 1):
        if y < 100:  # Start a new page if near the bottom
            c.showPage()
            c.setFont("Helvetica-Bold", 24)
            c.drawCentredString(width / 2, height - margin, f"Continued: Section {i}")
            y = height - margin - 80
        
        # Section Heading
        c.setFont("Helvetica-Bold", 18)
        c.setFillColor(colors.darkgreen)
        c.drawString(margin, y, f"Section {i}: Random Insights")
        y -= 30

        # Paragraph Content
        c.setFont("Times-Roman", 12)
        c.setFillColor(colors.black)
        paragraph = generate_random_text_paragraph(length=300)
        for line in split_text_into_lines(paragraph, width - 2 * margin, c):
            if y < 100:  # Start a new page if near the bottom
                c.showPage()
                c.setFont("Times-Roman", 12)
                y = height - margin - 80
            c.drawString(margin, y, line)
            y -= 14

    c.save()
    print(f"PDF generated: {file_name}")

def split_text_into_lines(text, max_width, canvas_obj):
    """Split a paragraph into lines that fit within the page width."""
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        if canvas_obj.stringWidth(current_line + word + " ") > max_width:
            lines.append(current_line)
            current_line = word + " "
        else:
            current_line += word + " "
    lines.append(current_line.strip())
    return lines

def generate_multiple_pdfs_with_format(num_pdfs, num_paragraphs=5):
    """Generate multiple PDF files with formatted content."""
    for i in range(1, num_pdfs + 1):
        file_name = f"formatted_random_document_{i}.pdf"
        create_pdf_with_format(file_name, num_paragraphs=num_paragraphs)

# User input: Number of PDFs and paragraphs
try:
    num_pdfs = int(input("Enter the number of PDF files to generate: "))
    num_paragraphs = int(input("Enter the number of paragraphs per PDF: "))
    generate_multiple_pdfs_with_format(num_pdfs, num_paragraphs)
except ValueError:
    print("Please enter valid numbers.")
