# tpl
Programming language

CFPL Interpreter - Modular Structure
This document outlines the modular structure of the CFPL (Custom Programming Language) interpreter.
File Structure
cfpl_interpreter/
├── main.py              # Entry point and Eel interface
├── interpreter.py       # Main interpreter orchestrator
├── lexer.py            # Lexical analyzer (tokenizer)
├── parser.py           # Syntax analyzer (AST generator)
├── evaluator.py        # AST evaluator/executor
├── token_types.py      # Token definitions and types
├── exceptions.py       # Custom exception classes
├── config.py          # Configuration constants
└── web/               # Web interface files
    └── index.html
Module Responsibilities
1. token_types.py

Defines TokenType enum with all token types
Implements Token class for token representation
Purpose: Central definition of all language tokens

2. lexer.py

Contains CFPLLexer class
Responsible for tokenizing source code
Handles string parsing, number parsing, identifier recognition
Purpose: Converts raw source code into tokens

3. parser.py

Contains CFPLParser class
Implements recursive descent parser
Generates Abstract Syntax Tree (AST)
Purpose: Converts tokens into structured AST

4. evaluator.py

Contains CFPLEvaluator class
Executes the AST
Manages variable state and program execution
Purpose: Actually runs the parsed program

5. interpreter.py

Contains CFPLInterpreter class
Orchestrates lexer, parser, and evaluator
Provides high-level interface for code execution
Purpose: Main interface for running CFPL code

6. exceptions.py

Custom exception classes for better error handling
Includes line number information
Purpose: Structured error reporting

7. config.py

Configuration constants and settings
Default values and mappings
Purpose: Centralized configuration

8. main.py

Entry point of the application
Eel web interface setup
Purpose: Application startup and web interface

Key Improvements
Separation of Concerns

Lexing: Pure tokenization logic
Parsing: Syntax analysis and AST generation
Evaluation: Program execution and state management
Interface: Web interface and user interaction

Error Handling

Custom exception hierarchy
Line number tracking
Better error messages

Maintainability

Each module has a single responsibility
Easy to test individual components
Clear interfaces between modules

Extensibility

Easy to add new language features
Modular design allows selective enhancement
Configuration externalized

Usage
pythonfrom interpreter import CFPLInterpreter

# Create interpreter instance
interpreter = CFPLInterpreter()

# Run CFPL code
code = """
VAR x AS INT
START
    OUTPUT: "Hello World"
STOP
"""

result = interpreter.run(code)
print(result)  # Output: Hello World
Testing Individual Modules
Each module can be tested independently:
python# Test lexer
from lexer import CFPLLexer
lexer = CFPLLexer("VAR x AS INT")
tokens = lexer.tokenize()

# Test parser  
from parser import CFPLParser
parser = CFPLParser(tokens)
ast = parser.parse_program()

# Test evaluator
from evaluator import CFPLEvaluator
evaluator = CFPLEvaluator()
result = evaluator.execute_program(ast)