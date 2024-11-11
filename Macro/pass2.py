def pass2(input_file, pass1_output_file, output_file):
    mnt = []
    mdt = []
    kptab = {}
    pntab = {}

    with open(input_file, "r") as infile:
        section = None
        for line in infile:
            line = line.strip()
            if line.startswith("Macro Name Table(MNT):"):
                section = "MNT"
                continue
            elif line.startswith("Macro Definition Table(MDT):"):
                section = "MDT"
                continue
            elif line.startswith("Keyword Parameter Table(KPTAB):"):
                section = "KPTAB"
                continue
            elif line.startswith("Parameter Name Table(PNTAB):"):
                section = "PNTAB"
                continue
            if section == "MNT" and line:
                parts = line.split()
                line = next(infile)
                mnt.append({
                    "name": parts[1],
                    "pp_count": int(parts[2]),
                    "kp_count": int(parts[3]),
                    "mdt_pointer": int(parts[4]),
                    "kptab_pointer": int(parts[5]) if len(parts) > 5 else None
                })
            elif section == "MDT" and line:
                mdt.append(line.split(maxsplit=1)[1])
            elif section == "KPTAB" and line:
                parts = line.split()
                if len(parts) >= 3:
                    kptab[parts[1]] = parts[2]
                else:
                    print("Skipping or replacing missing keyword.\n")
            elif section == "PNTAB" and line.startswith("Macro:"):
                macro_name = line.split(":")[1].strip()
                line = next(infile)
                param_string = line.split(":")[1].strip()
                param_list = param_string.split(", ")
    
    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            line = line.strip()
            macro_call = None

            for macro in mnt:
                if line.startswith(macro["name"]):
                    macro_call = macro
                    break
            
            if macro_call:
                macro_name = macro_call["name"]
                args = line.split()[1:]
                
                #replace arguments with PNTAB:
                for i in range(macro_call["mdt_pointer"], len(mdt)):
                    if mdt[i].strip() == "MEND":
                        break
                    expanded_line = mdt[i]
                    param_list = pntab[macro_name]

                    #replace parameters with actual arguments
                    for j, param in enumerate(param_list):
                        if j < len(args):   #positional parameters
                            expanded_line = expanded_line.replace(param, args[j])
                        else:               
                            if param in kptab:  #keyword parameters
                                expanded_line = expanded_line.replace(param, kptab[param])
                            else:
                                expanded_line = expanded_line.replace(param, "")
                    outfile.write(expanded_line + "\n")
            else:
                outfile.write(line + "\n")
    
    print(f"Pass 2 complete, asm code generated in {output_file}")
#example usage
input_file = "/Users/yashraj146/Documents/LP1 Sem 5/Macro/source_code.asm"
pass1_output_file = "/Users/yashraj146/Documents/LP1 Sem 5/Macro/output-mPass1.txt"
output_file = "/Users/yashraj146/Documents/LP1 Sem 5/Macro/output-mPass2.asm"

pass2(input_file, pass1_output_file, output_file)
