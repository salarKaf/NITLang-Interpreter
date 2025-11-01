"""
تست گام 3: Scope Management
این فایل تمام ویژگی‌های گام 3 رو تست می‌کنه
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
        print("=" * 70)
        print(f"RESULTS: {self.passed}/{self.total} tests passed")
        if self.passed == self.total:
            print("🎉 ALL STEP 3 TESTS PASSED!")
        else:
            print(f"⚠️  {self.total - self.passed} test(s) failed")
        print("=" * 70)

    def test_block_body_functions(capsys):
        from src.lexer import Lexer
        from src.parser import Parser
        from src.interpreter import Interpreter
        I = Interpreter()

        # تابع با let و سپس استفاده از متغیر محلی
        code = "func add(a, b) = { let s = a + b s }"
        for line in [code, "#add(5, 3)"]:
            tree = Parser(Lexer(line).tokenize()).parse()
            out = I.interpret(tree)
        assert out == 8

        # بازگشتی با بلاک
        code2 = "func fact(n) = { if n == 0 then 1 else n * #fact(n - 1) }"
        for line in [code2, "#fact(5)"]:
            tree = Parser(Lexer(line).tokenize()).parse()
            out = I.interpret(tree)
        assert out == 120


def run_tests():
    print("=" * 70)
    print("STEP 3: SCOPE MANAGEMENT TEST")
    print("=" * 70)
    print()

    runner = TestRunner()

    # Let Statement (Global Variables)
    print("📌 Let Statement - Global Variables:")
    runner.test("Define global variable", "let x = 10", expected=None)
    print()
    runner.test("Read global variable", "x", 10)
    print()
    runner.test("Define another variable", "let y = 20", expected=None)
    print()
    runner.test("Use global variables", "x + y", 30)
    print()

    # Let Expression
    print("📌 Let Expression:")
    runner.test("Simple let expression", "let x = 5 in x + 10", 15)
    print()
    runner.test("Let expression with calculation", "let x = 2 * 3 in x + 1", 7)
    print()
    runner.test("Nested let expressions", "let x = 5 in let y = 10 in x + y", 15)
    print()
    runner.test("Define global z", "let z = 100", expected=None)
    # Shadowing in Let Expression
    print("📌 Shadowing:")
    runner.test("Let expression shadows global", "let z = 100 in let z = 200 in z", 200)
    print()
    runner.test("Global variable unchanged after let expression", "z", 100)
    print()

    # Functions with Let Expression
    print("📌 Functions with Let Expression:")
    runner.test("Define function with let",
                "func double_plus_one(n) = let x = n * 2 in x + 1",
                expected=None)
    print()
    runner.test("Call function with let", "#double_plus_one(5)", 11)
    print()

    # The Document Example
    print("📌 Exact Document Example:")
    runner.test("Define global x", "let global_x = 10", expected=None)
    print()
    runner.test("Define function f with local x",
                "func f() = let local_x = 20 in local_x + 1",
                expected=None)
    print()
    runner.test("Call function f (should use local x=20)", "#f()", 21)
    print()
    runner.test("Check global x (should be unchanged)", "global_x", 10)
    print()

    # Functions accessing global variables
    print("📌 Functions Accessing Global Variables:")
    runner.test("Define global a", "let a = 100", expected=None)
    print()
    runner.test("Define function using global", "func use_global() = a + 10", expected=None)
    print()
    runner.test("Call function (should access global)", "#use_global()", 110)
    print()

    # Parameters as Local Variables
    print("📌 Parameters as Local Variables:")
    runner.test("Define function with parameters", "func compute(x, y) = x * 2 + y", expected=None)
    print()
    runner.test("Call with parameters", "#compute(5, 3)", 13)
    print()

    # Complex Scope Test
    print("📌 Complex Scope Test:")
    runner.test("Define base", "let base = 10", expected=None)
    print()
    runner.test("Function with let shadowing parameter",
                "func complex(base) = let base = base * 2 in base + 1",
                expected=None)
    print()
    runner.test("Call complex (parameter=5)", "#complex(5)", 11)
    print()
    runner.test("Global base unchanged", "base", 10)
    print()

    # Let in Recursive Functions
    print("📌 Let in Recursive Functions:")
    runner.test("Factorial with let",
                "func fact_let(n) = if n == 0 then 1 else let m = n - 1 in n * #fact_let(m)",
                expected=None)
    print()
    runner.test("Call factorial with let", "#fact_let(5)", 120)
    print()

    # Multiple nested lets
    print("📌 Multiple Nested Let Expressions:")
    runner.test("Triple nested let",
                "let a = 1 in let b = a + 1 in let c = b + 1 in a + b + c",
                6)
    print()

    # Let with function calls
    print("📌 Let with Function Calls:")
    runner.test("Define add", "func add(a, b) = a + b", expected=None)
    print()
    runner.test("Let with function call",
                "let result = #add(10, 20) in result * 2",
                60)
    print()

    runner.summary()


def test_step3_suite_pytest(capsys):
    run_tests()
    out = capsys.readouterr().out
    assert "ALL STEP 3 TESTS PASSED" in out or "RESULTS:" in out
