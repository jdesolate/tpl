from typing import List, Union
from token_types import Token, TokenType

class CFPLLexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_line = 1
        self.tokens = []
        
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
            
            # Comments
            if self.peek() == '*':
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
      