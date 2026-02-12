
from pdf2docx import Converter as PDFConverter
from docx2pdf import convert as docx_to_pdf

from .base import BaseConverter


class PDFtoDOCXConverter(BaseConverter):

    def convert(self, input_path: str, output_path: str):
        pdf = PDFConverter(input_path)
        pdf.convert(output_path)
        pdf.close()



class DOCXtoPDFConverter(BaseConverter):

    def convert(self, input_path: str, output_path: str):
        docx_to_pdf(input_path, output_path)




