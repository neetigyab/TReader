from config import field_mappings_incout, originator_mappings, beneficiary_mappings
from group_parser import originator_parsing, beneficiary_parsing

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