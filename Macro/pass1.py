class Macro:
    def __init__(self, name, parameters, definition):
        self.name = name
        self.parameters = parameters
        self.definition = definition

def pass1(input_file, output_file):
    macros = {}  # Dictionary to store macro definitions
    mnt = []  # Macro Name Table (MNT)
    mdt = []  # Macro Definition Table (MDT)
    kptab = []  # Keyword Parameter Table (KPTAB)
    pntab = {}  # Parameter Name Table (PNTAB)

    # To track MDT and KPTAB pointers
    mdt_pointer = 1
    kptab_pointer = 1

    with open(input_file, "r") as infile:
        inside_macro = False
        current_macro_name = None
        current_macro_params = []
        current_macro_def = []
        pp_count = 0  # Positional parameters count
        kp_count = 0  # Keyword parameters count

        for line in infile:
            line = line.strip()

            if line.startswith("MACRO"):
                # Start of a macro definition
                inside_macro = True
                parts = line.split()
                current_macro_name = parts[1]
                current_macro_params = parts[2:]
                current_macro_def = []
                pp_count = 0
                kp_count = 0
                param_list = []
                # Process parameters for PNTAB and KPTAB
                for param in current_macro_params:
                    if '=' in param:  # Check if there is a default value (Keyword Parameter)
                        kp_count += 1
                        param_name, default_value = param.split('=')
                        kptab.append((param_name, default_value))
                        param_list.append(param_name)
                    else:  # Positional parameter
                        pp_count += 1
                        param_list.append(param)
                pntab[current_macro_name] = param_list

            elif line.startswith("MEND"):
                # End of a macro definition
                inside_macro = False
                macros[current_macro_name] = {
                    "params": current_macro_params,
                    "definition": current_macro_def
                }
                # Add macro definition to MDT
                mdt.extend(current_macro_def)
                mdt.append("MEND")

                # Add entry to MNT
                mnt.append({
                    "name": current_macro_name,
                    "pp_count": pp_count,
                    "kp_count": kp_count,
                    "mdt_pointer": mdt_pointer,
                    "kptab_pointer": kptab_pointer if kp_count > 0 else None
                })

                # Update pointers
                mdt_pointer = len(mdt) + 1
                kptab_pointer = len(kptab) + 1

            elif inside_macro:
                # Store the macro's definition lines
                current_macro_def.append(line)

    # Write the output to the output file (MNT, MDT, KPTAB, PNTAB)
    with open(output_file, "w") as outfile:
        outfile.write("Macro Name Table (MNT):\n")
        outfile.write("Index  Name     #PP  #KP  MDT_P  KPTAB_P\n")
        for i, macro in enumerate(mnt):
            outfile.write(f"{i + 1: <7} {macro["name"]: <8} {macro["pp_count"]: <5} {macro["kp_count"]: <5} {macro["mdt_pointer"]: <7}")
            outfile.write(f"{macro["kptab_pointer"]}\n" if macro["kp_count"] > 0 else "\n")

        outfile.write("\nMacro Definition Table (MDT):\n")
        for i, mdt_entry in enumerate(mdt):
            outfile.write(f"{i + 1: <5} {mdt_entry}\n")

        outfile.write("\nKeyword Parameter Table (KPTAB):\n")
        for i, (param_name, default_value) in enumerate(kptab):
            outfile.write(f"{i + 1: <5} {param_name: <10} {default_value}\n")

        outfile.write("\nParameter Name Table (PNTAB):\n")
        for macro_name, params in pntab.items():
            outfile.write(f"Macro: {macro_name}\n")
            outfile.write("Params: " + ", ".join(params) + "\n")

    print(f"Pass-1 complete. MNT, MDT, KPTAB, and PNTAB written to {output_file}.")

# Example usage
input_file = "/Users/yashraj146/Documents/LP1 Sem 5/Macro/source_code.asm"  # Input file containing the source code
output_file = "/Users/yashraj146/Documents/LP1 Sem 5/Macro/output-mPass1.txt"  # Output file to be used as input to Pass-2

pass1(input_file, output_file)
