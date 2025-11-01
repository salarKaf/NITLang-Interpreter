"""
تست کامل Phase 1 (Steps 1-3)
این فایل همه ویژگی‌های سه گام اول رو با هم تست می‌کنه
"""

import sys
sys.path.insert(0, '..')

import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

def run_complete_test():
    print("="*70)
    print("PHASE 1 COMPLETE TEST - ALL STEPS (1-3)")
    print("="*70)
    print()
    
    interpreter = Interpreter()
    
    print("🚀 Running comprehensive integration test...")
    print()
    
    # Test program combining all features
    test_program = [
        ("Define base value", "let base = 5", None),
        ("Simple arithmetic", "2 + 3 * 4", 14),
        ("Use global variable", "base * 2", 10),
        
        ("Define factorial", "func fact(n) = if n == 0 then 1 else n * #fact(n - 1)", None),
        ("Test factorial", "#fact(5)", 120),
        
        ("Define function with let", "func compute(n) = let doubled = n * 2 in doubled + base", None),
        ("Test function with let", "#compute(10)", 25),
        
        ("Complex let expression", "let x = 10 in let y = 20 in x + y + base", 35),
        
        ("Define recursive with let", "func sum(n) = if n == 0 then 0 else let m = n - 1 in n + #sum(m)", None),
        ("Test recursive with let", "#sum(5)", 15),
        
        ("Nested function calls", "#fact(#sum(3))", 720),
        
        ("Let expression in arithmetic", "(let x = 5 in x * 2) + 10", 20),
        
        ("Check base unchanged", "base", 5),
    ]
    
    passed = 0
    failed = 0
    
    for name, code, expected in test_program:
        print(f"🔹 {name}")
        print(f"   Code: {code}")
        
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            tree = parser.parse()
            result = interpreter.interpret(tree)
            
            print(f"   Result: {result}")
            
            if expected is not None:
                if result == expected:
                    print(f"   ✅ PASS")
                    passed += 1
                else:
                    print(f"   ❌ FAIL (Expected: {expected})")
                    failed += 1
            else:
                print(f"   ✅ OK")
                passed += 1
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            failed += 1
        
        print()
    
    # Summary
    print("="*70)
    print(f"FINAL RESULTS: {passed}/{passed + failed} tests passed")
    if failed == 0:
        print("🎉🎉🎉 ALL PHASE 1 TESTS PASSED! 🎉🎉🎉")
        print()
        print("✅ Step 1: Arithmetic Expressions - COMPLETE")
        print("✅ Step 2: Functions & Recursion - COMPLETE")
        print("✅ Step 3: Scope Management - COMPLETE")
        print()
        print("🚀 Phase 1 is ready! You can move to Phase 2!")
    else:
        print(f"⚠️  {failed} test(s) failed")
    print("="*70)

if __name__ == '__main__':
    run_complete_test()