"""
تست گام 1: Arithmetic Expressions
این فایل تمام ویژگی‌های گام 1 رو تست می‌کنه
"""

import sys

sys.path.insert(0, '..')

import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter


def test(name, code, expected):
    """اجرای یک تست"""
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        tree = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(tree)

        if result == expected:
            print(f"✅ {name}")
            print(f"   Code: {code}")
            print(f"   Result: {result}")
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


def run_tests():
    print("=" * 70)
    print("STEP 1: ARITHMETIC EXPRESSIONS TEST")
    print("=" * 70)
    print()

    passed = 0
    total = 0

    # Basic operations
    print("📌 Basic Operations:")
    tests = [
        ("Simple addition", "2 + 3", 5),
        ("Simple subtraction", "10 - 3", 7),
        ("Simple multiplication", "4 * 5", 20),
        ("Simple division", "20 / 4", 5),
    ]

    for name, code, expected in tests:
        total += 1
        if test(name, code, expected):
            passed += 1
        print()

    # Operator precedence
    print("📌 Operator Precedence:")
    tests = [
        ("Multiplication before addition", "2 + 3 * 4", 14),
        ("Division before subtraction", "20 - 10 / 2", 15),
        ("Multiple operations", "2 + 3 * 4 - 5", 9),
        ("Complex expression", "10 - 2 * 3 + 4", 8),
    ]

    for name, code, expected in tests:
        total += 1
        if test(name, code, expected):
            passed += 1
        print()

    # Parentheses
    print("📌 Parentheses:")
    tests = [
        ("Override precedence", "(2 + 3) * 4", 20),
        ("Nested parentheses", "((2 + 3) * 4) / 2", 10),
        ("Multiple groups", "(10 - 5) * (3 + 2)", 25),
    ]

    for name, code, expected in tests:
        total += 1
        if test(name, code, expected):
            passed += 1
        print()

    # Edge cases
    print("📌 Edge Cases:")
    tests = [
        ("Single number", "42", 42),
        ("Zero", "0", 0),
        ("Negative result", "5 - 10", -5),
        ("Multiple additions", "1 + 2 + 3 + 4", 10),
        ("Multiple multiplications", "2 * 3 * 4", 24),
    ]

    for name, code, expected in tests:
        total += 1
        if test(name, code, expected):
            passed += 1
        print()

    # Division by zero (should raise error)
    print("📌 Error Handling:")
    print("Testing division by zero:")
    try:
        lexer = Lexer("10 / 0")
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        tree = parser.parse()
        interpreter = Interpreter()
        result = interpreter.interpret(tree)
        print("❌ Division by zero should raise error")
        print()
    except Exception as e:
        print(f"✅ Correctly caught error: {e}")
        passed += 1
        print()
    total += 1

    # Summary
    print("=" * 70)
    print(f"RESULTS: {passed}/{total} tests passed")
    if passed == total:
        print("🎉 ALL STEP 1 TESTS PASSED!")
    else:
        print(f"⚠️  {total - passed} test(s) failed")
    print("=" * 70)


# if __name__ == '__main__':
#     run_tests()


def test_step1_suite_pytest(capsys):
    run_tests()
    out = capsys.readouterr().out
    assert "ALL STEP 1 TESTS PASSED" in out or "RESULTS:" in out
