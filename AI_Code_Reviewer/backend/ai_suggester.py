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

# ------------------ PROMPT TEMPLATE ------------------

prompt_template = PromptTemplate(
    input_variables=["code", "errors"],
    template="""
You are an expert Python code reviewer.

Analyze the following Python code and detected issues.

STRICT OUTPUT FORMAT — follow this exactly, no exceptions:

 FEEDBACK:
Give 2-3 bullet points of short feedback on the issues found.
- Max 1 line per bullet
- No long explanations

YOU MUST ALWAYS END WITH THIS EXACT BLOCK:

BEFORE:
<paste the original problematic code or a key snippet from it>

AFTER:
<paste the improved version of that same code>

Rules for BEFORE/AFTER:
- Always include this block even if code looks fine — show a best-practice improvement
- Keep snippets under 10 lines
- No markdown, no backticks, no code fences around the snippets
- BEFORE and AFTER must each be on their own line as shown above

Detected Issues:
{errors}

Python Code:
{code}
"""
)

# ------------------ AI SUGGESTION FUNCTION ------------------

def get_ai_suggestion(code: str, detected_errors: list):

    if not detected_errors:
        formatted_errors = "No major static issues detected."
    else:
        formatted_errors = "\n".join(
            [f"- {error['type']}: {error.get('message', '')}" for error in detected_errors]
        )

    final_prompt = prompt_template.format(
        code=code,
        errors=formatted_errors
    )

    try:
        response = model.invoke(final_prompt)
        return response.content

    except Exception as e:
        return f"AI suggestion failed: {str(e)}"