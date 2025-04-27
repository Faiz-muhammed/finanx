from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


class pdfUtils:
    def create_pdf_df(df, title):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)

        # Prepare the title
        styles = getSampleStyleSheet()
        title_paragraph = Paragraph(title, styles['Title'])

        # Convert DataFrame to list of lists (including header)
        data = [df.columns.tolist()] + df.values.tolist()

        print(data,'data to print')

        # Create the table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#dbeafe")),  # Header row background
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),                # Header row text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),             # Header font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

            ('GRID', (0, 0), (-1, -1), 1, colors.grey),                  # Grid lines
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])  # Alt row colors
        ]))

        # Add title and table to elements list
        elements = [title_paragraph, table]
        doc.build(elements)
        
        buffer.seek(0)
        return buffer