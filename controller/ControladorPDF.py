from fpdf import FPDF
import pandas as pd
from dateutil.relativedelta import relativedelta

class ControladorPdf(FPDF):

    def generar_recibo(self):
        return

    def generar_reporte(self, total_revenue:float, last_month:int, this_month:int, per_trans:int, taxes:float, diagram_path:str, circle_path:str):
        self.add_page(orientation='L')

        # Titulo del doc.
        self.set_xy(107,10)
        self.set_font('Arial', 'B', 24)
        self.cell(80, 10, "JAVE POS-SALES REPORT", 0, 1, 'C')

        # Intervalo de cálculo.
        self.set_xy(115, 17)
        self.set_font('Arial', '', 12)
        self.cell(80, 10, f"(From {(pd.Timestamp.now() - relativedelta(years=1)).strftime('%d %b %Y')} to {pd.Timestamp.now().strftime('%d %b %Y')})")

        # TOTAL REVENUE
        # sombra.
        self.set_fill_color(72, 72, 72)
        self.rect(42,32,100,40,'F')
        # rectangulo que rodea.
        self.set_fill_color(255, 255, 255)
        self.rect(40,30,100,40,'F')
        self.set_fill_color(255, 255, 255)
        self.rect(40,30,100,40,'L')

        # Titulo.
        self.set_xy(50,35)
        self.set_font('Arial', 'B', 22)
        self.cell(80, 10, "Total Revenue", 0, 1, 'C')

        # Valor.
        self.set_xy(50,55)
        self.set_text_color(0,102,153)
        self.set_font('Arial', '', 22)
        self.cell(80, 10, f'${total_revenue:,.2f}', 0, 1, 'C')

        # PRODUCTS SOLD
        # sombra.
        self.set_fill_color(72, 72, 72)
        self.rect(153,32,100,40,'F')
        # rectangulo que rodea.
        self.set_fill_color(255, 255, 255)
        self.rect(155,30,100,40,'F')
        self.set_fill_color(255, 255, 255)
        self.rect(155,30,100,40,'L')

        # Titulo.
        self.set_text_color(0,0,0)
        self.set_xy(165,35)
        self.set_font('Arial', 'B', 22)
        self.cell(80, 10, "Products Sold", 0, 1, 'C')

        # Valor.
        self.set_xy(165,50)
        self.set_font('Arial', '', 12)
        self.cell(80, 10, f'Current Month: {this_month}', 0, 1, 'C')
        self.set_xy(165,60)
        self.set_font('Arial', '', 12)
        self.cell(80, 10, f'Previous Month: {last_month}', 0, 1, 'C')

        # AVERAGE UNITS PER TRANSACTION
        # sombra.
        self.set_fill_color(72, 72, 72)
        self.rect(42,77,100,40,'F')
        # rectangulo que rodea.
        self.set_fill_color(255, 255, 255)
        self.rect(40,75,100,40,'F')
        self.set_fill_color(255, 255, 255)
        self.rect(40,75,100,40,'L')

        # Titulo.
        self.set_xy(50,78)
        self.set_font('Arial', 'B', 18)
        self.cell(80, 10, "Average Units Per Transaction", 0, 1, 'C')

        # Valor.
        self.set_xy(50,98)
        self.set_font('Arial', '', 22)
        self.cell(80, 10, f'{per_trans} units', 0, 1, 'C')

        # MOST SOLD PRODUCT
        # sombra.
        self.set_fill_color(72, 72, 72)
        self.rect(153,77,100,40,'F')
        # rectangulo que rodea.
        self.set_fill_color(255, 255, 255)
        self.rect(155,75,100,40,'F')
        self.set_fill_color(255, 255, 255)
        self.rect(155,75,100,40,'L')

        # Titulo.
        self.set_xy(165,78)
        self.set_font('Arial', 'B', 20)
        self.cell(80, 10, "Total Taxes", 0, 1, 'C')

        # Valor.
        self.set_xy(165,98)
        self.set_font('Arial', '', 22)
        self.set_text_color(255,45,45)
        self.cell(80, 10, f'${taxes:,.2f}', 0, 1, 'C')

        # Diagrama de lineas.
        self.image(diagram_path, x=140, y=120, w=130)

        # Diagrama Circular.
        self.image(circle_path, x=42, y=120, w=90)