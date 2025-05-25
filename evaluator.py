from typing import Any, Dict, List
from token_types import TokenType

class CFPLEvaluator:
    def __init__(self):
        self.variables = {}
        self.output = []
        self.input_queue = []
    
    def error(self, message: str):
        raise Exception(f"Runtime error: {message}")
    
    def evaluate_expression(self, expr):
        if isinstance(expr, (int, float, str, bool)):
            return expr
        
        if isinstance(expr, tuple):
            op = expr[0]
            
            if op == 'var':
                var_name = expr[1]
                if var_name not in self.variables:
                    self.error(f"Undefined variable: {var_name}")
                return self.variables[var_name]
            
            elif op == 'or':
                left = self.evaluate_expression(expr[1])
                right = self.evaluate_expression(expr[2])
                return left or right
            
            elif op == 'and':
                left = self.evaluate_expression(expr[1])
                right = self.evaluate_expression(expr[2])
                return left and right
            
            elif op == '==':
                left = self.evaluate_expression(expr[1])
                right = self.evaluate_expression(expr[2])
                return left == right
            
            elif op == '<>':
                left = self.evaluate_expression(expr[1])
                right = self.evaluate_expression(expr[2])
                return left != right
            
            elif op == '>':
                left = self.evaluate_expression(expr[1])
                right = self.evaluate_expression(expr[2])
                return left > right
            
            elif op == '<':
                left = self.evaluate_expression(expr[1])
                right = self.evaluate_expression(expr[2])
                return left < right
            
            elif op == '>=':
                left = self.evaluate_expression(expr[1])
                right = self.evaluate_expression(expr[2])
                return left >= right
            
            elif op == '<=':
                left = self.evaluate_expression(expr[1])
                right = self.evaluate_expression(expr[2])
                return left <= right
            
            elif op == '+':
                if len(expr) == 2:  # Unary plus
                    return +self.evaluate_expression(expr[1])
                else:  # Binary plus
                    left = self.evaluate_expression(expr[1])
                    right = self.evaluate_expression(expr[2])
                    return left + right
            
            elif op == '-':
                if len(expr) == 2:  # Unary minus
                    return -self.evaluate_expression(expr[1])
                else:  # Binary minus
                    left = self.evaluate_expression(expr[1])
                    right = self.evaluate_expression(expr[2])
                    return left - right
            
            elif op == '*':
                left = self.evaluate_expression(expr[1])
                right = self.evaluate_expression(expr[2])
                return left * right
            
            elif op == '/':
                left = self.evaluate_expression(expr[1])
                right = self.evaluate_expression(expr[2])
                if right == 0:
                    self.error("Division by zero")
                return left / right
            
            elif op == '%':
                left = self.evaluate_expression(expr[1])
                right = self.evaluate_expression(expr[2])
                return left % right
            
            elif op == 'NOT':
                return not self.evaluate_expression(expr[1])
        
        self.error(f"Unknown expression: {expr}")
    
    def execute_statement(self, stmt):
        if not isinstance(stmt, tuple):
            return
        
        op = stmt[0]
        
        if op == 'var_decl':
            variables, initial_values, var_type = stmt[1], stmt[1], stmt[2]
            
            for var_name, initial_value in variables:
                if initial_value is not None:
                    self.variables[var_name] = initial_value
                else:
                    # Default values
                    if var_type == TokenType.INT:
                        self.variables[var_name] = 0
                    elif var_type == TokenType.FLOAT:
                        self.variables[var_name] = 0.0
                    elif var_type == TokenType.CHAR:
                        self.variables[var_name] = ''
                    elif var_type == TokenType.BOOL:
                        self.variables[var_name] = False
        
        elif op == 'assign':
            var_name = stmt[1]
            value_expr = stmt[2]
            
            if var_name not in self.variables:
                self.error(f"Undefined variable: {var_name}")
            
            value = self.evaluate_expression(value_expr)
            self.variables[var_name] = value
        
        elif op == 'chain_assign':
            var_names = stmt[1]
            value_expr = stmt[2]
            
            for var_name in var_names:
                if var_name not in self.variables:
                    self.error(f"Undefined variable: {var_name}")
            
            value = self.evaluate_expression(value_expr)
            for var_name in var_names:
                self.variables[var_name] = value
        
        elif op == 'output':
            output_parts = stmt[1]
            result_parts = []
            
            for part in output_parts:
                if part[0] == 'string':
                    value = part[1]
                    # Handle escape sequences
                    value = value.replace('[#]', '\n').replace('[[', '[').replace(']]', ']')
                    result_parts.append(str(value))
                elif part[0] == 'newline':
                    result_parts.append('\n')
                elif part[0] == 'expr':
                    expr_value = self.evaluate_expression(part[1])
                    result_parts.append(str(expr_value))
            
            result = ''.join(result_parts)
            self.output.append(result)
        
        elif op == 'input':
            variables = stmt[1]
            
            for i, var_name in enumerate(variables):
                if var_name not in self.variables:
                    self.error(f"Undefined variable: {var_name}")
                
                if i < len(self.input_queue):
                    value = self.input_queue[i].strip()
                    # Try to convert to appropriate type
                    try:
                        if '.' in value:
                            self.variables[var_name] = float(value)
                        else:
                            self.variables[var_name] = int(value)
                    except ValueError:
                        if value.upper() in ['TRUE', 'FALSE']:
                            self.variables[var_name] = value.upper() == 'TRUE'
                        elif len(value) == 1:
                            self.variables[var_name] = value
                        else:
                            self.variables[var_name] = value
                else:
                    self.error(f"Not enough input values provided for variable: {var_name}")
        
        elif op == 'if':
            condition = stmt[1]
            if_statements = stmt[2]
            else_statements = stmt[3]
            
            if self.evaluate_expression(condition):
                for statement in if_statements:
                    self.execute_statement(statement)
            else:
                for statement in else_statements:
                    self.execute_statement(statement)
        
        elif op == 'while':
            condition = stmt[1]
            statements = stmt[2]
            
            while self.evaluate_expression(condition):
                for statement in statements:
                    self.execute_statement(statement)
    
    def execute_program(self, ast, input_data: str = ""):
        self.variables = {}
        self.output = []
        self.input_queue = input_data.split(',') if input_data.strip() else []
        
        if ast[0] == 'program':
            statements = ast[1]
            for statement in statements:
                self.execute_statement(statement)
        
        return '\n'.join(self.output)
      