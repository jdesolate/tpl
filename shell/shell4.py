class CFPLInterpreter:
    def __init__(self):
        self.variables = {}

    def parse_line(self, line):
        line = line.strip()
        if line.startswith('*') or not line:
            return  # Ignore comments and empty lines
        if line.startswith("VAR"):
            self.declare_variables(line)
        elif line.startswith("OUTPUT:"):
            return self.handle_output(line)
        elif line.startswith("START"):
            return self.execute_block()
        elif line.startswith("STOP"):
            return  # End of execution block
        else:
            self.execute_statement(line)

    def declare_variables(self, line):
        # Example: VAR abc, b, c AS INT
        declarations = line[4:].split(',')
        for declaration in declarations:
            name, var_type = declaration.split('AS')
            name = name.strip()
            var_type = var_type.strip()
            if '=' in name:
                name, value = name.split('=')
                name = name.strip()
                value = value.strip()
                self.variables[name] = self.cast_value(value, var_type)
            else:
                self.variables[name.strip()] = None  # Declare without initialization

    def cast_value(self, value, var_type):
        value = value.strip().strip('"').strip("'")
        if var_type == "INT":
            return int(value)
        elif var_type == "FLOAT":
            return float(value)
        elif var_type == "BOOL":
            return value == "TRUE"
        elif var_type == "CHAR":
            return value[0] if value else None
        return None

    def execute_statement(self, line):
        # Evaluate the statement and assign values
        if '=' in line:
            var_name, expression = line.split('=')
            var_name = var_name.strip()
            self.variables[var_name] = self.evaluate_expression(expression.strip())

    def evaluate_expression(self, expression):
        # Simple evaluation of expressions (arithmetic and logical)
        # This can be expanded to handle more complex expressions
        try:
            return eval(expression, {}, self.variables)
        except Exception as e:
            print(f"Error evaluating expression: {e}")
            return None

    def handle_output(self, line):
        # Example: OUTPUT: abc & "hi" & b & "#" & w_23 & "[#]"
        output_expr = line[7:].strip()
        output_value = self.evaluate_expression(output_expr)
        print(output_value)

    def execute_block(self):
        # Placeholder for executing a block of code
        pass

    def run(self):
        print("CFPL Interpreter. Type 'exit' to quit.")
        while True:
            code = input(">>> ")
            if code.lower() == 'exit':
                break
            for line in code.splitlines():
                self.parse_line(line)

if __name__ == "__main__":
    interpreter = CFPLInterpreter()
    interpreter.run()
    