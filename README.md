# CPL - Configuration Processing Language

A powerful, flexible programming language designed for configuration management and data processing with built-in support for modern development workflows. Features a web-based interpreter interface for easy access and testing.

## 🚀 Features

- **Multi-paradigm Support**: Object-oriented and functional programming capabilities
- **Flexible I/O**: File operations, network communication, and data streaming
- **Error Handling**: Robust exception handling and debugging capabilities
- **Desktop Application**: Built with Eel for seamless Python-JavaScript integration
- **Modern Web Interface**: HTML5, CSS3, and JavaScript frontend
- **Real-time Execution**: Interactive code execution and results display

## 📋 Requirements

- Python 3.7 or higher
- Eel library for Python-JavaScript bridge

## 🛠️ Installation

```bash
git clone https://github.com/yourusername/cpl.git
cd cpl
pip install eel
```

## 🏃 Quick Start

### Running the Application
```bash
python main.py
```
The CPL interpreter will launch in a desktop window powered by Eel.

## 🌐 Desktop Interface

The CPL interpreter features a desktop application built with Eel, combining Python backend processing with a modern web-based frontend:

- **index.html**: Main application interface
- **styles.css**: Modern UI styling
- **cpl-interpreter.js**: Frontend logic and Python integration
- **config.py**: Application configuration

### Application Architecture
CPL uses Eel to create a seamless bridge between Python and JavaScript, allowing:
- Real-time code execution
- Interactive results display
- Modern web UI in a desktop application
- Direct Python-JavaScript communication

## 🛠️ Development

### Project Structure
```
cpl/
├── web/                    # Web interface files
│   ├── index.html         # Main web interface  
│   ├── styles.css         # CSS styling
│   ├── cpl-interpreter.js # Client-side logic
│   └── favicon files      # Browser icons
├── config.py              # Configuration settings
├── evaluator.py           # Expression evaluator
├── exceptions.py          # Error handling
├── interpreter.py         # Core interpreter
├── lexer.py              # Lexical analyzer
├── main.py               # Application entry point
├── parser.py             # Language parser
└── token_types.py        # Token definitions
```

### Core Components

- **main.py**: Application entry point and web server
- **interpreter.py**: Core CPL interpreter logic
- **parser.py**: Parses CPL source code into AST
- **lexer.py**: Tokenizes CPL source code
- **evaluator.py**: Evaluates expressions and executes code
- **exceptions.py**: Custom exception handling
- **token_types.py**: Defines language tokens
- **config.py**: Application configuration

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes with both Python API and web interface
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/cpl/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/cpl/discussions)
- **Documentation**: [Project Wiki](https://github.com/yourusername/cpl/wiki)

## 🗺️ Roadmap

- [ ] Enhanced desktop IDE features (syntax highlighting, autocomplete)
- [ ] Configuration file templates
- [ ] Performance optimizations
- [ ] Extended language features
- [ ] Debugging tools and breakpoints
- [ ] Export/import functionality
- [ ] Plugin system for custom extensions

---

**CPL** - Making configuration management and data processing simple and powerful through an intuitive desktop application.
