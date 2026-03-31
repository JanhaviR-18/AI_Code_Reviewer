import ast
import re


# ── Python AST-based reviewer ──────────────────────────────────────────────

class AIReviewer(ast.NodeVisitor):

    def __init__(self):
        self.defined = set()
        self.used    = set()
        self.imports = set()
        self.issues  = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.asname or alias.name.split('.')[0])
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        if not node.name[0].isupper():
            self.issues.append({
                "type": "Naming Convention",
                "line": node.lineno,
                "message": f"Class '{node.name}' should follow PascalCase naming.",
            })
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.defined.add(node.name)
        for arg in node.args.args:
            self.defined.add(arg.arg)

        if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
            self.issues.append({
                "type": "Naming Convention",
                "line": node.lineno,
                "message": f"Function '{node.name}' should follow snake_case naming.",
            })

        if hasattr(node, "end_lineno"):
            length = node.end_lineno - node.lineno
            if length > 40:
                self.issues.append({
                    "type": "Function Too Long",
                    "line": node.lineno,
                    "message": f"Function '{node.name}' is {length} lines long. Consider splitting it.",
                })

        fn = node.name
        has_call = any(
            isinstance(c, ast.Call)
            and isinstance(c.func, ast.Name)
            and c.func.id == fn
            for c in ast.walk(node)
        )
        if has_call and not any(isinstance(n, ast.If) for n in ast.walk(node)):
            self.issues.append({
                "type": "Infinite Recursion",
                "line": node.lineno,
                "message": "Recursive function without a clear base condition.",
            })

        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.defined.add(node.id)
            if not re.match(r'^[a-z_][a-z0-9_]*$', node.id):
                self.issues.append({
                    "type": "Naming Convention",
                    "line": node.lineno,
                    "message": f"Variable '{node.id}' should follow snake_case naming.",
                })
        elif isinstance(node.ctx, ast.Load):
            self.used.add(node.id)
        self.generic_visit(node)

    def visit_While(self, node):
        if isinstance(node.test, ast.Constant) and node.test.value is True:
            if not any(isinstance(n, ast.Break) for n in ast.walk(node)):
                self.issues.append({
                    "type": "Infinite Loop",
                    "line": node.lineno,
                    "message": "Detected 'while True' without a break statement.",
                })

        if isinstance(node.test, ast.Compare):
            variables = [
                c.id for c in ast.walk(node.test)
                if isinstance(c, ast.Name)
            ]
            updated = any(
                isinstance(c, (ast.Assign, ast.AugAssign))
                and isinstance(
                    getattr(c, 'target', None) or
                    (c.targets[0] if hasattr(c, 'targets') else None),
                    ast.Name
                )
                and (
                    getattr(c, 'target', ast.Name(id='__none__')).id in variables
                    if hasattr(c, 'target')
                    else c.targets[0].id in variables
                )
                for stmt in node.body
                for c in ast.walk(stmt)
            )
            if variables and not updated:
                self.issues.append({
                    "type": "Possible Infinite Loop",
                    "line": node.lineno,
                    "message": "Loop condition variable is not updated inside the loop.",
                })

        self.generic_visit(node)

    def visit_For(self, node):
        if (
            isinstance(node.iter, ast.Call)
            and isinstance(node.iter.func, ast.Name)
            and node.iter.func.id == "iter"
        ):
            self.issues.append({
                "type": "Possible Infinite Loop",
                "line": node.lineno,
                "message": "Loop may iterate over an infinite iterator.",
            })
        self.generic_visit(node)

    def analyze(self):
        undefined  = self.used - self.defined - set(dir(__builtins__))
        unused_var = self.defined - self.used
        unused_imp = self.imports - self.used

        results = []
        for v in undefined:
            results.append({"type": "Undefined Variable",
                            "message": f"Variable '{v}' is used before being defined."})
        for v in unused_var:
            results.append({"type": "Unused Variable",
                            "message": f"Variable '{v}' is defined but never used."})
        for i in unused_imp:
            results.append({"type": "Unused Import",
                            "message": f"Module '{i}' is imported but never used."})

        results.extend(self.issues)
        return results


# ── Non-Python static checkers ─────────────────────────────────────────────

def _detect_c_errors(code: str) -> list:
    issues = []
    lines = code.splitlines()

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # malloc without checking NULL
        if re.search(r'\bmalloc\s*\(', line) and "=" in line:
            if not any("NULL" in lines[j] or "null" in lines[j]
                       for j in range(i, min(i + 4, len(lines)))):
                issues.append({"type": "Null Check Missing", "severity": "error",
                                "message": f"Line {i}: malloc() result not checked for NULL."})

        # gets() — unsafe
        if re.search(r'\bgets\s*\(', line):
            issues.append({"type": "Unsafe Function", "severity": "error",
                           "message": f"Line {i}: gets() is unsafe, use fgets() instead."})

        # strcpy without bounds
        if re.search(r'\bstrcpy\s*\(', line):
            issues.append({"type": "Unsafe Function", "severity": "warning",
                           "message": f"Line {i}: strcpy() is unsafe, use strncpy() instead."})

        # printf without format string literal
        if re.search(r'\bprintf\s*\(\s*[^"\']', line):
            issues.append({"type": "Format String Risk", "severity": "warning",
                           "message": f"Line {i}: printf() called without a string literal format."})

        # missing semicolons on non-preprocessor, non-brace lines
        if (stripped and
                not stripped.startswith("//") and
                not stripped.startswith("#") and
                not stripped.startswith("/*") and
                not stripped.endswith("{") and
                not stripped.endswith("}") and
                not stripped.endswith(";") and
                not stripped.endswith(",") and
                not stripped.endswith("\\") and
                re.search(r'\w', stripped)):
            issues.append({"type": "Missing Semicolon", "severity": "warning",
                           "message": f"Line {i}: possible missing semicolon."})

        # == instead of = in assignments (common typo)
        if re.search(r'\bif\s*\(.*=[^=]', line) and "==" not in line:
            issues.append({"type": "Assignment in Condition", "severity": "warning",
                           "message": f"Line {i}: possible assignment inside if condition (use == for comparison)."})

    # Check for main() function
    if not re.search(r'\bmain\s*\(', code):
        issues.append({"type": "No Entry Point", "severity": "warning",
                       "message": "No main() function found."})

    # Check for free() when malloc is used
    if re.search(r'\bmalloc\b', code) and not re.search(r'\bfree\b', code):
        issues.append({"type": "Memory Leak", "severity": "error",
                       "message": "malloc() used without corresponding free() — possible memory leak."})

    return issues


def _detect_cpp_errors(code: str) -> list:
    issues = []
    lines = code.splitlines()

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Raw pointers — suggest smart pointers
        if re.search(r'\bnew\b', line) and not re.search(r'\bdelete\b', line):
            issues.append({"type": "Raw Pointer", "severity": "warning",
                           "message": f"Line {i}: raw 'new' detected — consider unique_ptr or shared_ptr."})

        # using namespace std in header-like context
        if re.search(r'using\s+namespace\s+std', line):
            issues.append({"type": "Bad Practice", "severity": "warning",
                           "message": f"Line {i}: 'using namespace std' can cause name conflicts."})

        # C-style cast
        if re.search(r'\(int\)|\(char\)|\(float\)|\(double\)', line):
            issues.append({"type": "C-Style Cast", "severity": "warning",
                           "message": f"Line {i}: C-style cast detected — use static_cast<> instead."})

        # printf in C++ code
        if re.search(r'\bprintf\s*\(', line):
            issues.append({"type": "C-Style IO", "severity": "warning",
                           "message": f"Line {i}: prefer std::cout over printf() in C++."})

        # endl vs "\n"
        if re.search(r'<<\s*endl', line):
            issues.append({"type": "Performance", "severity": "warning",
                           "message": f"Line {i}: std::endl flushes the buffer — prefer '\\n' for performance."})

    # new without delete
    new_count    = len(re.findall(r'\bnew\b', code))
    delete_count = len(re.findall(r'\bdelete\b', code))
    if new_count > delete_count:
        issues.append({"type": "Memory Leak", "severity": "error",
                       "message": f"{new_count} 'new' vs {delete_count} 'delete' — possible memory leak."})

    # Virtual destructor check
    if re.search(r'\bclass\b', code) and re.search(r'\bvirtual\b', code):
        if not re.search(r'virtual\s+~', code):
            issues.append({"type": "Missing Virtual Destructor", "severity": "error",
                           "message": "Class with virtual methods should have a virtual destructor."})

    return issues


def _detect_java_errors(code: str) -> list:
    issues = []
    lines = code.splitlines()

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # == for String comparison
        if re.search(r'String.*==|==.*String', line):
            issues.append({"type": "String Comparison", "severity": "error",
                           "message": f"Line {i}: use .equals() instead of == for String comparison."})

        # Raw types (List, Map without generics)
        if re.search(r'\bList\s+\w|\bMap\s+\w|\bArrayList\s*\(\)', line):
            issues.append({"type": "Raw Type", "severity": "warning",
                           "message": f"Line {i}: use generic types e.g. List<String> instead of raw List."})

        # System.out.println in production code
        if re.search(r'System\.out\.print', line):
            issues.append({"type": "Debug Statement", "severity": "warning",
                           "message": f"Line {i}: System.out.println found — use a logger instead."})

        # Empty catch block
        if re.search(r'catch\s*\(.*\)\s*\{?\s*\}?', line) and stripped.endswith("}"):
            issues.append({"type": "Empty Catch Block", "severity": "error",
                           "message": f"Line {i}: empty catch block silences exceptions."})

        # Missing access modifier on methods/fields
        if re.search(r'^\s*(void|int|String|boolean|double|float)\s+\w+\s*\(', line):
            if not re.search(r'\b(public|private|protected)\b', line):
                issues.append({"type": "Missing Access Modifier", "severity": "warning",
                               "message": f"Line {i}: method or field missing access modifier (public/private/protected)."})

        # Null check missing after object creation
        if re.search(r'=\s*new\s+\w+', line):
            if not any("null" in lines[j].lower() for j in range(i, min(i + 3, len(lines)))):
                issues.append({"type": "Null Check Missing", "severity": "warning",
                               "message": f"Line {i}: object created without null check."})

    # No class definition
    if not re.search(r'\bclass\s+\w+', code):
        issues.append({"type": "No Class Definition", "severity": "error",
                       "message": "No class definition found — Java code requires a class."})

    return issues


def _detect_javascript_errors(code: str) -> list:
    issues = []
    lines = code.splitlines()

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # var usage
        if re.search(r'\bvar\s+', line):
            issues.append({"type": "Avoid var", "severity": "warning",
                           "message": f"Line {i}: use 'let' or 'const' instead of 'var'."})

        # == instead of ===
        if re.search(r'[^=!<>]==[^=]', line) and not re.search(r'===', line):
            issues.append({"type": "Loose Equality", "severity": "warning",
                           "message": f"Line {i}: use === instead of == for strict equality check."})

        # != instead of !==
        if re.search(r'!=[^=]', line) and not re.search(r'!==', line):
            issues.append({"type": "Loose Inequality", "severity": "warning",
                           "message": f"Line {i}: use !== instead of != for strict inequality check."})

        # console.log left in code
        if re.search(r'\bconsole\.log\s*\(', line):
            issues.append({"type": "Debug Statement", "severity": "warning",
                           "message": f"Line {i}: console.log() should be removed from production code."})

        # async function without try/catch
        if re.search(r'\basync\s+function\b|\basync\s+\(', line):
            fn_body_start = i
            fn_lines = lines[fn_body_start:fn_body_start + 20]
            if not any("try" in l or "catch" in l for l in fn_lines):
                issues.append({"type": "Unhandled Async Error", "severity": "warning",
                               "message": f"Line {i}: async function without try/catch error handling."})

        # eval() usage
        if re.search(r'\beval\s*\(', line):
            issues.append({"type": "Dangerous Function", "severity": "error",
                           "message": f"Line {i}: eval() is dangerous and should be avoided."})

        # Undefined variable patterns
        if re.search(r'\bundefined\s*==\s*', line) or re.search(r'==\s*undefined\b', line):
            issues.append({"type": "Undefined Check", "severity": "warning",
                           "message": f"Line {i}: use typeof x === 'undefined' instead of x == undefined."})

    return issues


def _detect_sql_errors(code: str) -> list:
    issues = []
    lines = code.splitlines()
    upper = code.upper()

    for i, line in enumerate(lines, 1):
        upper_line = line.upper().strip()

        # SELECT *
        if re.search(r'\bSELECT\s+\*', line, re.IGNORECASE):
            issues.append({"type": "SELECT *", "severity": "warning",
                           "message": f"Line {i}: avoid SELECT * — specify column names explicitly."})

        # UPDATE without WHERE
        if re.search(r'\bUPDATE\b', line, re.IGNORECASE):
            block = " ".join(lines[i-1:i+5]).upper()
            if "WHERE" not in block:
                issues.append({"type": "UPDATE without WHERE", "severity": "error",
                               "message": f"Line {i}: UPDATE statement without WHERE clause will affect all rows."})

        # DELETE without WHERE
        if re.search(r'\bDELETE\b', line, re.IGNORECASE):
            block = " ".join(lines[i-1:i+5]).upper()
            if "WHERE" not in block:
                issues.append({"type": "DELETE without WHERE", "severity": "error",
                               "message": f"Line {i}: DELETE statement without WHERE clause will delete all rows."})

        # String concatenation in queries (SQL injection risk)
        if re.search(r"'\s*\+\s*|'\s*\|\|\s*'", line):
            issues.append({"type": "SQL Injection Risk", "severity": "error",
                           "message": f"Line {i}: string concatenation in query — use parameterized queries."})

        # LIKE without index hint
        if re.search(r"\bLIKE\s+'%", line, re.IGNORECASE):
            issues.append({"type": "Leading Wildcard", "severity": "warning",
                           "message": f"Line {i}: LIKE with leading '%' cannot use index — may cause full table scan."})

        # NOT IN with subquery (performance)
        if re.search(r'\bNOT\s+IN\s*\(', line, re.IGNORECASE):
            issues.append({"type": "Performance", "severity": "warning",
                           "message": f"Line {i}: NOT IN with subquery can be slow — consider NOT EXISTS."})

    # No WHERE in any SELECT
    if re.search(r'\bSELECT\b', upper) and not re.search(r'\bWHERE\b', upper):
        if not re.search(r'\bLIMIT\b|\bTOP\b', upper):
            issues.append({"type": "Missing Filter", "severity": "warning",
                           "message": "SELECT query without WHERE or LIMIT — may return entire table."})

    return issues


# ── Public interface ───────────────────────────────────────────────────────

def detect_errors(code: str, language: str = "Python") -> list:
    """
    Detect errors in code for all supported languages.
    Python: full AST analysis.
    Others: regex-based static checks covering common issues per language.
    """
    lang = language.strip().lower()

    if lang == "python":
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return [{"type": "Syntax Error", "severity": "error", "message": str(e)}]
        reviewer = AIReviewer()
        reviewer.visit(tree)
        return reviewer.analyze()

    elif lang == "c":
        return _detect_c_errors(code)

    elif lang in ("c++", "cpp"):
        return _detect_cpp_errors(code)

    elif lang == "java":
        return _detect_java_errors(code)

    elif lang == "javascript":
        return _detect_javascript_errors(code)

    elif lang == "sql":
        return _detect_sql_errors(code)

    return []