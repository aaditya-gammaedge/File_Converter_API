
import pandas as pd
from .base import BaseConverter


class CSVtoJSONConverter(BaseConverter):

    def convert(self, input_path: str, output_path: str):
        df = pd.read_csv(input_path)
        df.to_json(output_path, orient="records", indent=4)


class JSONtoCSVConverter(BaseConverter):

    def convert(self, input_path: str, output_path: str):
        df = pd.read_json(input_path)
        df.to_csv(output_path, index=False)


class CSVtoExcelConverter(BaseConverter):

    def convert(self, input_path: str, output_path: str):
        df = pd.read_csv(input_path)
        df.to_excel(output_path, index=False)


class ExceltoCSVConverter(BaseConverter):

    def convert(self, input_path: str, output_path: str):
        df = pd.read_excel(input_path)
        df.to_csv(output_path, index=False)


