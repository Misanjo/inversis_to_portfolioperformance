import unittest
import pandas as pd
from src.parsers.investment_parser import InvestmentParser
from src.parsers.pension_parser import PensionPlanParser


class TestParsers(unittest.TestCase):
    def setUp(self):
        self.config = {
            'parsers': {
                'investment': {
                    'columns': {
                        'date_op': 'Fechas|Operación',
                        'date_liq': 'Fechas|Liquidación',
                        'op_num': 'Operación|Operación',
                        'op_type': 'Operación|Operación.1',
                        'isin': 'ISIN|ISIN',
                        'quantity': 'Títulos/NOMINAL|Títulos/NOMINAL',
                        'currency': 'Divisa|Divisa',
                        'price': 'Precio Neto|Precio Neto'
                    },
                    'mappings': {
                        'buy': ['SUSCRIPCION'],
                        'sell': ['REEMBOLSO']
                    }
                },
                'pension': {
                    'columns': {
                        'date_op': 'Fechas|Operación',
                        'date_liq': 'Fechas|Liquidación',
                        'op_num': 'Operación|Operación',
                        'op_type': 'Operación|Operación.1',
                        'isin': 'ISIN|ISIN',
                        'quantity': 'Títulos/NOMINAL|Títulos/NOMINAL',
                        'currency': 'Divisa|Divisa',
                        'price': 'Precio Neto|Precio Neto'
                    },
                    'mappings': {
                        'buy': ['APORTACION P.P.'],
                        'sell': []
                    }
                }
            }
        }
        self.investment_parser = InvestmentParser(self.config)
        self.pension_parser = PensionPlanParser(self.config)

    def test_investment_parser_transform(self):
        # Mock data for investment file
        data = {
            'Fechas|Operación': ['01/01/2023'],
            'Fechas|Liquidación': ['02/01/2023'],
            'Operación|Operación': ['123456'],
            'Operación|Operación.1': ['SUSCRIPCION'],
            'ISIN|ISIN': ['ES0123456789'],
            'Títulos/NOMINAL|Títulos/NOMINAL': ['10.5'],
            'Divisa|Divisa': ['EUR'],
            'Precio Neto|Precio Neto': ['100.0']
        }
        df = pd.DataFrame(data)

        df_transformed = self.investment_parser.transform(df)

        self.assertEqual(len(df_transformed), 1)
        self.assertEqual(df_transformed.iloc[0]['Tipo'], 'Compra')
        self.assertEqual(df_transformed.iloc[0]['Fecha'], '2023-01-02')
        self.assertEqual(float(df_transformed.iloc[0]['Cantidad']), 10.5)

    def test_pension_parser_transform(self):
        # Mock data for pension file
        data = {
            'Fechas|Operación': ['2023-01-01'],
            'Fechas|Liquidación': ['2023-01-02'],
            'Operación|Operación': ['789012'],
            'Operación|Operación.1': ['APORTACION P.P.'],
            'ISIN|ISIN': ['N5138'],
            'Títulos/NOMINAL|Títulos/NOMINAL': ['11'],
            'Divisa|Divisa': ['EUR'],
            'Precio Neto|Precio Neto': ['23.43']
        }
        df = pd.DataFrame(data)

        df_transformed = self.pension_parser.transform(df)

        self.assertEqual(len(df_transformed), 1)
        self.assertEqual(df_transformed.iloc[0]['Tipo'], 'Compra')
        self.assertEqual(df_transformed.iloc[0]['Fecha'], '2023-01-02')
        self.assertEqual(int(df_transformed.iloc[0]['Cantidad']), 11)

    def test_investment_mapping(self):
        self.assertEqual(self.investment_parser.map_operation_type(
            'SUSCRIPCION'), 'Compra')
        self.assertEqual(
            self.investment_parser.map_operation_type('REEMBOLSO'), 'Venta')


if __name__ == '__main__':
    unittest.main()
