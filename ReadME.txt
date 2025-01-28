# PDF Data Extraction and Mapping Project

## Project Overview
This project is designed to extract, parse, and map data from specifically structured Transaction summary files. It processes banking or financial PDFs, identifying specific fields such as IMAD, OMAD, and transaction details, and outputs the data into structured JSON files. The modular design allows for flexibility, scalability, and maintainability by separating concerns into distinct modules.

## Features
- Extracts text from PDF files.
- Validates the presence of mandatory fields (e.g., IMAD and OMAD) before processing.
- Parses originator and beneficiary information.
- Maps extracted text to predefined fields.
- Outputs the processed data to JSON files.
- Modular codebase with reusable components.

---

## Project Structure
### Modules and Functions

### 1. **`config.py`**
This module contains configuration data such as field mappings for identifying and extracting specific fields from the PDF text.
- **`field_mappings_incout`**: Maps field names to aliases or keywords for detecting corresponding values in the PDF.
- **`originator_mappings`**: Defines mappings for originator-related fields.
- **`beneficiary_mappings`**: Defines mappings for beneficiary-related fields.

### 2. **`extractor.py`**
Handles the extraction of text from PDFs and validation of mandatory fields.
- **`extract_pdf_text(pdf_path)`**:
  - Extracts text line by line from the provided PDF file.
  - Uses the `pdfplumber` library for reading the PDF.
  - Returns a list of text lines from the PDF.
- **`check_pdf(lines)`**:
  - Validates whether the mandatory fields `IMAD` and `OMAD` are present in the extracted lines.
  - Returns `True` if both fields are found, otherwise returns `False`.

### 3. **`group_parser.py`**
Parses detailed information related to originators and beneficiaries.
- **`originator_parsing(lines, spec_field)`**:
  - Extracts detailed information for specified originator fields.
  - Handles multi-line values, such as addresses, by combining relevant lines.
- **`beneficiary_parsing(lines, spec_field)`**:
  - Similar to `originator_parsing`, but processes beneficiary-related fields.

### 4. **`field_mapper.py`**
Maps extracted text to predefined fields based on the configuration.
- **`map_incout_fields_to_content(lines)`**:
  - Iterates through lines of extracted text and maps values to fields defined in `field_mappings_incout`.
  - Handles special parsing logic for fields such as system dates, creation times, and amounts.
  - Ensures all configured fields are included in the output, defaulting to `None` if not found.

### 5. **`output_generator.py`**
Generates the final JSON output.
- **`save_to_json(mapped_data, output_path)`**:
  - Saves the processed data to a JSON file at the specified output path.
  - Utilizes Python's built-in `json` library for structured output.

### 6. **`main.py`**
The entry point for the application.
- Calls functions from all other modules to process PDF files.
- Validates the PDF using `check_pdf`.
- Extracts text, maps fields, and generates JSON output.
- Displays an error message if the mandatory fields are missing.

---

## Libraries Used
- **`pdfplumber`**:
  - Extracts text from PDF files.
  - Handles structured PDFs, preserving line-by-line formatting.

- **`json`**:
  - Serializes Python objects into JSON format.
  - Enables structured storage of processed data.

- **`glob`**:
  - Retrieves file paths matching specific patterns (e.g., all PDFs in a folder).

- **`os`**:
  - Handles file system interactions such as path manipulations.

- **`pandas`**:
  - Reserved for potential advanced data processing (not extensively used in the current implementation).

---

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   ```
2. Navigate to the project directory:
   ```bash
   cd pdf-data-extraction
   ```
3. Install dependencies:
   ```bash
   pip install pdfplumber pandas
   ```

---

## Usage
1. Place all PDF files to be processed in the `ref/` directory.
2. Run the `main.py` script:
   ```bash
   python main.py
   ```
3. Check the `ref/` directory for the generated JSON files.

---

## Example Output
For a sample PDF file containing:
```
IMAD: 12345
OMAD: 67890
Amount: 1000.00
```
The JSON output will be:
```json
{
    "imad": "12345",
    "omad": "67890",
    "amount": 1000.00,
    ...
}
```

---

## Error Handling
- If mandatory fields (`IMAD`, `OMAD`) are missing, an error message will be displayed:
  ```
  ERROR Reading PDF OR Invalid FILE Input
  ```
- Ensure the PDF files are structured correctly and contain the required fields.

---

## Future Enhancements
- Add support for other structured document types.
- Implement a graphical interface for easier operation.
- Extend logging and error reporting for better diagnostics.

---

## Contributors
- **Neetigya Bisen**: Developer and maintainer of the project.

---


