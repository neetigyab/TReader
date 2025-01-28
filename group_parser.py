from config import field_mappings_incout, originator_mappings, beneficiary_mappings

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