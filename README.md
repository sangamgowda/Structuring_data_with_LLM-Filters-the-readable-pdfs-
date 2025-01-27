# PDF Table Extractor

This program extracts tables from PDF files and processes them into structured JSON data. It uses `pdfplumber` to extract tables from PDFs and `pandas` to process the data. The structured data is saved as JSON files.

## Requirements

- Python 3.8 or above
- `pdfplumber`
- `pandas`
- `transformers`

You can install the required packages using pip:

```sh
pip install pdfplumber pandas transformers
```

## Usage

1. Place the PDF files you want to process in the `Data/Pricelist` folder.
2. Run the script to process all PDFs in the folder and save the structured data in the `Data/Extracted_Data` folder.

```sh
python hehe.py
```

## Script Details

- `identify_column(column_name, mapping_type)`: Identifies the standardized column type based on predefined mappings.
- `process_table(df)`: Processes a DataFrame to extract structured data.
- `extract_tables_from_pdf(pdf_path)`: Extracts tables from a PDF file and processes them.
- `process_all_pdfs(input_folder, output_folder)`: Processes all PDFs in the input folder and saves the structured data in the output folder.

## Folder Structure

- `Data/Pricelist`: Folder containing the PDF files to be processed.
- `Data/Extracted_Data`: Folder where the structured JSON data will be saved.

## Example

If you have a PDF file named `example.pdf` in the `Data/Pricelist` folder, running the script will generate a file named `example_data.json` in the `Data/Extracted_Data` folder containing the extracted and processed data.

## License

This project is licensed under the MIT License.