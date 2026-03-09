import ast
import re
class AIReviewer(ast.NodeVisitor):

    def __init__(self):
        self.defined = set()
        self.used = set()
        self.imports = set()
        self.issues = []

    # ------------------ IMPORTS ------------------

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.asname or alias.name.split('.')[0])
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.add(alias.asname or alias.name)
        self.generic_visit(node)

    # ------------------ CLASS ------------------

    def visit_ClassDef(self, node):

        # Naming convention: PascalCase
        if not node.name[0].isupper():
            self.issues.append({
                "type": "Naming Convention",
                "line": node.lineno,
                "message": f"Class '{node.name}' should follow PascalCase naming."
            })

        self.generic_visit(node)

    # ------------------ FUNCTIONS ------------------

    def visit_FunctionDef(self, node):
        self.defined.add(node.name)

        # Function arguments are defined variables
        for arg in node.args.args:
            self.defined.add(arg.arg)

        # -------- Naming Convention --------
        if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
            self.issues.append({
                "type": "Naming Convention",
                "line": node.lineno,
                "message": f"Function '{node.name}' should follow snake_case naming."
            })

        # -------- Function Length Check --------
        if hasattr(node, "end_lineno"):
            function_length = node.end_lineno - node.lineno

            if function_length > 40:
                self.issues.append({
                    "type": "Function Too Long",
                    "line": node.lineno,
                    "message": f"Function '{node.name}' is {function_length} lines long. Consider splitting it."
                })

        # -------- Recursion Detection --------
        function_name = node.name
        recursive_call = False

        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name) and child.func.id == function_name:
                    recursive_call = True

        if recursive_call:
            has_if = any(isinstance(n, ast.If) for n in ast.walk(node))
            if not has_if:
                self.issues.append({
                    "type": "Infinite Recursion",
                    "line": node.lineno,
                    "message": "Recursive function without a clear base condition."
                })

        self.generic_visit(node)

    # ------------------ VARIABLES ------------------

    def visit_Name(self, node):

        if isinstance(node.ctx, ast.Store):

            self.defined.add(node.id)

            # Naming Convention for variables
            if not re.match(r'^[a-z_][a-z0-9_]*$', node.id):
                self.issues.append({
                    "type": "Naming Convention",
                    "line": node.lineno,
                    "message": f"Variable '{node.id}' should follow snake_case naming."
                })

        elif isinstance(node.ctx, ast.Load):
            self.used.add(node.id)

        self.generic_visit(node)

    # ------------------ WHILE LOOP ------------------

    def visit_While(self, node):

        # Case 1: while True without break
        if isinstance(node.test, ast.Constant) and node.test.value is True:
            has_break = any(isinstance(n, ast.Break) for n in ast.walk(node))
            if not has_break:
                self.issues.append({
                    "type": "Infinite Loop",
                    "line": node.lineno,
                    "message": "Detected 'while True' without a break statement."
                })

        # Case 2: condition variable not updated
        if isinstance(node.test, ast.Compare):

            variables = [
                child.id for child in ast.walk(node.test)
                if isinstance(child, ast.Name)
            ]

            updated = False

            for stmt in node.body:
                for child in ast.walk(stmt):

                    if isinstance(child, (ast.Assign, ast.AugAssign)):

                        target = child.target if isinstance(child, ast.AugAssign) else child.targets[0]

                        if isinstance(target, ast.Name) and target.id in variables:
                            updated = True

            if variables and not updated:
                self.issues.append({
                    "type": "Possible Infinite Loop",
                    "line": node.lineno,
                    "message": "Loop condition variable is not updated inside the loop."
                })

        self.generic_visit(node)

    # ------------------ FOR LOOP ------------------

    def visit_For(self, node):

        if isinstance(node.iter, ast.Call):

            if isinstance(node.iter.func, ast.Name) and node.iter.func.id == "iter":

                self.issues.append({
                    "type": "Possible Infinite Loop",
                    "line": node.lineno,
                    "message": "Loop may iterate over an infinite iterator."
                })

        self.generic_visit(node)

    # ------------------ FINAL ANALYSIS ------------------

    def analyze(self):
        import builtins

        undefined_vars = self.used - self.defined - set(dir(__builtins__))
        unused_vars = self.defined - self.used
        unused_imports = self.imports - self.used

        results = []

        for var in undefined_vars:
            results.append({
                "type": "Undefined Variable",
                "message": f"Variable '{var}' is used before being defined."
            })

        for var in unused_vars:
            results.append({
                "type": "Unused Variable",
                "message": f"Variable '{var}' is defined but never used."
            })

        for imp in unused_imports:
            results.append({
                "type": "Unused Import",
                "message": f"Module '{imp}' is imported but never used."
            })

        results.extend(self.issues)

        return results


def detect_errors(code: str):

    try:
        tree = ast.parse(code)

    except SyntaxError as e:
        return [{
            "type": "Syntax Error",
            "message": str(e)
        }]

    reviewer = AIReviewer()
    reviewer.visit(tree)

    return reviewer.analyze()