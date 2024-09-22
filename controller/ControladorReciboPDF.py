from fpdf import FPDF
from datetime import datetime

# Create a PDF class extending FPDF
class PDF(FPDF):
    def header(self):
        # Add a title for the receipt
        self.set_font('Arial', 'B', 12)
        self.cell(200, 10, 'Recibo de venta', ln=True, align='C')

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_client_info(self, client_id, client_name, vendor_name, date):
        self.set_font('Arial', '', 10)
        self.ln(10)
        self.cell(100, 10, f'Cédula cliente: {client_id}', ln=True)
        self.cell(100, 10, f'Nombre del cliente: {client_name}', ln=True)
        self.cell(100, 10, f'Nombre del vendedor: {vendor_name}', ln=True)
        self.cell(100, 10, f'Fecha de venta: {date}', ln=True)

    def add_table_header(self):
        self.set_font('Arial', 'B', 10)
        self.cell(50, 10, 'Producto', 1)
        self.cell(30, 10, 'Cantidad', 1)
        self.cell(30, 10, 'Precio', 1)
        self.cell(30, 10, 'SubTotal', 1)
        self.ln()

    def add_product_row(self, product_name, quantity, price):
        self.set_font('Arial', '', 10)
        self.cell(50, 10, product_name, 1)
        self.cell(30, 10, str(quantity), 1)
        self.cell(30, 10, f'${price:.2f}', 1)
        self.cell(30, 10, f'${quantity * price:.2f}', 1)
        self.ln()

    def add_total(self, total):
        self.set_font('Arial', 'B', 10)
        self.cell(110, 10, 'Total', 1)
        self.cell(30, 10, f'${total:.2f}', 1)
        self.ln()