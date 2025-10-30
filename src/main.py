from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def main():
    print("NITLang Interpreter - Phase 1: Arithmetic Expressions")
    print("Enter 'exit' to quit\n")
    
    while True:
        try:
            text = input('NITLang> ')
            if text.lower() == 'exit':
                break
            
            if not text.strip():
                continue
            
            # مرحله 1: Lexing
            lexer = Lexer(text)
            tokens = lexer.tokenize()
            # print(f"Tokens: {tokens}")
            
            # مرحله 2: Parsing
            parser = Parser(tokens)
            tree = parser.parse()
            # print(f"AST: {tree}")
            
            # مرحله 3: Interpreting
            interpreter = Interpreter()
            result = interpreter.interpret(tree)
            print(f"Result: {result}\n")
            
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == '__main__':
    main()