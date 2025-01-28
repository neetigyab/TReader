import glob
import os
from extractor import extract_pdf_text, check_pdf
from field_mapper import map_incout_fields_to_content
from output_generator import save_to_json

if __name__ == "__main__":
    input_folder = "ref/"
    pdf_files = glob.glob(f"{input_folder}*.pdf")

    for input_pdf in pdf_files:
        print(f"Processing file: {input_pdf}")
        lines = extract_pdf_text(input_pdf)
        
        if check_pdf(lines):
            mapped_incoming_data = map_incout_fields_to_content(lines)
            # Generate JSON output file path
            output_filename = os.path.splitext(os.path.basename(input_pdf))[0] + "_output.json"
            output_path = os.path.join(input_folder, output_filename)
            # Save the mapped data to a JSON file
            save_to_json(mapped_incoming_data, output_path)
        else:
            print("Error Reading PDF OR Invalid FILE Input")