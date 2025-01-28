import json
import glob
import os
import pdfplumber
import pandas as pd

field_mappings_incout = {
    "environment" : ["Environment:"],
    "aba" : ["ABA:"],
    "mode" : ["Mode:"],
    "service_unit" : ["Service Unit:","Unit:","Service"],
    "cycle_date" : ["Cycle Date:","Date:","Cycle"],
    "system_date/time" : ["System Date/Time:","Date/Time:","System"],
    "status" : ["Status:"],
    "message_type" : ["Message Type:","Type:","Message"],
    "create_time" : ["Create Time:","Time:","Create"],
    "test/prod" : ["Test/Prod:"],
    "imad" : ["IMAD:"],
    "omad" : ["OMAD:"],
    "sender_aba" : ["Sender ABA {3100}:"],
    "receiver_aba" : ["Receiver ABA {3400}:"],
    "amount" : ["Amount {2000}:"],
    "type/subtype_code" : ["Type/Subtype Code {1510}:"],
    "business_function" : ["Business Function {3600}:"],
    "sender_reference" : ["Sender Reference {3320}:"],
    "reference_for_beneficary" : ["Reference for Beneficiary {4320}:"],
    "originator_to_beneficiary_information_text" : ["Originator to Beneficiary Information {6000}"],
    "originator_id" : ["ID Code:"],
    "originator_identifier" : ["Identifier:"],
    "originator_name" : ["Name:"],
    "originator_address" : ["Address:"], 
    "beneficiary_id" : ["ID Code:"],
    "beneficiary_identifier" : ["Identifier:"],
    "beneficiary_name" : ["Name:"],
    "beneficiary_address" : ["Address:"],
    "beneficiary_information_text" : ["Beneficiary Information {6400}"],
}
originator_mappings = {
    "originator_id" : ["ID Code:"],
    "originator_identifier" : ["Identifier:"],
    "originator_name" : ["Name:"],
    "originator_address" : ["Address:"],
}
beneficiary_mappings = {
    "beneficiary_id" : ["ID Code:"],
    "beneficiary_identifier" : ["Identifier:"],
    "beneficiary_name" : ["Name:"],
    "beneficiary_address" : ["Address:"],
}










def extract_pdf_text(pdf_path):
    """Extract all text lines from a PDF."""
    try:
        lines = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                page_lines = text.splitlines()
                if text:
                    print(f"--- Page {page_number} Text ---\n{page_lines}\n{'-'*50}")
                lines.extend(page_lines)
        return lines
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return []










def check_pdf(lines):
    imad_found = any("IMAD:" in line for line in lines)
    omad_found = any("OMAD:" in line for line in lines)
    return imad_found and omad_found









def originator_parsing(lines, spec_field):
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        if line == "ORIGINATOR INFORMATION":
            linex = lines[i:i+8]
        
            for field, aliases in originator_mappings.items():
                if field == spec_field:
                    # Generate all substrings of the line
                    substrings = [' '.join(linex[start:end]) for start in range(len(linex)) for end in range(start + 1, len(linex) + 1)]
                    for substring in substrings:
                        for alias in aliases:
                            if alias.lower() in substring.lower():

                                if spec_field == "originator_address":
                                    for y in range(0,len(linex)):
                                        if alias in linex[y]:
                                            xline = []
                                            xline.append(linex[y].split(":", 1)[-1].strip())
                                            for x in range(y+1,len(linex)):
                                                if x<len(linex):
                                                    if (value not in linex[x] for value in field_mappings_incout.keys()):
                                                        xline.append(linex[x]) if "Beneficiary" not in linex[x] and "INFORMATION" not in linex[x] else ""
                                    return ' '.join(xline)

                                else:
                                    for y in range(0,len(linex)):
                                        if alias in linex[y]:
                                            return linex[y].split(":", 1)[-1].strip()










def beneficiary_parsing(lines, spec_field):
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        if line == "BENEFICIARY INFORMATION":
            linex = lines[i:i+8]
        
            for field, aliases in beneficiary_mappings.items():
                if field == spec_field:
                    # Generate all substrings of the line
                    substrings = [' '.join(linex[start:end]) for start in range(len(linex)) for end in range(start + 1, len(linex) + 1)]
                    for substring in substrings:
                        for alias in aliases:
                            if alias.lower() in substring.lower():

                                if field == "beneficiary_address":
                                    for y in range(0,len(linex)):
                                        if alias in linex[y]:
                                            xline = []
                                            xline.append(linex[y].split(":", 1)[-1].strip())
                                            for x in range(y+1,len(linex)):
                                                if x<len(linex):
                                                    if (value not in linex[x] for value in field_mappings_incout.keys()):
                                                        xline.append(linex[x]) if "Page" not in linex[x] and "INFORMATION" not in linex[x] else ""
                                    return ' '.join(xline)

                                else:
                                    for y in range(0,len(linex)):
                                        if alias in linex[y]:
                                            return linex[y].split(":", 1)[-1].strip()










def map_incout_fields_to_content(lines):
    mapped_data = {}
    count = 0
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        for field, aliases in field_mappings_incout.items():
            if field not in mapped_data and any(alias.lower() in line.lower() for alias in aliases):
                if any(alias.lower() in line.lower() for alias in aliases):
                    # Generate all substrings of the line
                    words = line.split()
                    substrings = [' '.join(words[start:end]) for start in range(len(words)) for end in range(start + 1, len(words) + 1)]

                    # Check if any substring matches an alias
                    if any(alias.lower() in substring.lower() for alias in aliases for substring in substrings):

                        if field not in originator_mappings and field not in beneficiary_mappings:
                            if field == "originator_to_beneficiary_information_text" or field == "beneficiary_information_text":
                                if i + 1 < len(lines) and ":" in lines[i + 1]:
                                    mapped_data[field] = lines[i + 1].split(":", 1)[-1].strip()

                            else:
                                xline = []
                                # Extract text after the ":" and assign to the field
                                if ":" in line:
                                    xline = line.split()
                                    for x in range(0, len(xline)):
                                        if xline[x] in aliases:
                                            count = count + 1

                                        if count < 16:
                                            # There are more than 1 fields in the line
                                            for x in range(0, len(xline)):
                                                if xline[x] in aliases:
                                                    if field == "system_date/time" or field == "create_time":
                                                        mapped_data[field] = ' '.join(xline[x+1:x+3]) if x+2 < len(xline) else xline[x+1]
                                                    else:
                                                        mapped_data[field] = xline[x+1]

                                        else:
                                            # There is only 1 field in the line
                                            if field == "amount":
                                                mapped_data[field] = float(line.split(":", 1)[-1].strip())

                                            elif field not in mapped_data.keys():
                                                mapped_data[field] = line.split(":", 1)[-1].strip()

                        elif field in originator_mappings:
                            data = originator_parsing(lines, field)
                            mapped_data[field] = data

                        elif field in beneficiary_mappings:
                            data = beneficiary_parsing(lines, field)
                            mapped_data[field] = data

    # Ensure all fields have a value, defaulting to None if not found
    for field in field_mappings_incout.keys():
        if field not in mapped_data:
            mapped_data[field] = None

    return mapped_data











    



def save_to_json(mapped_data, output_path):
    """Save the mapped data to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(mapped_data, json_file, indent=4, ensure_ascii=False)
    print(f"Data saved to {output_path}")










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
