import pandas as pd
import yaml
from pathlib import Path
from src.parsers.investment_parser import InvestmentParser
from src.parsers.pension_parser import PensionPlanParser


def setup_directories(input_dir: Path, output_dir: Path):
    """Ensures input and output directories exist."""
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)


def load_config(config_path: Path) -> dict:
    """Loads YAML configuration."""
    if not config_path.exists():
        print(f"Warning: Configuration file {config_path} not found.")
        return {}
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def display_summary(all_data: pd.DataFrame):
    """Displays a professional summary grouped by ISIN."""
    if all_data.empty:
        print("\nNo data processed to display summary.")
        return

    print("\n" + "="*80)
    print(f"{'ISIN':<15} | {'Trans.':<6} | {'Total Qty':<12} | {'Avg Price':<12} | {'Total Value':<12}")
    print("-" * 80)

    # Create a copy to avoid modifying original data
    df = all_data.copy()

    # Negate quantities and amounts for sales to calculate current balance
    mask_venta = df['Tipo'] == 'Venta'
    df.loc[mask_venta, 'Cantidad'] = -df.loc[mask_venta, 'Cantidad']
    df.loc[mask_venta, 'Importe'] = -df.loc[mask_venta, 'Importe']

    summary = df.groupby('ISIN').agg({
        'Tipo': 'count',
        'Cantidad': 'sum',
        'Importe': 'sum'
    }).rename(columns={'Tipo': 'Count', 'Cantidad': 'Total_Qty', 'Importe': 'Total_Value'})

    # Filter out ISINs with zero balance (considering floating point precision)
    summary = summary[summary['Total_Qty'].abs() > 1e-6]

    if summary.empty:
        print("\nAll positions in this file are closed (zero balance).")
        return

    summary['Avg_Price'] = summary['Total_Value'] / summary['Total_Qty']

    # Sort by Total Value descending
    summary = summary.sort_values(by='Total_Value', ascending=False)

    for isin, row in summary.iterrows():
        print(
            f"{isin:<15} | {int(row['Count']):<6} | {row['Total_Qty']:>12.4f} | "
            f"{row['Avg_Price']:>12.4f} | {row['Total_Value']:>12.2f}"
        )

    print("="*80)


def process_all_files(input_dir: Path, output_dir: Path, config: dict):
    """
    Scans input directory and processes files based on their names.
    - Files with 'pp' in name -> PensionPlanParser
    - Others -> InvestmentParser
    """
    files = list(input_dir.glob("*.xls"))

    if not files:
        print(f"No .xls files found in {input_dir}")
        return

    investment_parser = InvestmentParser(config)
    pension_parser = PensionPlanParser(config)

    for file_path in files:
        filename = file_path.name.lower()
        output_filename = file_path.stem + ".csv"
        output_path = output_dir / output_filename

        print(f"\n--- Processing {file_path.name} ---")

        try:
            if 'pp' in filename:
                print("Detected as: Pension Plan File")
                df = pension_parser.process_file(file_path, output_path)
            else:
                print("Detected as: Investment Fund File")
                df = investment_parser.process_file(file_path, output_path)

            if df is not None and not df.empty:
                display_summary(df)
        except Exception as e:
            print(f"ERROR processing {file_path.name}: {e}")


def main():
    # Define paths relative to the project root
    base_dir = Path(__file__).parent
    input_dir = base_dir / "input"
    output_dir = base_dir / "output"
    config_path = base_dir / "config.yaml"

    setup_directories(input_dir, output_dir)
    config = load_config(config_path)

    print("* Inversis to Portfolio Performance Converter")
    print(f"Input folder: {input_dir}")
    print(f"Output folder: {output_dir}")

    process_all_files(input_dir, output_dir, config)

    print("\nProcessing complete!")


if __name__ == "__main__":
    main()
