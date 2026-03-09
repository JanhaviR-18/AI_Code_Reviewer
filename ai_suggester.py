import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

# ------------------ LOAD ENV ------------------

load_dotenv()
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

Your job is to analyze Python code and provide helpful feedback.
Analyze the following Python code and detected issues.

Give SHORT feedback.

Rules:
- Max 1–2 lines per issue
- No long explanations
- Provide a quick fix suggestion
- Use bullet points

Detected Issues:
{errors}

Python Code:
{code}

Provide clear, structured, beginner-friendly explanations.
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