# Configuration file for CFPL Interpreter

# Default values for different data types
DEFAULT_VALUES = {
    'INT': 0,
    'FLOAT': 0.0,
    'CHAR': '',
    'BOOL': False
}

# Keywords mapping
KEYWORDS = {
    'VAR': 'VAR', 'AS': 'AS', 'START': 'START',
    'STOP': 'STOP', 'OUTPUT': 'OUTPUT', 'INPUT': 'INPUT',
    'IF': 'IF', 'ELSE': 'ELSE', 'WHILE': 'WHILE',
    'AND': 'AND', 'OR': 'OR', 'NOT': 'NOT',
    'INT': 'INT', 'CHAR': 'CHAR', 'BOOL': 'BOOL',
    'FLOAT': 'FLOAT', 'TRUE': 'TRUE', 'FALSE': 'FALSE'
}

# Single character tokens
SINGLE_CHAR_TOKENS = {
    '=': 'ASSIGN', '+': 'PLUS', '-': 'MINUS',
    '*': 'MULTIPLY', '/': 'DIVIDE', '%': 'MODULO',
    '>': 'GT', '<': 'LT', '(': 'LPAREN',
    ')': 'RPAREN', '[': 'LSQUARE', ']': 'RSQUARE',
    ',': 'COMMA', '&': 'AMPERSAND', ':': 'COLON',
    '#': 'HASH'
}

# Multi-character operators
MULTI_CHAR_OPERATORS = {
    '>=': 'GTE',
    '<=': 'LTE', 
    '==': 'EQ',
    '<>': 'NEQ'
}

# Escape sequences for strings
ESCAPE_SEQUENCES = {
    '[#]': '\n',
    '[[': '[',
    ']]': ']'
}

# Application settings
APP_SETTINGS = {
    'WINDOW_SIZE': (1200, 800),
    'HTML_FILE': 'index.html',
    'WEB_FOLDER': 'web'
}
