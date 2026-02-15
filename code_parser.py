import ast


def parse_code(code_string: str) -> dict:
    """
    Parse and preprocess Python code using AST.
    """

    # 1️⃣ Syntax check + parsing
    try:
        tree = ast.parse(code_string)
    except SyntaxError as e:
        return {
            "success": False,
            "error": f"Syntax Error: {e}",
            "line": e.lineno,
        }

    # 2️⃣ Preprocess / format code
    formatted_code = ast.unparse(tree)

    # 3️⃣ Extract simple structure
    functions = []
    classes = []
    imports = []

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)

        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            for alias in node.names:
                imports.append(f"{module}.{alias.name}")

    return {
        "success": True,
        "formatted_code": formatted_code,
        "imports": imports,
        "functions": functions,
        "classes": classes,
    }


# 🔹 Demo run
if __name__ == "__main__":
    sample_code = """
import math

class Demo:
    pass

def add(a, b):
    return a + b
"""

    result = parse_code(sample_code)
    print(result)
