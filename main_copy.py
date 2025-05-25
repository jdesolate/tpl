import eel
import re
from typing import Dict, Any, List, Union
from enum import Enum

class TokenType(Enum):
    # Data types
    INT = 'INT'
    CHAR = 'CHAR'
    BOOL = 'BOOL'
    FLOAT = 'FLOAT'
    
    # Keywords
    VAR = 'VAR'
    AS = 'AS'
    START = 'START'
    STOP = 'STOP'
    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'
    IF = 'IF'
    ELSE = 'ELSE'
    WHILE = 'WHILE'
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'
    
    # Operators
    ASSIGN = '='
    PLUS = '+'
    MINUS = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    MODULO = '%'
    GT = '>'
    LT = '<'
    GTE = '>='
    LTE = '<='
    EQ = '=='
    NEQ = '<>'
    
    # Delimiters
    LPAREN = '('
    RPAREN = ')'
    LSQUARE = '['
    RSQUARE = ']'
    COMMA = ','
    AMPERSAND = '&'
    COLON = ':'
    HASH = '#'
    
    # Literals
    INTEGER = 'INTEGER'
    FLOAT_NUM = 'FLOAT_NUM'
    STRING = 'STRING'
    CHARACTER = 'CHARACTER'
    BOOLEAN = 'BOOLEAN'
    
    # Identifiers
    IDENTIFIER = 'IDENTIFIER'
    
    # Special
    NEWLINE = 'NEWLINE'
    EOF = 'EOF'
    COMMENT = 'COMMENT'

class Token:
    def __init__(self, type_: TokenType, value: Any, line: int = 0):
        self.type = type_
        self.value = value
        self.line = line
    
    def __repr__(self):
        return f'Token({self.type}, {self.value})'

class CFPLLexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_line = 1
        self.tokens = []
        self.line_start = True  # Track if we're at the start of a line
        
    def error(self, message: str):
        raise Exception(f"Lexical error at line {self.current_line}: {message}")
    
    def peek(self, offset: int = 0) -> str:
        pos = self.pos + offset
        if pos >= len(self.text):
            return '\0'
        return self.text[pos]
    
    def advance(self) -> str:
        if self.pos < len(self.text):
            char = self.text[self.pos]
            self.pos += 1
            if char == '\n':
                self.current_line += 1
                self.line_start = True
            elif char not in ' \t\r':
                self.line_start = False
            return char
        return '\0'
    
    def skip_whitespace(self):
        while self.peek() in ' \t\r':
            self.advance()
    
    def read_string(self, quote_char: str) -> str:
        value = ''
        self.advance()  # Skip opening quote
        
        while self.peek() != quote_char and self.peek() != '\0':
            if self.peek() == '\n':
                self.error("Unterminated string literal")
            value += self.advance()
        
        if self.peek() == '\0':
            self.error("Unterminated string literal")
        
        self.advance()  # Skip closing quote
        return value
    
    def read_number(self) -> Union[int, float]:
        value = ''
        has_dot = False
        
        while self.peek().isdigit() or self.peek() == '.':
            if self.peek() == '.':
                if has_dot:
                    break
                has_dot = True
            value += self.advance()
        
        return float(value) if has_dot else int(value)
    
    def read_identifier(self) -> str:
        value = ''
        while self.peek().isalnum() or self.peek() == '_':
            value += self.advance()
        return value
    
    def read_comment(self) -> str:
        comment = ''
        while self.peek() != '\n' and self.peek() != '\0':
            comment += self.advance()
        return comment
    
    def tokenize(self) -> List[Token]:
        keywords = {
            'VAR': TokenType.VAR, 'AS': TokenType.AS, 'START': TokenType.START,
            'STOP': TokenType.STOP, 'OUTPUT': TokenType.OUTPUT, 'INPUT': TokenType.INPUT,
            'IF': TokenType.IF, 'ELSE': TokenType.ELSE, 'WHILE': TokenType.WHILE,
            'AND': TokenType.AND, 'OR': TokenType.OR, 'NOT': TokenType.NOT,
            'INT': TokenType.INT, 'CHAR': TokenType.CHAR, 'BOOL': TokenType.BOOL,
            'FLOAT': TokenType.FLOAT, 'TRUE': TokenType.BOOLEAN, 'FALSE': TokenType.BOOLEAN
        }
        
        while self.pos < len(self.text):
            self.skip_whitespace()
            
            if self.peek() == '\0':
                break
            
            # Comments - only at start of line (after whitespace)
            if self.peek() == '*' and self.line_start:
                self.advance()
                comment = self.read_comment()
                self.tokens.append(Token(TokenType.COMMENT, comment, self.current_line))
                continue
            
            # Newlines
            if self.peek() == '\n':
                self.advance()
                self.tokens.append(Token(TokenType.NEWLINE, '\\n', self.current_line - 1))
                continue
            
            # Strings
            if self.peek() == '"':
                string_val = self.read_string('"')
                self.tokens.append(Token(TokenType.STRING, string_val, self.current_line))
                continue
            
            # Characters
            if self.peek() == "'":
                char_val = self.read_string("'")
                if len(char_val) != 1:
                    self.error(f"Character literal must be exactly one character, got: '{char_val}'")
                self.tokens.append(Token(TokenType.CHARACTER, char_val, self.current_line))
                continue
            
            # Numbers
            if self.peek().isdigit():
                num = self.read_number()
                token_type = TokenType.FLOAT_NUM if isinstance(num, float) else TokenType.INTEGER
                self.tokens.append(Token(token_type, num, self.current_line))
                continue
            
            # Multi-character operators
            if self.peek() == '>' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GTE, '>=', self.current_line))
                continue
            
            if self.peek() == '<' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LTE, '<=', self.current_line))
                continue
            
            if self.peek() == '=' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQ, '==', self.current_line))
                continue
            
            if self.peek() == '<' and self.peek(1) == '>':
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NEQ, '<>', self.current_line))
                continue
            
            # Single character tokens
            single_chars = {
                '=': TokenType.ASSIGN, '+': TokenType.PLUS, '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY, '/': TokenType.DIVIDE, '%': TokenType.MODULO,
                '>': TokenType.GT, '<': TokenType.LT, '(': TokenType.LPAREN,
                ')': TokenType.RPAREN, '[': TokenType.LSQUARE, ']': TokenType.RSQUARE,
                ',': TokenType.COMMA, '&': TokenType.AMPERSAND, ':': TokenType.COLON,
                '#': TokenType.HASH
            }
            
            if self.peek() in single_chars:
                char = self.advance()
                self.tokens.append(Token(single_chars[char], char, self.current_line))
                continue
            
            # Identifiers and keywords
            if self.peek().isalpha() or self.peek() == '_':
                identifier = self.read_identifier()
                token_type = keywords.get(identifier.upper(), TokenType.IDENTIFIER)
                value = identifier.upper() == 'TRUE' or identifier.upper() == 'FALSE' if token_type == TokenType.BOOLEAN else identifier
                self.tokens.append(Token(token_type, value, self.current_line))
                continue
            
            # Unknown character
            self.error(f"Unexpected character: '{self.peek()}'")
        
        self.tokens.append(Token(TokenType.EOF, None, self.current_line))
        return self.tokens

class CFPLInterpreter:
    def __init__(self):
        self.variables = {}
        self.tokens = []
        self.pos = 0
        self.output = []
        self.input_queue = []
        
    def error(self, message: str):
        current_token = self.current_token()
        line = current_token.line if current_token else "unknown"
        raise Exception(f"Runtime error at line {line}: {message}")
    
    def current_token(self) -> Token:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return Token(TokenType.EOF, None)
    
    def peek_token(self, offset: int = 1) -> Token:
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return Token(TokenType.EOF, None)
    
    def consume(self, expected_type: TokenType = None) -> Token:
        token = self.current_token()
        if expected_type and token.type != expected_type:
            self.error(f"Expected {expected_type}, got {token.type}")
        self.pos += 1
        return token
    
    def skip_newlines(self):
        while self.current_token().type in [TokenType.NEWLINE, TokenType.COMMENT]:
            self.pos += 1
    
    def parse_program(self, code: str, input_data: str = "") -> str:
        self.variables = {}
        self.output = []
        self.input_queue = input_data.split(',') if input_data.strip() else []
        self.pos = 0
        
        try:
            lexer = CFPLLexer(code)
            self.tokens = lexer.tokenize()
            
            # Parse variable declarations
            self.skip_newlines()
            while self.current_token().type == TokenType.VAR:
                self.parse_variable_declaration()
                self.skip_newlines()
            
            # Parse START block
            if self.current_token().type != TokenType.START:
                self.error("Expected START block")
            
            self.consume(TokenType.START)
            self.skip_newlines()
            
            # Parse statements until STOP
            while self.current_token().type != TokenType.STOP and self.current_token().type != TokenType.EOF:
                if self.current_token().type in [TokenType.NEWLINE, TokenType.COMMENT]:
                    self.pos += 1
                    continue
                self.parse_statement()
                self.skip_newlines()
            
            if self.current_token().type != TokenType.STOP:
                self.error("Expected STOP")
            
            return '\n'.join(self.output)
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def parse_variable_declaration(self):
        self.consume(TokenType.VAR)
        
        # Parse variable list
        variables = []
        while True:
            var_name = self.consume(TokenType.IDENTIFIER).value
            
            # Check for initialization
            initial_value = None
            if self.current_token().type == TokenType.ASSIGN:
                self.consume(TokenType.ASSIGN)
                initial_value = self.parse_literal()
            
            variables.append((var_name, initial_value))
            
            if self.current_token().type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
            else:
                break
        
        # Parse AS type
        self.consume(TokenType.AS)
        var_type = self.consume()
        
        if var_type.type not in [TokenType.INT, TokenType.CHAR, TokenType.BOOL, TokenType.FLOAT]:
            self.error(f"Invalid type: {var_type.value}")
        
        # Initialize variables
        for var_name, initial_value in variables:
            if initial_value is not None:
                self.variables[var_name] = initial_value
            else:
                # Default values
                if var_type.type == TokenType.INT:
                    self.variables[var_name] = 0
                elif var_type.type == TokenType.FLOAT:
                    self.variables[var_name] = 0.0
                elif var_type.type == TokenType.CHAR:
                    self.variables[var_name] = ''
                elif var_type.type == TokenType.BOOL:
                    self.variables[var_name] = False
    
    def parse_literal(self):
        token = self.current_token()
        
        if token.type == TokenType.INTEGER:
            self.pos += 1
            return token.value
        elif token.type == TokenType.FLOAT_NUM:
            self.pos += 1
            return token.value
        elif token.type == TokenType.STRING:
            self.pos += 1
            return token.value
        elif token.type == TokenType.CHARACTER:
            self.pos += 1
            return token.value
        elif token.type == TokenType.BOOLEAN:
            self.pos += 1
            return token.value
        else:
            self.error(f"Expected literal, got {token.type}")
    
    def parse_statement(self):
        token = self.current_token()
        
        if token.type == TokenType.IDENTIFIER:
            self.parse_assignment()
        elif token.type == TokenType.OUTPUT:
            self.parse_output()
        elif token.type == TokenType.INPUT:
            self.parse_input()
        elif token.type == TokenType.IF:
            self.parse_if()
        elif token.type == TokenType.WHILE:
            self.parse_while()
        else:
            self.error(f"Unexpected token: {token.type}")
    
    def parse_assignment(self):
        var_name = self.consume(TokenType.IDENTIFIER).value
        
        if var_name not in self.variables:
            self.error(f"Undefined variable: {var_name}")
        
        self.consume(TokenType.ASSIGN)
        
        # Handle chained assignment (a=b=10)
        if self.peek_token().type == TokenType.ASSIGN:
            next_var = self.consume(TokenType.IDENTIFIER).value
            if next_var not in self.variables:
                self.error(f"Undefined variable: {next_var}")
            self.consume(TokenType.ASSIGN)
            value = self.parse_expression()
            self.variables[var_name] = value
            self.variables[next_var] = value
        else:
            value = self.parse_expression()
            self.variables[var_name] = value
    
    def parse_expression(self):
        return self.parse_or_expression()
    
    def parse_or_expression(self):
        left = self.parse_and_expression()
        
        while self.current_token().type == TokenType.OR:
            self.consume(TokenType.OR)
            right = self.parse_and_expression()
            left = left or right
        
        return left
    
    def parse_and_expression(self):
        left = self.parse_equality_expression()
        
        while self.current_token().type == TokenType.AND:
            self.consume(TokenType.AND)
            right = self.parse_equality_expression()
            left = left and right
        
        return left
    
    def parse_equality_expression(self):
        left = self.parse_relational_expression()
        
        while self.current_token().type in [TokenType.EQ, TokenType.NEQ]:
            op = self.consume().type
            right = self.parse_relational_expression()
            
            if op == TokenType.EQ:
                left = left == right
            else:  # NEQ
                left = left != right
        
        return left
    
    def parse_relational_expression(self):
        left = self.parse_additive_expression()
        
        while self.current_token().type in [TokenType.GT, TokenType.LT, TokenType.GTE, TokenType.LTE]:
            op = self.consume().type
            right = self.parse_additive_expression()
            
            if op == TokenType.GT:
                left = left > right
            elif op == TokenType.LT:
                left = left < right
            elif op == TokenType.GTE:
                left = left >= right
            else:  # LTE
                left = left <= right
        
        return left
    
    def parse_additive_expression(self):
        left = self.parse_multiplicative_expression()
        
        while self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.consume().type
            right = self.parse_multiplicative_expression()
            
            if op == TokenType.PLUS:
                left = left + right
            else:  # MINUS
                left = left - right
        
        return left
    
    def parse_multiplicative_expression(self):
        left = self.parse_unary_expression()
        
        while self.current_token().type in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO]:
            op = self.consume().type
            right = self.parse_unary_expression()
            
            if op == TokenType.MULTIPLY:
                left = left * right
            elif op == TokenType.DIVIDE:
                if right == 0:
                    self.error("Division by zero")
                left = left / right
            else:  # MODULO
                left = left % right
        
        return left
    
    def parse_unary_expression(self):
        if self.current_token().type in [TokenType.PLUS, TokenType.MINUS, TokenType.NOT]:
            op = self.consume().type
            expr = self.parse_unary_expression()
            
            if op == TokenType.PLUS:
                return +expr
            elif op == TokenType.MINUS:
                return -expr
            else:  # NOT
                return not expr
        
        return self.parse_primary_expression()
    
    def parse_primary_expression(self):
        token = self.current_token()
        
        if token.type == TokenType.INTEGER:
            self.pos += 1
            return token.value
        elif token.type == TokenType.FLOAT_NUM:
            self.pos += 1
            return token.value
        elif token.type == TokenType.STRING:
            self.pos += 1
            return token.value
        elif token.type == TokenType.CHARACTER:
            self.pos += 1
            return token.value
        elif token.type == TokenType.BOOLEAN:
            self.pos += 1
            return token.value
        elif token.type == TokenType.IDENTIFIER:
            var_name = self.consume(TokenType.IDENTIFIER).value
            if var_name not in self.variables:
                self.error(f"Undefined variable: {var_name}")
            return self.variables[var_name]
        elif token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN)
            return expr
        else:
            self.error(f"Unexpected token in expression: {token.type}")
    
    def parse_output(self):
        self.consume(TokenType.OUTPUT)
        self.consume(TokenType.COLON)
        
        output_parts = []
        
        while True:
            # Parse expression or concatenation
            if self.current_token().type == TokenType.STRING:
                value = self.consume(TokenType.STRING).value
                # Handle escape sequences
                value = value.replace('[#]', '\n').replace('[[', '[').replace(']]', ']')
                output_parts.append(str(value))
            elif self.current_token().type == TokenType.HASH:
                self.consume(TokenType.HASH)
                output_parts.append('\n')
            else:
                expr = self.parse_expression()
                output_parts.append(str(expr))
            
            if self.current_token().type == TokenType.AMPERSAND:
                self.consume(TokenType.AMPERSAND)
            else:
                break
        
        result = ''.join(output_parts)
        self.output.append(result)
    
    def parse_input(self):
        self.consume(TokenType.INPUT)
        self.consume(TokenType.COLON)
        
        variables = []
        while True:
            var_name = self.consume(TokenType.IDENTIFIER).value
            if var_name not in self.variables:
                self.error(f"Undefined variable: {var_name}")
            variables.append(var_name)
            
            if self.current_token().type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
            else:
                break
        
        # Get input values
        for i, var_name in enumerate(variables):
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
    
    def parse_if(self):
        self.consume(TokenType.IF)
        self.consume(TokenType.LPAREN)
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN)
        self.skip_newlines()
        self.consume(TokenType.START)
        self.skip_newlines()
        
        # Store position for else clause
        if_statements = []
        else_statements = []
        
        # Parse if block
        while self.current_token().type != TokenType.STOP:
            if self.current_token().type in [TokenType.NEWLINE, TokenType.COMMENT]:
                self.pos += 1
                continue
            
            # Store current position and statement
            pos_before = self.pos
            if_statements.append(pos_before)
            self.parse_statement()
            self.skip_newlines()
        
        self.consume(TokenType.STOP)
        self.skip_newlines()
        
        # Check for ELSE
        has_else = self.current_token().type == TokenType.ELSE
        if has_else:
            self.consume(TokenType.ELSE)
            self.skip_newlines()
            self.consume(TokenType.START)
            self.skip_newlines()
            
            # Parse else block
            while self.current_token().type != TokenType.STOP:
                if self.current_token().type in [TokenType.NEWLINE, TokenType.COMMENT]:
                    self.pos += 1
                    continue
                
                pos_before = self.pos
                else_statements.append(pos_before)
                self.parse_statement()
                self.skip_newlines()
            
            self.consume(TokenType.STOP)
        
        # Execute appropriate block
        if condition:
            # Execute if block (already executed during parsing)
            pass
        elif has_else:
            # Execute else block
            for pos in else_statements:
                self.pos = pos
                self.parse_statement()
    
    def parse_while(self):
        self.consume(TokenType.WHILE)
        self.consume(TokenType.LPAREN)
        
        # Store condition position
        condition_pos = self.pos
        condition = self.parse_expression()
        
        self.consume(TokenType.RPAREN)
        self.skip_newlines()
        self.consume(TokenType.START)
        self.skip_newlines()
        
        # Store loop body positions
        body_start = self.pos
        loop_statements = []
        
        while self.current_token().type != TokenType.STOP:
            if self.current_token().type in [TokenType.NEWLINE, TokenType.COMMENT]:
                self.pos += 1
                continue
            loop_statements.append(self.pos)
            self.parse_statement()
            self.skip_newlines()
        
        self.consume(TokenType.STOP)
        
        # Execute while loop
        while condition:
            for pos in loop_statements:
                self.pos = pos
                self.parse_statement()
            
            # Re-evaluate condition
            self.pos = condition_pos
            condition = self.parse_expression()

# Initialize Eel
eel.init('web')

# Create interpreter instance
interpreter = CFPLInterpreter()

@eel.expose
def run_cfpl_code(code, input_data=""):
    """Execute CFPL code and return output"""
    try:
        result = interpreter.parse_program(code, input_data)
        return {"success": True, "output": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@eel.expose
def get_variables():
    """Get current variable state"""
    return interpreter.variables

if __name__ == '__main__':
    try:
        eel.start('index.html', size=(1200, 800))
    except (SystemExit, MemoryError, KeyboardInterrupt):
        pass
    
    