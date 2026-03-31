import ast

SUPPORTED_LANGUAGES = ["Python", "C", "C++", "Java", "JavaScript", "SQL"]

def parse_code(code_string: str, language: str = "Python") -> dict:
    """
    Parse and preprocess code.
    For Python: uses AST for proper syntax validation.
    For other languages: basic checks only (AI handles deep analysis).
    """

    if language == "Python":
        return _parse_python(code_string)
    else:
        return _parse_generic(code_string, language)


def _parse_python(code_string: str) -> dict:
    """Full AST-based parsing for Python."""
    try:
        tree = ast.parse(code_string)
    except SyntaxError as e:
        return {
            "success": False,
            "error": {
                "message": str(e.msg),
                "lineno": e.lineno,
            },
            "formatted_code": None,
            "ast_dump": None,
            "tree": None,
        }

    try:
        formatted_code = ast.unparse(tree)
    except AttributeError:
        formatted_code = code_string

    return {
        "success": True,
        "error": None,
        "formatted_code": formatted_code,
        "ast_dump": ast.dump(tree, indent=4),
        "tree": tree,
    }


def _parse_generic(code_string: str, language: str) -> dict:
    """
    Basic validation for non-Python languages.
    We cannot AST-parse these, so we do minimal checks
    and let the AI handle the deep analysis.
    """
    if not code_string.strip():
        return {
            "success": False,
            "error": {
                "message": "No code provided.",
                "lineno": None,
            },
            "formatted_code": None,
            "ast_dump": None,
            "tree": None,
        }

    # Basic bracket balance check
    open_chars  = "({["
    close_chars = ")}]"
    stack = []
    in_string = False
    string_char = None

    for ch in code_string:
        if in_string:
            if ch == string_char:
                in_string = False
        else:
            if ch in ('"', "'"):
                in_string = True
                string_char = ch
            elif ch in open_chars:
                stack.append(ch)
            elif ch in close_chars:
                if not stack:
                    return {
                        "success": False,
                        "error": {
                            "message": f"Unmatched closing bracket '{ch}'.",
                            "lineno": None,
                        },
                        "formatted_code": None,
                        "ast_dump": None,
                        "tree": None,
                    }
                stack.pop()

    if stack:
        return {
            "success": False,
            "error": {
                "message": f"Unclosed bracket '{stack[-1]}'.",
                "lineno": None,
            },
            "formatted_code": None,
            "ast_dump": None,
            "tree": None,
        }

    return {
        "success": True,
        "error": None,
        "formatted_code": code_string,
        "ast_dump": None,
        "tree": None,
    }


if __name__ == "__main__":
    sample = """
def add(a, b):
    return a + b
"""
    result = parse_code(sample, "Python")
    print("Success:", result["success"])