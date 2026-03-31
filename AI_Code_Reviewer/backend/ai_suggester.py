import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

# ------------------ LOAD ENV ------------------

load_dotenv(dotenv_path="AI_Code_Reviewer/.env")
groq_api_key = os.getenv("GROQ_API_KEY")

# ------------------ MODEL SETUP ------------------

model = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=groq_api_key
)

# ------------------ LANGUAGE RULES ------------------

LANGUAGE_RULES = {
    "python": """
- Check for PEP8 style violations (naming, indentation, spacing)
- Flag unused imports, undefined variables, unreachable code
- Suggest list comprehensions, f-strings, context managers where appropriate
- Check for mutable default arguments, bare excepts, and anti-patterns
""",
    "c": """
- Check for memory leaks (malloc without free)
- Flag uninitialized variables and buffer overflows
- Suggest proper use of pointers and memory management
- Check for missing null checks and unsafe string functions (strcpy, gets)
""",
    "cpp": """
- Check for memory leaks (new without delete)
- Suggest RAII, smart pointers (unique_ptr, shared_ptr) over raw pointers
- Flag missing virtual destructors, improper use of references
- Suggest STL algorithms over manual loops where appropriate
""",
    "java": """
- Check for missing access modifiers (public/private/protected)
- Flag unchecked exceptions, raw types, and missing @Override annotations
- Suggest proper use of interfaces, generics, and design patterns
- Check for resource leaks (streams/connections not closed)
""",
    "javascript": """
- Flag use of var (suggest let/const instead)
- Check for == vs === equality issues
- Suggest async/await over raw Promise chains where appropriate
- Flag missing error handling in async code and potential undefined access
""",
    "sql": """
- Check for SELECT * usage (suggest explicit columns)
- Flag missing WHERE clauses in UPDATE/DELETE statements
- Suggest proper indexing strategies based on query patterns
- Check for SQL injection vulnerabilities and inefficient JOINs
""",
}

# ------------------ PROMPT TEMPLATE ------------------
# IMPORTANT: The output sections must appear in this exact order:
#   1. Feedback bullet points (plain text)
#   2. TIME COMPLEXITY: block
#   3. BEFORE: / AFTER: block
# state.py's _parse_ai_output() splits on these markers in order,
# so they must not be nested inside numbered "PART X" headings.

prompt_template = PromptTemplate(
    input_variables=["language", "language_rules", "code", "errors"],
    template="""
You are an expert {language} code reviewer.

Analyze the following {language} code and detected issues.

Language-specific rules to apply:
{language_rules}

STRICT OUTPUT FORMAT — follow this exactly, no exceptions, no extra headings:

Give 2-3 bullet points of short, actionable feedback. Be specific to the language. Max 1 line per bullet.

TIME COMPLEXITY:
Original: O(?)
Optimized: O(?)
Briefly explain the difference in 1 line.

BEFORE:
<paste the original problematic code or a key snippet, no backticks>

AFTER:
<paste the improved version of that same code, no backticks>

Rules:
- Output the sections in exactly the order shown above: feedback bullets, then TIME COMPLEXITY:, then BEFORE:, then AFTER:
- Always include TIME COMPLEXITY:, BEFORE:, and AFTER: even if the code looks fine — show a best-practice improvement
- Keep BEFORE/AFTER snippets under 10 lines
- No markdown, no backticks, no code fences, no "PART 1 / PART 2 / PART 3" labels
- BEFORE and AFTER must each be on their own line as shown above

Detected Issues:
{errors}

{language} Code:
{code}
"""
)

# ------------------ AI SUGGESTION FUNCTION ------------------

def get_ai_suggestion(code: str, detected_errors: list, language: str = "python"):
    language = language.lower()

    if not detected_errors:
        formatted_errors = "No major static issues detected."
    else:
        formatted_errors = "\n".join(
            [f"- {e['type']}: {e.get('message', '')}" for e in detected_errors]
        )

    language_rules = LANGUAGE_RULES.get(
        language,
        "- Follow best practices for this language.\n- Write clean, readable, efficient code."
    )

    final_prompt = prompt_template.format(
        language=language.upper(),
        language_rules=language_rules,
        code=code,
        errors=formatted_errors,
    )

    try:
        response = model.invoke(final_prompt)
        return response.content
    except Exception as e:
        return f"AI suggestion failed: {str(e)}"