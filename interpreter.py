from lexer import CFPLLexer
from parser import CFPLParser
from evaluator import CFPLEvaluator

class CFPLInterpreter:
    def __init__(self):
        self.evaluator = CFPLEvaluator()
    
    def run(self, code: str, input_data: str = "") -> str:
        """
        Execute CFPL code and return output
        """
        try:
            # Tokenize
            lexer = CFPLLexer(code)
            tokens = lexer.tokenize()
            
            # Parse
            parser = CFPLParser(tokens)
            ast = parser.parse_program()
            
            # Evaluate
            result = self.evaluator.execute_program(ast, input_data)
            
            return result
            
        except Exception as e:
            raise Exception(f"Interpreter error: {str(e)}")
    
    def get_variables(self):
        """Get current variable state"""
        return self.evaluator.variables.copy()
    
    def reset(self):
        """Reset interpreter state"""
        self.evaluator = CFPLEvaluator()
        