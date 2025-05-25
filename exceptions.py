# Custom exceptions for CFPL Interpreter

class CFPLError(Exception):
    """Base exception class for CFPL interpreter"""
    def __init__(self, message: str, line_number: int = None):
        self.message = message
        self.line_number = line_number
        super().__init__(self.format_message())
    
    def format_message(self):
        if self.line_number:
            return f"Line {self.line_number}: {self.message}"
        return self.message

class LexicalError(CFPLError):
    """Exception raised for lexical analysis errors"""
    def __init__(self, message: str, line_number: int = None):
        super().__init__(f"Lexical error: {message}", line_number)

class ParseError(CFPLError):
    """Exception raised for parsing errors"""
    def __init__(self, message: str, line_number: int = None):
        super().__init__(f"Parse error: {message}", line_number)

class RuntimeError(CFPLError):
    """Exception raised for runtime errors"""
    def __init__(self, message: str, line_number: int = None):
        super().__init__(f"Runtime error: {message}", line_number)

class UndefinedVariableError(RuntimeError):
    """Exception raised when accessing undefined variables"""
    def __init__(self, variable_name: str, line_number: int = None):
        super().__init__(f"Undefined variable: '{variable_name}'", line_number)

class TypeMismatchError(RuntimeError):
    """Exception raised for type mismatch errors"""
    def __init__(self, expected_type: str, actual_type: str, line_number: int = None):
        super().__init__(f"Type mismatch: expected {expected_type}, got {actual_type}", line_number)

class DivisionByZeroError(RuntimeError):
    """Exception raised for division by zero"""
    def __init__(self, line_number: int = None):
        super().__init__("Division by zero", line_number)

class InvalidInputError(RuntimeError):
    """Exception raised for invalid input"""
    def __init__(self, message: str, line_number: int = None):
        super().__init__(f"Invalid input: {message}", line_number)
        