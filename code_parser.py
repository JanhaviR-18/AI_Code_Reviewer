import ast

def parse_code(code_string: str) -> dict:
    """
    Parse and preprocess Python code using AST.
    """

    try:
        tree = ast.parse(code_string)

    except SyntaxError as e:
        return {
            "success": False,
            "error": f"Syntax Error: {e}",
            "line": e.lineno,
            "formatted_code": None,
            "ast_dump": None
        }

    # Try formatting code
    try:
        formatted_code = ast.unparse(tree)
    except AttributeError:
        formatted_code = code_string

    ast_structure = ast.dump(tree, indent=4)

    return {
        "success": True,
        "error": None,
        "formatted_code": formatted_code,
        "ast_dump": ast_structure
    }


# Demo run
if __name__ == "__main__":

    sample_code = """
import math

class Demo:
    pass

def add(a, b):
    return a + b
"""

    result = parse_code(sample_code)

    if not result["success"]:
        print("Error found:")
        print(result["error"])
    else:
        print("Code parsed successfully!\n")

        print("Formatted Code:")
        print(result["formatted_code"])

        print("\nAST Dump:")
        print(result["ast_dump"])