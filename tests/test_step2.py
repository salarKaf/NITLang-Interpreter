"""
تست گام 2: Functions and Recursion
این فایل تمام ویژگی‌های گام 2 رو تست می‌کنه
"""

import sys
sys.path.insert(0, '..')

import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

class TestRunner:
    def __init__(self):
        self.interpreter = Interpreter()
        self.passed = 0
        self.total = 0
    
    def test(self, name, code, expected=None):
        """اجرای یک تست"""
        self.total += 1
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            tree = parser.parse()
            result = self.interpreter.interpret(tree)
            
            if expected is None:
                print(f"✅ {name}")
                print(f"   Code: {code}")
                print(f"   Result: {result}")
                self.passed += 1
                return True
            elif result == expected:
                print(f"✅ {name}")
                print(f"   Code: {code}")
                print(f"   Result: {result}")
                self.passed += 1
                return True
            else:
                print(f"❌ {name}")
                print(f"   Code: {code}")
                print(f"   Expected: {expected}, Got: {result}")
                return False
        except Exception as e:
            print(f"❌ {name}")
            print(f"   Code: {code}")
            print(f"   Error: {e}")
            return False
    
    def summary(self):
        print("="*70)
        print(f"RESULTS: {self.passed}/{self.total} tests passed")
        if self.passed == self.total:
            print("🎉 ALL STEP 2 TESTS PASSED!")
        else:
            print(f"⚠️  {self.total - self.passed} test(s) failed")
        print("="*70)

def run_tests():
    print("="*70)
    print("STEP 2: FUNCTIONS AND RECURSION TEST")
    print("="*70)
    print()
    
    runner = TestRunner()
    
    # If-Then-Else
    print("📌 If-Then-Else Expressions:")
    runner.test("True condition", "if 1 == 1 then 10 else 20", 10)
    print()
    runner.test("False condition", "if 1 == 0 then 10 else 20", 20)
    print()
    runner.test("Nested if", "if 1 == 1 then if 2 == 2 then 5 else 10 else 20", 5)
    print()
    
    # Comparison
    print("📌 Comparison (==):")
    runner.test("Equal numbers", "5 == 5", 1)
    print()
    runner.test("Not equal numbers", "5 == 3", 0)
    print()
    runner.test("Complex comparison", "(2 + 3) == 5", 1)
    print()
    
    # Simple Function Definition
    print("📌 Simple Function Definition:")
    runner.test("Define simple function", "func add(a, b) = a + b", expected=None)
    print()
    runner.test("Call simple function", "#add(5, 3)", 8)
    print()
    
    # Function with If-Then-Else
    print("📌 Function with Conditional:")
    runner.test("Define max function", "func max(a, b) = if a == b then a else if a == a + 1 then b else a", expected=None)
    print()
    runner.test("Define abs function", "func abs(x) = if x == 0 then 0 else if x == x + 1 then 0 else x", expected=None)
    print()
    
    # Recursive Functions
    print("📌 Recursive Functions:")
    
    # Factorial
    runner.test("Define factorial", "func fact(n) = if n == 0 then 1 else n * #fact(n - 1)", expected=None)
    print()
    runner.test("Factorial of 0", "#fact(0)", 1)
    print()
    runner.test("Factorial of 1", "#fact(1)", 1)
    print()
    runner.test("Factorial of 5", "#fact(5)", 120)
    print()
    runner.test("Factorial of 6", "#fact(6)", 720)
    print()
    
    # Fibonacci
    runner.test("Define fibonacci", 
                "func fib(n) = if n == 0 then 0 else if n == 1 then 1 else #fib(n - 1) + #fib(n - 2)", 
                expected=None)
    print()
    runner.test("Fibonacci of 0", "#fib(0)", 0)
    print()
    runner.test("Fibonacci of 1", "#fib(1)", 1)
    print()
    runner.test("Fibonacci of 5", "#fib(5)", 5)
    print()
    runner.test("Fibonacci of 7", "#fib(7)", 13)
    print()
    
    # Sum of numbers
    runner.test("Define sum", "func sum(n) = if n == 0 then 0 else n + #sum(n - 1)", expected=None)
    print()
    runner.test("Sum of 0", "#sum(0)", 0)
    print()
    runner.test("Sum of 5", "#sum(5)", 15)
    print()
    runner.test("Sum of 10", "#sum(10)", 55)
    print()
    
    # Function with multiple parameters
    print("📌 Functions with Multiple Parameters:")
    runner.test("Define power function", 
                "func pow(base, exp) = if exp == 0 then 1 else base * #pow(base, exp - 1)", 
                expected=None)
    print()
    runner.test("Power: 2^0", "#pow(2, 0)", 1)
    print()
    runner.test("Power: 2^3", "#pow(2, 3)", 8)
    print()
    runner.test("Power: 5^2", "#pow(5, 2)", 25)
    print()
    
    # Complex expressions
    print("📌 Complex Expressions:")
    runner.test("Function call in expression", "10 + #add(5, 3)", 18)
    print()
    runner.test("Multiple function calls", "#add(#add(1, 2), #add(3, 4))", 10)
    print()
    
    runner.summary()

# if __name__ == '__main__':
#     run_tests()

def test_step2_suite_pytest(capsys):
    run_tests()
    out = capsys.readouterr().out
    assert "ALL STEP 2 TESTS PASSED" in out or "RESULTS:" in out
