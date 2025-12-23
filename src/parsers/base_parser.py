import pandas as pd
from abc import ABC, abstractmethod
from pathlib import Path


class BaseParser(ABC):
    """
    Base class for Inversis parsers.
    Handles file loading and CSV export.
    """

    def __init__(self, config: dict, mapping_name: str):
        self.config = config.get('parsers', {}).get(mapping_name, {})
        self.columns = self.config.get('columns', {})
        self.mappings = self.config.get('mappings', {})

    def load_file(self, file_path: Path) -> pd.DataFrame:
        """
        Loads the Inversis HTML-based XLS file.
        """
        # Inversis exports are actually HTML tables
        df_list = pd.read_html(str(file_path))
        if not df_list:
            raise ValueError(f"No tables found in {file_path}")

        df = df_list[0]

        # Flatten MultiIndex columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['|'.join(col).strip() for col in df.columns.values]

        # Remove empty rows or headers-as-rows
        if len(df) > 0 and df.iloc[0].astype(str).str.contains('Operación|Liquidación', na=False).any():
            df = df.iloc[1:].reset_index(drop=True)

        return df

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the Inversis DataFrame to Portfolio Performance format.
        Must be implemented by subclasses.
        """
        pass

    def save_to_csv(self, df: pd.DataFrame, output_path: Path):
        """
        Saves the transformed DataFrame to a CSV compatible with Portfolio Performance.
        Uses ';' as separator and ',' as decimal separator by default.
        """
        df.to_csv(output_path, index=False,
                  encoding='utf-8-sig', sep=';', decimal=',')

    def parse_dates(self, series: pd.Series) -> pd.Series:
        """
        Parses dates assuming YYYY-MM-DD format as specified by User.
        """
        return pd.to_datetime(series, errors='coerce')

    def process_file(self, input_path: Path, output_path: Path) -> pd.DataFrame:
        """
        Full process: load, transform, and save.
        Returns the transformed DataFrame.
        """
        print(f"Reading: {input_path}")
        df = self.load_file(input_path)
        print(f"  Parsed {len(df)} rows")

        df_transformed = self.transform(df)
        print(
            f"  Transformed to {len(df_transformed)} Portfolio Performance rows")

        self.save_to_csv(df_transformed, output_path)
        print(f"  Saved to: {output_path}")
        return df_transformed
