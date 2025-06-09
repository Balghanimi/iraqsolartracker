# output.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib.pyplot as plt
from io import BytesIO
import os
from datetime import datetime

def generate_pdf(offers, categorize_offer):
    font_path = "DejaVuSans.ttf"
    if not os.path.exists(font_path):
        raise FileNotFoundError("DejaVuSans.ttf is missing. Download from https://sourceforge.net/projects/dejavu/files/dejavu/.")
    pdfmetrics.registerFont(TTFont("Arabic", font_path))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"outputs/iraqsolartracker_{timestamp}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    title = Paragraph("<para align=right><font name='Arabic' size=14>عروض الطاقة الشمسية في العراق</font></para>", styles["Normal"])
    elements.append(title)

    prices = [o['price'] for o in offers if o['price'] > 0]
    if prices:
        plt.figure(figsize=(6, 3))
        plt.hist(prices, bins=5, color='gold', edgecolor='black')
        plt.title('توزيع الأسعار')
        plt.xlabel('السعر (IQD)')
        plt.ylabel('العدد')
        imgdata = BytesIO()
        plt.savefig(imgdata, format='png')
        imgdata.seek(0)
        elements.append(Paragraph("<para align=center><font name='Arabic'>توزيع الأسعار</font></para>", styles["Normal"]))
        elements.append(Image(imgdata, width=400, height=200))
        plt.close()

    data = [["الفئة", "العنوان", "السعر", "المحافظة", "المصدر"]]
    for offer in offers:
        category = categorize_offer(offer['title'], offer.get('snippet', ''))
        data.append([
            category,
            offer.get('title', '')[:40],
            f"{offer.get('price', 0)} {offer.get('currency', '')}",
            offer.get('governorate', ''),
            offer.get('source', '')
        ])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Arabic'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    doc.build(elements)
    return filename
