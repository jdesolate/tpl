from typing import List
from token_types import Token, TokenType

class CFPLParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def error(self, message: str):
        current_token = self.current_token()
        line = current_token.line if current_token else "unknown"
        raise Exception(f"Parse error at line {line}: {message}")
    
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
    
    def parse_expression(self):
        return self.parse_or_expression()
    
    def parse_or_expression(self):
        left = self.parse_and_expression()
        
        while self.current_token().type == TokenType.OR:
            self.consume(TokenType.OR)
            right = self.parse_and_expression()
            left = ('or', left, right)
        
        return left
    
    def parse_and_expression(self):
        left = self.parse_equality_expression()
        
        while self.current_token().type == TokenType.AND:
            self.consume(TokenType.AND)
            right = self.parse_equality_expression()
            left = ('and', left, right)
        
        return left
    
    def parse_equality_expression(self):
        left = self.parse_relational_expression()
        
        while self.current_token().type in [TokenType.EQ, TokenType.NEQ]:
            op = self.consume().type
            right = self.parse_relational_expression()
            left = (op.value, left, right)
        
        return left
    
    def parse_relational_expression(self):
        left = self.parse_additive_expression()
        
        while self.current_token().type in [TokenType.GT, TokenType.LT, TokenType.GTE, TokenType.LTE]:
            op = self.consume().type
            right = self.parse_additive_expression()
            left = (op.value, left, right)
        
        return left
    
    def parse_additive_expression(self):
        left = self.parse_multiplicative_expression()
        
        while self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.consume().type
            right = self.parse_multiplicative_expression()
            left = (op.value, left, right)
        
        return left
    
    def parse_multiplicative_expression(self):
        left = self.parse_unary_expression()
        
        while self.current_token().type in [TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO]:
            op = self.consume().type
            right = self.parse_unary_expression()
            left = (op.value, left, right)
        
        return left
    
    def parse_unary_expression(self):
        if self.current_token().type in [TokenType.PLUS, TokenType.MINUS, TokenType.NOT]:
            op = self.consume().type
            expr = self.parse_unary_expression()
            return (op.value, expr)
        
        return self.parse_primary_expression()
    
    def parse_primary_expression(self):
        token = self.current_token()
        
        if token.type in [TokenType.INTEGER, TokenType.FLOAT_NUM, TokenType.STRING, 
                         TokenType.CHARACTER, TokenType.BOOLEAN]:
            self.pos += 1
            return token.value
        elif token.type == TokenType.IDENTIFIER:
            var_name = self.consume(TokenType.IDENTIFIER).value
            return ('var', var_name)
        elif token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            expr = self.parse_expression()
            self.consume(TokenType.RPAREN)
            return expr
        else:
            self.error(f"Unexpected token in expression: {token.type}")
    
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
        
        return ('var_decl', variables, var_type.type)
    
    def parse_assignment(self):
        var_name = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.ASSIGN)
        
        # Handle chained assignment (a=b=10)
        if self.peek_token().type == TokenType.ASSIGN:
            next_var = self.consume(TokenType.IDENTIFIER).value
            self.consume(TokenType.ASSIGN)
            value = self.parse_expression()
            return ('chain_assign', [var_name, next_var], value)
        else:
            value = self.parse_expression()
            return ('assign', var_name, value)
    
    def parse_output(self):
        self.consume(TokenType.OUTPUT)
        self.consume(TokenType.COLON)
        
        output_parts = []
        
        while True:
            if self.current_token().type == TokenType.STRING:
                value = self.consume(TokenType.STRING).value
                output_parts.append(('string', value))
            elif self.current_token().type == TokenType.HASH:
                self.consume(TokenType.HASH)
                output_parts.append(('newline',))
            else:
                expr = self.parse_expression()
                output_parts.append(('expr', expr))
            
            if self.current_token().type == TokenType.AMPERSAND:
                self.consume(TokenType.AMPERSAND)
            else:
                break
        
        return ('output', output_parts)
    
    def parse_input(self):
        self.consume(TokenType.INPUT)
        self.consume(TokenType.COLON)
        
        variables = []
        while True:
            var_name = self.consume(TokenType.IDENTIFIER).value
            variables.append(var_name)
            
            if self.current_token().type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
            else:
                break
        
        return ('input', variables)
    
    def parse_if(self):
        self.consume(TokenType.IF)
        self.consume(TokenType.LPAREN)
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN)
        self.skip_newlines()
        self.consume(TokenType.START)
        self.skip_newlines()
        
        # Parse if block
        if_statements = []
        while self.current_token().type != TokenType.STOP:
            if self.current_token().type in [TokenType.NEWLINE, TokenType.COMMENT]:
                self.pos += 1
                continue
            if_statements.append(self.parse_statement())
            self.skip_newlines()
        
        self.consume(TokenType.STOP)
        self.skip_newlines()
        
        # Check for ELSE
        else_statements = []
        if self.current_token().type == TokenType.ELSE:
            self.consume(TokenType.ELSE)
            self.skip_newlines()
            self.consume(TokenType.START)
            self.skip_newlines()
            
            while self.current_token().type != TokenType.STOP:
                if self.current_token().type in [TokenType.NEWLINE, TokenType.COMMENT]:
                    self.pos += 1
                    continue
                else_statements.append(self.parse_statement())
                self.skip_newlines()
            
            self.consume(TokenType.STOP)
        
        return ('if', condition, if_statements, else_statements)
    
    def parse_while(self):
        self.consume(TokenType.WHILE)
        self.consume(TokenType.LPAREN)
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN)
        self.skip_newlines()
        self.consume(TokenType.START)
        self.skip_newlines()
        
        # Parse loop body
        statements = []
        while self.current_token().type != TokenType.STOP:
            if self.current_token().type in [TokenType.NEWLINE, TokenType.COMMENT]:
                self.pos += 1
                continue
            statements.append(self.parse_statement())
            self.skip_newlines()
        
        self.consume(TokenType.STOP)
        return ('while', condition, statements)
    
    def parse_statement(self):
        token = self.current_token()
        
        if token.type == TokenType.IDENTIFIER:
            return self.parse_assignment()
        elif token.type == TokenType.OUTPUT:
            return self.parse_output()
        elif token.type == TokenType.INPUT:
            return self.parse_input()
        elif token.type == TokenType.IF:
            return self.parse_if()
        elif token.type == TokenType.WHILE:
            return self.parse_while()
        else:
            self.error(f"Unexpected token: {token.type}")
    
    def parse_program(self):
        statements = []
        
        # Parse variable declarations
        self.skip_newlines()
        while self.current_token().type == TokenType.VAR:
            statements.append(self.parse_variable_declaration())
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
            statements.append(self.parse_statement())
            self.skip_newlines()
        
        if self.current_token().type != TokenType.STOP:
            self.error("Expected STOP")
        
        return ('program', statements)
      