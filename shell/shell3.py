import re

class CFPLInterpreter:
    def __init__(self):
        self.variables = {}
        self.types = {}
        self.output = []

    def run(self, code):
        lines = self.preprocess(code)
        self.execute(lines)

    def preprocess(self, code):
        lines = code.splitlines()
        clean_lines = []
        for line in lines:
            line = line.strip()
            if line.startswith("*") or not line:
                continue
            clean_lines.append(line)
        return clean_lines

    def execute(self, lines):
        in_program = False

        for line in lines:
            if line == "START":
                in_program = True
            elif line == "STOP":
                in_program = False
            elif not in_program:
                self.declare_variables(line)
            else:
                self.process_statement(line)

    def declare_variables(self, line):
        match = re.match(r"VAR (.+) AS (\w+)", line)
        if not match:
            raise SyntaxError(f"Invalid variable declaration: {line}")

        var_section, var_type = match.groups()
        for var_decl in var_section.split(","):
            if "=" in var_decl:
                var_name, var_value = map(str.strip, var_decl.split("="))
                self.variables[var_name] = self.parse_value(var_value, var_type)
            else:
                var_name = var_decl.strip()
                self.variables[var_name] = None
            self.types[var_name] = var_type

    def parse_value(self, value, var_type):
        if var_type == "INT":
            return int(value)
        elif var_type == "CHAR":
            return value.strip("'")
        elif var_type == "BOOL":
            return value.upper() == "TRUE"
        elif var_type == "FLOAT":
            return float(value)
        else:
            raise TypeError(f"Unsupported type: {var_type}")

    def process_statement(self, line):
        if line.startswith("OUTPUT:"):
            self.handle_output(line[7:].strip())
        elif "=" in line:
            self.assign_value(line)
        else:
            raise SyntaxError(f"Invalid statement: {line}")

    def handle_output(self, expression):
        output = self.evaluate_expression(expression)
        self.output.append(output)
        print(output)

    def assign_value(self, line):
        var_name, expression = map(str.strip, line.split("=", 1))
        if var_name not in self.variables:
            raise NameError(f"Variable '{var_name}' is not declared")
        value = self.evaluate_expression(expression)
        self.variables[var_name] = value

    def evaluate_expression(self, expression):
        expression = re.sub(r"\[(.*?)\]", lambda m: m.group(1).replace("#", "\n"), expression)
        tokens = re.split(r"(&|\+|-|\*|/|%|==|<>|>=|<=|>|<)", expression)
        tokens = [self.resolve_token(token.strip()) for token in tokens]

        try:
            return eval("".join(map(str, tokens)))
        except Exception as e:
            raise ValueError(f"Error evaluating expression '{expression}': {e}")

    def resolve_token(self, token):
        if token in self.variables:
            return self.variables[token]
        if re.match(r"^-?\d+(\.\d+)?$", token):
            return float(token) if "." in token else int(token)
        if token.startswith("'") and token.endswith("'"):
            return token.strip("'")
        if token.upper() == "TRUE":
            return True
        if token.upper() == "FALSE":
            return False
        return token

# Example usage
cfpl_code = """
* my first program in CFPL
VAR abc, b, c AS INT
VAR x, w_23='w' AS CHAR
VAR t="TRUE" AS BOOL

START
abc=b=10
w_23='a'

OUTPUT: abc & "hi" & b & "#" & w_23 & "[#]"
STOP
"""

interpreter = CFPLInterpreter()
interpreter.run(cfpl_code)
