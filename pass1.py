class Assembler:
    def __init__(self):
        self.symbol_table = {}
        self.literal_table = {}
        self.intermediate_code = []
        self.location_counter = 0
        self.mot = self.create_mot()

    def create_mot(self):
        return {
            'ORIGIN': ('AD','03',1),
            'STOP': ('IS', '00',1),
            'ADD': ('IS', '01',1),
            'SUB': ('IS', '02',1),
            'MULT': ('IS', '03',1),
            'MOVER': ('IS', '04',1),
            'MOVEM': ('IS', '05',1),
            'COMP': ('IS', '06',1),
            'BC': ('IS', '07',1),
            'DIV': ('IS', '08',1),
            'READ': ('IS', '09',1),
            'PRINT': ('IS', '10',1),
            'START': ('AD', '01',1),
            'END': ('AD', '02',1),            
            'EQU': ('AD', '04',1),
            'LTORG': ('AD', '05',1),
            'DC': ('DL', '01',1),
            'DS': ('DL', '02',1),
        }

    def read_input(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
        return lines

    def parse_line(self, line):
        parts = line.split()
        label, opcode, operands = None, None, []

        if len(parts) == 4:
            label, opcode, operands = parts[0], parts[1], parts[2:]
        elif len(parts) == 3:
            if parts[1] in self.mot:
                label, opcode, operands = parts[0], parts[1], parts[2:]
            else:
                opcode, operands = parts[0], parts[1:]
        elif len(parts) == 2:
            if parts[0] in self.mot:
                opcode, operands = parts[0], parts[1:]
            else:
                label, opcode = parts[0], parts[1]
        elif len(parts) == 1:
            opcode = parts[0]

        return label, opcode, operands

    def process_line(self, label, opcode, operands):
        if label:
            if label not in self.symbol_table:
                self.symbol_table[label] = self.location_counter
            else:
                raise ValueError(f"Duplicate symbol: {label}")

        if opcode == 'START':
            self.location_counter = int(operands[0])
        elif opcode == 'END':
            self.process_literals()
            return
        elif opcode == 'LTORG':
            self.process_literals()
        else:
            if operands:
                for operand in operands:
                    if operand.startswith('='):
                        if operand not in self.literal_table:
                            self.literal_table[operand] = -1

            if opcode in self.mot:
                opcode_info = self.mot[opcode]
                self.intermediate_code.append((self.location_counter, label, opcode_info, operands))
                self.location_counter += opcode_info[2]
            else:
                self.intermediate_code.append((self.location_counter, label, opcode, operands))
                self.location_counter += 1

    def process_literals(self):
        for literal in list(self.literal_table.keys()):
            if self.literal_table[literal] == -1:
                self.literal_table[literal] = self.location_counter
                self.intermediate_code.append((self.location_counter, None, ('DL', '02', 1), literal))
                self.location_counter += 1

    def write_output(self, filename):
        with open(filename, 'w') as file:
            file.write("Intermediate Code:\n")
            for line in self.intermediate_code:
                file.write(f"{line}\n")
            file.write("\nSymbol Table:\n")
            for symbol, address in self.symbol_table.items():
                file.write(f"{symbol}: {address}\n")
            file.write("\nLiteral Table:\n")
            for literal, address in self.literal_table.items():
                file.write(f"{literal}: {address}\n")

    def assemble(self, input_file, output_file):
        lines = self.read_input(input_file)
        for line in lines:
            label, opcode, operands = self.parse_line(line.strip())
            self.process_line(label, opcode, operands)
        self.write_output(output_file)

if __name__ == "__main__":
    assembler = Assembler()
    assembler.assemble("/Users/yashraj146/Documents/LP1 Sem 5/Assember Python/input.asm",
                        "/Users/yashraj146/Documents/LP1 Sem 5/Assember Python/output.txt")