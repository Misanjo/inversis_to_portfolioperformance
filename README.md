# Inversis to Portfolio Performance Converter

This tool automates the conversion of Inversis investment fund and pension plan export files (`.xls` format) into CSV files compatible with [Portfolio Performance](https://www.portfolio-performance.info/).

## Key Features

- **Automatic File Detection**: Distinguishes between standard investment funds and pension plans based on the filename (checks for 'pp' suffix).
- **Precision Recovery**:
    - **Pension Plans**: Recalculates shares using `Amount / Price` to recover fractional digits truncated in Inversis reports.
    - **Investment Funds**: Uses original reported quantities to maintain consistency.
- **Differentiated Logic**: Correctly handles "Importe neto" as the source of truth for all cash flows.
- **Signed Execution Summary**: Displays a professional summary after each file, correctly subtracting sales/transfers and showing only active positions.
- **Dynamic Configuration**: All column mappings and operation types are externalized in `config.yaml`.
- **Portfolio Performance Ready**: Generates CSVs with Spanish locale compatibility (`;` separator, `,` decimal).

## Project Structure

```text
.
├── input/                # Place your raw Inversis .xls files here
├── output/               # Converted .csv files will appear here
├── src/
│   └── parsers/          # Modular parsing logic
│       ├── base_parser.py
│       ├── investment_parser.py
│       └── pension_parser.py
├── tests/                # Automated unit tests
├── config.yaml           # External configuration for columns and operations
├── main.py               # Main application entry point
└── requirements.txt      # Dependency list
```

## Setup

1. Ensure you have Python 3.8+ installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your Inversis exports in the `input` directory.
   - For pension plans, ensure the filename contains `pp` (e.g., `salida_pp.xls`).
   - For standard funds, use any other name (e.g., `salida.xls`).
2. Run the converter:
   ```bash
   python main.py
   ```
3. Find your converted files in the `output` directory and a detailed summary in the terminal.

## Configuration

You can customize column names and operation types in `config.yaml` without touching the code. This is useful if Inversis changes their export format.

## Testing

Run unit tests using the built-in `unittest` module:
```bash
python -m unittest discover tests
```
