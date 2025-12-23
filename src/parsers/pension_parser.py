import pandas as pd
from .base_parser import BaseParser


class PensionPlanParser(BaseParser):
    """
    Parser for pension plan files (salida_pp.xls)
    """

    def __init__(self, config: dict):
        super().__init__(config, 'pension')

    def map_operation_type(self, operation: str) -> str:
        """
        Maps Pension Plan operations to Portfolio Performance types.
        """
        buy_operations = set(self.mappings.get('buy', []))
        sell_operations = set(self.mappings.get('sell', []))

        if operation in buy_operations:
            return 'Compra'
        elif operation in sell_operations:
            return 'Venta'
        return 'Compra'  # Default

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_pp = pd.DataFrame()

        # Get column names from config
        col_fecha_op = self.columns.get('date_op')
        col_fecha_liq = self.columns.get('date_liq')
        col_operacion_num = self.columns.get('op_num')
        col_tipo_op = self.columns.get('op_type')
        col_isin = self.columns.get('isin')
        col_titulos = self.columns.get('quantity')
        col_divisa = self.columns.get('currency')
        col_precio = self.columns.get('price')
        col_importe = self.columns.get('amount')

        # Date logic
        df['Fecha_Op'] = self.parse_dates(df[col_fecha_op])
        df['Fecha_Liq'] = self.parse_dates(df[col_fecha_liq])
        df_pp['Fecha'] = df['Fecha_Liq'].fillna(
            df['Fecha_Op']).dt.strftime('%Y-%m-%d')

        # Type logic
        df_pp['Tipo'] = df[col_tipo_op].apply(self.map_operation_type)

        # Basic fields
        df_pp['ISIN'] = df[col_isin]
        # Calculate quantity from amount/price for maximum precision
        raw_qty = pd.to_numeric(df[col_titulos], errors='coerce')
        price = pd.to_numeric(df[col_precio], errors='coerce')
        amount = pd.to_numeric(df[col_importe], errors='coerce').abs()

        # In pension plan files, the displayed quantity is often rounded to integers.
        # We recalculate it from the total amount and unit price.
        df_pp['Cantidad'] = amount / price
        df_pp['Valor'] = price
        df_pp['Importe'] = amount
        df_pp['Moneda de la transacción'] = df[col_divisa]
        df_pp['Comisiones'] = 0.0

        # Note
        df_pp['Nota'] = df[col_tipo_op] + ' - Op: ' + \
            df[col_operacion_num].astype(str)

        # Cleanup
        return df_pp.dropna(subset=['Fecha', 'ISIN', 'Cantidad'])
