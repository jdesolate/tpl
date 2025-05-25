# CFPL Interpreter

A modular interpreter for a Custom Functional Programming Language (CFPL) with a web interface powered by [Eel](https://github.com/ChrisKnott/Eel).

---

## 📁 File Structure

cfpl_interpreter/
├── main.py # Entry point and Eel interface
├── interpreter.py # Main interpreter orchestrator
├── lexer.py # Lexical analyzer (tokenizer)
├── parser.py # Syntax analyzer (AST generator)
├── evaluator.py # AST evaluator/executor
├── token_types.py # Token definitions and types
├── exceptions.py # Custom exception classes
├── config.py # Configuration constants
└── web/ # Web interface files
└── index.html


---

## 🧩 Module Responsibilities

### `token_types.py`
- Defines the `TokenType` enum with all token types
- Implements the `Token` class for token representation  
**Purpose:** Centralized definition of all language tokens

### `lexer.py`
- Contains `CFPLLexer` class
- Responsible for tokenizing source code
- Handles string parsing, number parsing, and identifier recognition  
**Purpose:** Converts raw source code into tokens

### `parser.py`
- Contains `CFPLParser` class
- Implements a recursive descent parser
- Generates the Abstract Syntax Tree (AST)  
**Purpose:** Converts tokens into structured AST

### `evaluator.py`
- Contains `CFPLEvaluator` class
- Executes the AST
- Manages variable state and program execution  
**Purpose:** Executes parsed CFPL programs

### `interpreter.py`
- Contains `CFPLInterpreter` class
- Orchestrates lexer, parser, and evaluator
- Provides a high-level interface for code execution  
**Purpose:** Acts as the main interface for interpreting CFPL code

### `exceptions.py`
- Defines custom exception classes with line number tracking  
**Purpose:** Structured and user-friendly error reporting

### `config.py`
- Holds configuration constants and mappings  
**Purpose:** Centralized and reusable configuration data

### `main.py`
- Entry point of the application
- Sets up the Eel web interface  
**Purpose:** Starts the application and connects UI with the interpreter

---

## 🚀 Key Features

### ✅ Separation of Concerns
- **Lexing**: Pure tokenization logic  
- **Parsing**: Syntax analysis and AST generation  
- **Evaluation**: Program execution and state management  
- **Interface**: Web interface integration via Eel

### ⚠️ Error Handling
- Custom exception hierarchy
- Line number tracking for debugging
- Clear and informative error messages

### 🔧 Maintainability
- Each module has a single responsibility
- Easy to test and debug individual components
- Clean interfaces between system parts

### 🧱 Extensibility
- Add new language features without disrupting structure
- Modular architecture supports scalable enhancements
- Centralized configurations simplify updates

---

## 🛠️ Usage

```python
from interpreter import CFPLInterpreter

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

🧪 Testing Individual Modules
Tokenizer (Lexer)

from lexer import CFPLLexer
lexer = CFPLLexer("VAR x AS INT")
tokens = lexer.tokenize()
print(tokens)

Parser
from parser import CFPLParser
parser = CFPLParser(tokens)
ast = parser.parse_program()
print(ast)

Evaluator
from evaluator import CFPLEvaluator
evaluator = CFPLEvaluator()
result = evaluator.execute_program(ast)
print(result)

🌐 Web Interface
Run the app with:

python main.py
The app will launch a local web interface (index.html) using Eel to run CFPL code.

📜 License
This project is licensed under the MIT License.

🤝 Contributions
Pull requests and suggestions are welcome. Feel free to fork the project and submit a PR.

