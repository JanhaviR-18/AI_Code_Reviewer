from code_parser import parse_code
from error_detector import detect_errors
from ai_suggester import get_ai_suggestion


def main():

    # ---------------- USER CODE INPUT ----------------
    user_code = """
import os

x = 5

while True:
    print("Hello")

def fun():
    return fun()
"""

    # ---------------- STEP 1: PARSE CODE ----------------
    parse_result = parse_code(user_code)

    if not parse_result["success"]:
        print("❌ Syntax Error Found:")
        print(parse_result["error"])
        return

    print("✅ Syntax Check Passed\n")

    # ---------------- STEP 2: STATIC ERROR DETECTION ----------------
    detected_errors = detect_errors(user_code)

    print("🔍 Detected Issues:")
    for err in detected_errors:
        print(err)

    # ---------------- STEP 3: AI SUGGESTIONS ----------------
    print("\n🤖 Generating AI Suggestions...\n")

    ai_feedback = get_ai_suggestion(user_code, detected_errors)

    print("----- AI FEEDBACK -----")
    print(ai_feedback)


if __name__ == "__main__":
    main()