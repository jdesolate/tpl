# CPL - Configuration Processing Language

A powerful, flexible programming language designed for configuration management and data processing with built-in support for modern development workflows.

## 🚀 Features

- **Multi-paradigm Support**: Object-oriented and functional programming capabilities
- **Built-in HTTP Client**: Native support for REST API interactions and web requests
- **Advanced String Processing**: Comprehensive string manipulation and pattern matching
- **JSON Integration**: First-class JSON parsing, manipulation, and generation
- **Flexible I/O**: File operations, network communication, and data streaming
- **Error Handling**: Robust exception handling and debugging capabilities
- **Cross-platform**: Runs on Windows, macOS, and Linux

## 📋 Requirements

- Python 3.7 or higher
- Required dependencies (see `requirements.txt`)

## 🛠️ Installation

### Quick Install
```bash
git clone https://github.com/yourusername/cpl.git
cd cpl
pip install -r requirements.txt
```

### Development Setup
```bash
git clone https://github.com/yourusername/cpl.git
cd cpl
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

## 🏃 Quick Start

### Create an Interpreter Instance
```python
from cpl import CPLInterpreter

interpreter = CPLInterpreter()
```

### Run CPL Code
```python
# Execute CPL code directly
result = interpreter.execute('print("Hello, CPL!")')

# Run from file
interpreter.run_file('example.cpl')
```

### Basic CPL Syntax Examples

**Variables and Data Types:**
```cpl
name = "CPL"
version = 1.0
features = ["http", "json", "strings"]
```

**HTTP Requests:**
```cpl
response = http.get("https://api.github.com/users/octocat")
user_data = json.parse(response.body)
print("User: " + user_data.name)
```

**String Processing:**
```cpl
text = "Hello, World!"
result = text.upper().replace("WORLD", "CPL")
```

## 📖 Language Features

### HTTP Client
```cpl
# GET request
response = http.get("https://api.example.com/data")

# POST with JSON
data = {"key": "value"}
response = http.post("https://api.example.com/create", json=data)

# Custom headers
headers = {"Authorization": "Bearer token123"}
response = http.get("https://api.example.com/secure", headers=headers)
```

### JSON Operations
```cpl
# Parse JSON string
data = json.parse('{"name": "John", "age": 30}')

# Generate JSON
person = {"name": "Jane", "age": 25}
json_string = json.stringify(person)
```

### String Manipulation
```cpl
text = "The quick brown fox"
words = text.split(" ")
result = text.contains("quick")  # true
formatted = text.format_template({"animal": "fox"})
```

### File Operations
```cpl
# Read file
content = file.read("config.txt")

# Write file
file.write("output.txt", "Hello, CPL!")

# Check if file exists
if file.exists("config.json") {
    config = json.parse(file.read("config.json"))
}
```

## 🧪 Testing

### Run All Tests
```bash
python -m pytest tests/
```

### Test Specific Components
```bash
# Test parser
python -m pytest tests/test_parser.py

# Test evaluator
python -m pytest tests/test_evaluator.py

# Test HTTP functionality
python -m pytest tests/test_http.py
```

## 📚 Documentation

- [Language Reference](docs/language-reference.md)
- [API Documentation](docs/api.md)
- [Examples](examples/)
- [Contributing Guide](CONTRIBUTING.md)

## 🛠️ Development

### Project Structure
```
cpl/
├── src/
│   ├── interpreter/     # Core interpreter logic
│   ├── parser/         # Language parser
│   ├── evaluator/      # Expression evaluator
│   └── stdlib/         # Standard library
├── tests/              # Test suite
├── examples/           # Example CPL programs
└── docs/              # Documentation
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`python -m pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/cpl/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/cpl/discussions)
- **Documentation**: [Wiki](https://github.com/yourusername/cpl/wiki)

## 🗺️ Roadmap

- [ ] Package manager integration
- [ ] IDE extensions (VS Code, Vim)
- [ ] Performance optimizations
- [ ] Extended standard library
- [ ] Debugging tools
- [ ] Language server protocol support

---

**CPL** - Making configuration management and data processing simple and powerful.