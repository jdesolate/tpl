DIGITS = "0123456789"

# Symbol Table to store variables and their values
class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, var_names, var_type):
        for name in var_names:
            if name in self.symbols:
                raise Exception(f"Variable '{name}' already declared.")
            self.symbols[name] = {"type": var_type, "value": None}

    def assign(self, var_name, value):
        if var_name not in self.symbols:
            raise Exception(f"Variable '{var_name}' not declared.")
        var_type = self.symbols[var_name]["type"]
        # Type checking
        if var_type == "INT" and not isinstance(value, int):
            raise Exception(f"Type mismatch: expected INT, got {type(value).__name__}.")
        elif var_type == "CHAR" and not (isinstance(value, str) and len(value) == 1):
            raise Exception(f"Type mismatch: expected CHAR, got {type(value).__name__}.")
        elif var_type == "BOOL" and not isinstance(value, bool):
            raise Exception(f"Type mismatch: expected BOOL, got {type(value).__name__}.")
        elif var_type == "FLOAT" and not isinstance(value, float):
            raise Exception(f"Type mismatch: expected FLOAT, got {type(value).__name__}.")
        self.symbols[var_name]["value"] = value

    def get(self, var_name):
        if var_name not in self.symbols:
            raise Exception(f"Variable '{var_name}' not declared.")
        return self.symbols[var_name]["value"]

# CFPL Interpreter
class Interpreter:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.inside_program = False

    def interpret_line(self, line):
        line = line.strip()
        if line.startswith("*"):  # Skip comments
            return
        if line == "START":
            self.inside_program = True
            return
        if line == "STOP":
            self.inside_program = False
            print("Program execution completed.")
            return

        if not self.inside_program:
            self.handle_declaration(line)
        else:
            self.handle_execution(line)

    def handle_declaration(self, line):
        if line.startswith("VAR"):
            parts = line.split(" AS ")
            var_names = parts[0].replace("VAR", "").strip().split(", ")
            var_type = parts[1].strip()
            self.symbol_table.declare(var_names, var_type)

    def handle_execution(self, line):
        if "=" in line:
            self.handle_assignment(line)
        elif line.startswith("OUTPUT:"):
            self.handle_output(line.replace("OUTPUT:", "").strip())

    def handle_assignment(self, line):
        parts = line.split("=")
        values = [part.strip() for part in parts]

        # Evaluate the last value in the chain
        try:
            value = eval(values[-1])  # Simplified; assumes valid input
        except NameError as e:
            raise Exception(f"Undefined variable or invalid expression: {e}")

        # Assign values to all variables in the chain
        for var_name in reversed(values[:-1]):
            if var_name not in self.symbol_table.symbols:
                raise Exception(f"Variable '{var_name}' not declared.")
            self.symbol_table.assign(var_name, value)

    def handle_output(self, line):
        parts = line.split("&")
        result = ""
        for part in parts:
            part = part.strip()
            if part.startswith('"') and part.endswith('"'):
                result += part[1:-1]
            elif part.startswith("'") and part.endswith("'"):
                result += part[1:-1]
            elif part == "#":
                result += "\n"
            elif part in self.symbol_table.symbols:
                result += str(self.symbol_table.get(part))
            else:
                raise Exception(f"Unknown output part: {part}")
        print(result)

# Main function
def main():
    print("Welcome to the CFPL Interpreter!")
    print("Type your CFPL code line by line. Type 'STOP' to finish the program.\n")

    interpreter = Interpreter()

    while True:
        try:
            line = input("> ")  # Take user input
            interpreter.interpret_line(line)
            if line.strip() == "STOP":
                break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()