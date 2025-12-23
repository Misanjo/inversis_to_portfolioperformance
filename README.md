# Inversis to Portfolio Performance Converter

This tool automates the conversion of Inversis investment fund and pension plan export files (`.xls` format) into CSV files compatible with [Portfolio Performance](https://www.portfolio-performance.info/).

## Features

- **Automatic File Detection**: Distinguishes between standard investment funds and pension plans based on the filename (checks for 'pp' suffix).
- **Inheritance-based Architecture**: Modular design for easy extension to other file formats.
- **Robust Transformation**: Handles HTML-based XLS exports, MultiIndex columns, and normalized date formats.
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
├── main.py               # Main application entry point
└── README.md
```

## Setup

1. Ensure you have Python 3.8+ installed.
2. Install dependencies:
   ```bash
   pip install pandas lxml openpyxl
   ```

## Usage

1. Place your Inversis exports in the `input` directory.
   - For pension plans, ensure the filename contains `pp` (e.g., `salida_pp.xls`).
   - For standard funds, use any other name (e.g., `salida.xls`).
2. Run the converter:
   ```bash
   python main.py
   ```
3. Find your converted files in the `output` directory.

## Testing

Run unit tests using the built-in `unittest` module:
```bash
python -m unittest discover tests
```
