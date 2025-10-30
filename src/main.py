from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def main():
    print("=" * 50)
    print("NITLang Interpreter - Phase 1: Steps 1 & 2")
    print("Features: Arithmetic + Recursive Functions")
    print("=" * 50)
    print("Commands:")
    print("  exit    - Exit the interpreter")
    print("  debug   - Toggle debug mode")
    print("=" * 50)
    print()
    
    interpreter = Interpreter()
    debug_mode = False
    
    while True:
        try:
            text = input('NITLang> ')
            
            if text.lower() == 'exit':
                print("Goodbye!")
                break
            
            if text.lower() == 'debug':
                debug_mode = not debug_mode
                print(f"Debug mode: {'ON' if debug_mode else 'OFF'}")
                continue
            
            if not text.strip():
                continue
            
            # مرحله 1: Lexing
            lexer = Lexer(text)
            tokens = lexer.tokenize()
            if debug_mode:
                print(f"Tokens: {tokens}")
            
            # مرحله 2: Parsing
            parser = Parser(tokens)
            tree = parser.parse()
            if debug_mode:
                print(f"AST: {tree}")
            
            # مرحله 3: Interpreting
            result = interpreter.interpret(tree)
            print(f"=> {result}\n")
            
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit")
        except Exception as e:
            print(f"Error: {e}\n")


def run_file(filename):
    """اجرای یک فایل NITLang"""
    try:
        with open(filename, 'r') as f:
            content = f.read()
        
        interpreter = Interpreter()
        
        # اجرای هر خط
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            try:
                lexer = Lexer(line)
                tokens = lexer.tokenize()
                parser = Parser(tokens)
                tree = parser.parse()
                result = interpreter.interpret(tree)
                print(result)
            except Exception as e:
                print(f"Error in line '{line}': {e}")
    
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        # اجرای فایل
        run_file(sys.argv[1])
    else:
        # حالت REPL
        main()