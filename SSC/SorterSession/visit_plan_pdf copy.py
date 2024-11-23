from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_visit_plan_pdf_with_svg(data, filename="visit_plan_with_logo.pdf", svg_path=None):
    # Custom Canvas to set background color
    class BackgroundColorCanvas(canvas.Canvas):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Set background color
            self.setFillColor(colors.HexColor("#fffcf3"))
            self.rect(0, 0, self._pagesize[0], self._pagesize[1], stroke=0, fill=1)

    pdf = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=20,  # Set left margin to 20 points
        rightMargin=20,  # Set right margin to 20 points
        topMargin=20,  # Set top margin to 20 points
        bottomMargin=20,
    )
    elements = []

    # Add the SVG logo if provided
    if svg_path:
        drawing = svg2rlg(svg_path)
        elements.append(drawing)

    # Add spacing after logo
    elements.append(Paragraph("<br/><br/>", getSampleStyleSheet()['Normal']))

    # Title
    styles = getSampleStyleSheet()
    title = Paragraph("Visit Plan for Divyam Shah", styles['Title'])
    elements.append(title)

    # Add spacing after title
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    # Table data: add column headers
    table_data = [["Sr. No.", "Property Name", "Date", "Time", "Address"]]

    # Add rows from data
    for row in data:
        table_data.append([
            row.get("Sr. No."),
            row.get("property_name"),
            row.get("Arrival_date"),
            row.get("Arrival_time"),
            Paragraph(row.get("Address"), styles['Normal']),  # Wrap the text in Paragraph
        ])

    # Create a table
    table = Table(table_data, colWidths=[40, 100, 70, 70, 200])  # Adjust column widths

    # Style the table
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    # Add the table to the document
    elements.append(table)

    # Build the PDF with the custom canvas
    pdf.build(elements, canvasmaker=BackgroundColorCanvas)
    print(f"PDF generated successfully: {filename}")

# Example usage
visit_data = [
    {"Sr. No.": 1, "property_name": "Siddhi Sadhan", "Arrival_time": "10:05", "Arrival_date": "2024-11-24", "Address": "Rankaj Society, Ahmedabad, Rankaj Society, Ahmedabad, Rankaj Society, Ahmedabad, Rankaj Society, Ahmedabad"},
    {"Sr. No.": 2, "property_name": "Siddhi Sadhan", "Arrival_time": "11:09", "Arrival_date": "2024-11-24", "Address": "Rankaj Society, Ahmedabad, Rankaj Society, Ahmedabad, Rankaj Society, Ahmedabad, Rankaj Society, Ahmedabad"},
    {"Sr. No.": 3, "property_name": "Siddhi Sadhan", "Arrival_time": "12:09", "Arrival_date": "2024-11-24", "Address": "Rankaj Society, Ahmedabad, Rankaj Society, Ahmedabad, Rankaj Society, Ahmedabad, Rankaj Society, Ahmedabad"}
]

svg_path = r"C:\Users\Divyam Shah\OneDrive\Desktop\Dynamic Labz\Clients\Clients\Square Second Consultancy\SSC\SSC\static\img\Logo.svg"
generate_visit_plan_pdf_with_svg(visit_data, "visit_plan_with_svg_logo.pdf", svg_path)
