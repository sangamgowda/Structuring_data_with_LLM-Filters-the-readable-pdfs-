import os
import pdfplumber
import pandas as pd
import json
import re
from transformers import pipeline

# Initialize Hugging Face pipeline for LLM processing
generator = pipeline("text-generation", model="gpt2")

# Define column mappings
COLUMN_MAPPINGS = {
    "id_columns": ['Cat. NO', 'Order no', 'Diamond Chain Part No', 'Part No.', 'Catalog No.', 'Cat.Nos', 'IDH No.'],
    "title_columns": ['type', 'electrical product names', 'Carding Machine'],
    "description_columns": ['description', 'Type and frame size', 'Product Description', 'in mm', 'in inches'],
    "price_columns": ['M.R.P.', 'LP in INR', 'PRICE IN RS', 'MRP Per Metre', 'Rs.   P.', 'Price', 'MRP', 'price']
}

def identify_column(column_name, mapping_type):
    """Identify the standardized column type using regular expressions."""
    if not column_name:  # Handle None or empty column names
        return False
    for keyword in COLUMN_MAPPINGS[mapping_type]:
        if re.search(rf"\b{re.escape(keyword.lower())}\b", column_name.lower()):
            return True
    return False

def process_table(df):
    """Process the table to extract structured data."""
    structured_data = []
    for _, row in df.iterrows():
        if row.isnull().all():  # Skip empty rows
            continue
        
        # Map columns to standardized names
        sku_id = next((row[col] for col in df.columns if identify_column(col, "id_columns")), None)
        title = next((row[col] for col in df.columns if identify_column(col, "title_columns")), None)
        description = next((row[col] for col in df.columns if identify_column(col, "description_columns")), None)
        
        # Clean and parse price
        price = next((row[col] for col in df.columns if identify_column(col, "price_columns")), None)
        try:
            price = float(str(price).replace(",", "").strip().replace("₹", "").replace("$", "")) if price else None
        except ValueError:
            price = None

        # Collect additional attributes
        attributes = {}
        for col in df.columns:
            if not any(identify_column(col, key) for key in COLUMN_MAPPINGS.keys()):
                value = row[col]
                attributes[col] = str(value).strip() if pd.notnull(value) else None

        # Skip rows with no meaningful data
        if not sku_id and not title and not description:
            continue

        title = title.strip() if title else "Unknown Title"
        description = description.strip() if description else "No Description"

        # Add structured entry
        structured_data.append({
            "ID": sku_id,
            "title": title,
            "description": description,
            "price": price,
            "attributes": attributes
        })
    return structured_data

def extract_tables_from_pdf(pdf_path):
    """Extract tables from PDF using pdfplumber."""
    all_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            try:
                table = page.extract_table(table_settings={
                    "vertical_strategy": "lines",
                    "horizontal_strategy": "lines"
                })
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])  # First row as header
                    if df.shape[1] > 2:  # Only process tables with > 2 columns
                        print(f"DEBUG: Extracting structured data from Page {page_number}")
                        structured_data = process_table(df)
                        all_data.extend(structured_data)
            except Exception as e:
                print(f"ERROR: Failed to extract table on page {page_number}: {e}")
    return all_data

def process_all_pdfs(input_folder, output_folder):
    """Process all PDFs in a folder and save structured data for each."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".pdf"):  # Process only PDF files
            pdf_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}_data.json")
            
            print(f"Processing {pdf_path}...")
            all_data = extract_tables_from_pdf(pdf_path)
            if all_data:  # Save only if there's valid data
                with open(output_path, "w") as f:
                    json.dump(all_data, f, indent=4)
                print(f"Data saved to {output_path}")
            else:
                print(f"No data extracted from {pdf_path}")

# Folder paths
input_folder = "Data/Pricelist"
output_folder = "Data/Extracted_Data"

# Run the process
process_all_pdfs(input_folder, output_folder)
