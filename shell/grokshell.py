variables = {}

def declare_variable(name, type_str, value=None):
    if type_str == "INT":
        variables[name] = int(value) if value and value.isdigit() else 0
    elif type_str == "CHAR":
        variables[name] = str(value)[0] if value else ''
    elif type_str == "BOOL":
        variables[name] = value.upper() == "TRUE" if isinstance(value, str) else bool(value)
    elif type_str == "FLOAT":
        variables[name] = float(value) if value and value.replace('.', '').isdigit() else 0.0

def parse_expression(expression):
    if '&' in expression:  # String concatenation
        return ''.join([str(variables.get(part.strip(), part)) for part in expression.split('&')])
    elif expression in variables:
        return variables[expression]
    else:
        return eval(expression, {"__builtins__": None}, variables)

def execute_line(line):
    if 'OUTPUT:' in line:
        output = parse_expression(line.split('OUTPUT:')[1].strip())
        print(output if '\n' not in str(output) else output.replace('\n', '#'))
    elif '=' in line:
        parts = line.split('=')  # Split by '='
        value = parts.pop().strip()  # Last part is the value
        vars_to_assign = [part.strip() for part in parts]  # All but last are variables
        result = parse_expression(value)
        for var in reversed(vars_to_assign):  # Assign right to left for multiple assignments
            variables[var] = result

def run_block(lines, start, stop):
    i = start
    while i < stop:
        if lines[i].startswith('*'):
            i += 1
            continue
        if 'IF' in lines[i]:
            condition = lines[i].split('(')[1].split(')')[0]
            if parse_expression(condition):
                if_start = i + 1
                if_stop = next((j for j in range(if_start, len(lines)) if lines[j].strip() == 'STOP'), None)
                if if_stop:
                    run_block(lines, if_start, if_stop)
                    i = if_stop  # Skip to after the STOP of this block
                else:
                    raise SyntaxError("Mismatched IF structure: Missing STOP")
            else:
                i = next((j for j in range(i, len(lines)) if lines[j].strip() == 'STOP'), i)
        elif 'WHILE' in lines[i]:
            while_start = i
            condition = lines[i].split('(')[1].split(')')[0]
            while parse_expression(condition):
                while_body_start = i + 1
                while_body_stop = next((j for j in range(while_body_start, len(lines)) if lines[j].strip() == 'STOP'), None)
                if while_body_stop:
                    run_block(lines, while_body_start, while_body_stop)
                    i = while_body_start - 1  # Reset i to recheck the condition
                else:
                    raise SyntaxError("Mismatched WHILE structure: Missing STOP")
                condition = lines[while_start].split('(')[1].split(')')[0]  # Re-fetch condition in case it changed
            i = next((j for j in range(i, len(lines)) if lines[j].strip() == 'STOP'), i)
        else:
            execute_line(lines[i])
        i += 1

def run_program(lines):
    start = next((i for i, line in enumerate(lines) if line.strip() == 'START'), None)
    stop = next((i for i, line in enumerate(lines) if line.strip() == 'STOP'), None)
    if start is not None and stop is not None:
        run_block(lines, start + 1, stop)

def interpret_cfpl(code):
    lines = code.split('\n')
    for line in lines:
        if line.strip().startswith('VAR'):
            parts = line.split()
            type_str = parts[-1]
            var_names = parts[1].split(',')
            for name in var_names:
                value = None
                if '=' in line:
                    eq_pos = line.find('=')
                    value_part = line[eq_pos+1:].strip()
                    if value_part.startswith('"') or value_part.startswith("'"):  # For CHAR or STRING
                        value = value_part[1:-1]  # Remove quotes
                    else:
                        value = value_part.split(',')[0]  # Get first value if multiple are declared
                declare_variable(name.strip(), type_str, value)
    
    run_program(lines)

# Example usage
sample_code = """
VAR abc, b, c AS INT
VAR $x, w_2 23='$w$' AS CHAR
VAR $t="RUE" AS BOOL
START
    abc = b = 10
    w_23 = 'a'
    OUTPUT: abc & "hi" & b & "#" & w_23 & "[#]"
STOP
"""

interpret_cfpl(sample_code)