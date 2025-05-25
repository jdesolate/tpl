import eel
from interpreter import CFPLInterpreter

# Initialize Eel
eel.init('web')

# Create interpreter instance
interpreter = CFPLInterpreter()

@eel.expose
def run_cfpl_code(code, input_data=""):
    """Execute CFPL code and return output"""
    try:
        result = interpreter.run(code, input_data)
        return {"success": True, "output": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@eel.expose
def get_variables():
    """Get current variable state"""
    return interpreter.get_variables()

@eel.expose
def reset_interpreter():
    """Reset interpreter state"""
    interpreter.reset()
    return {"success": True, "message": "Interpreter reset successfully"}

if __name__ == '__main__':
    try:
        eel.start('index.html', size=(1200, 800))
    except (SystemExit, MemoryError, KeyboardInterrupt):
        pass
    