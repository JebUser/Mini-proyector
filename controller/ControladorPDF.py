import os

from fpdf import FPDF

class ControladorPdf:
    # Constructor
    def __init__(self) -> None:
        super().__init__()
        self.pdf = FPDF()

    def generar_recibo(self):
        return

    def generar_reporte(self):
        return