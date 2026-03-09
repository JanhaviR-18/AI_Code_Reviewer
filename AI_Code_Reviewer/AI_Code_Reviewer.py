import reflex as rx

from code_parser import parse_code
from error_detector import detect_errors
from ai_suggester import get_ai_suggestion


# -----------------------------
# State
# -----------------------------
class CodeState(rx.State):

    code_input: str = ""
    error_output: str = ""
    style_output: str = ""
    optimization_output: str = ""

    async def analyze_code(self):

        code = self.code_input.strip()

        if not code:
            self.error_output = "Please enter Python code."
            self.style_output = ""
            self.optimization_output = ""
            return

        # ---------------- Syntax Check ----------------
        parse_result = parse_code(code)

        if not parse_result["success"]:
            self.error_output = parse_result["error"]
            self.style_output = ""
            self.optimization_output = ""
            return

        # ---------------- Static Analysis ----------------
        detected_errors = detect_errors(code)

        if detected_errors:
            self.error_output = "\n".join(
             [f"- **{err['type']}**: {err.get('message','')}" for err in detected_errors]
          )
        else:
            self.error_output = "No major static issues detected."

        # ---------------- AI Suggestions ----------------
        ai_feedback = get_ai_suggestion(code, detected_errors)

        self.style_output = ai_feedback
        self.optimization_output = "See AI suggestions above for optimization improvements."


# -----------------------------
# Navbar Component
# -----------------------------
def navbar():
    return rx.hstack(

        rx.hstack(
            rx.icon("cpu", size=28),
            rx.text("AI Code Reviewer", font_weight="bold", font_size="20px"),
            spacing="2",
        ),

        rx.spacer(),

        rx.hstack(
            rx.link("Home", href="/"),
            rx.link("Analyzer", href="/analyzer"),
            rx.link("History", href="/history"),
            rx.link("About", href="/about"),
            rx.link("Help", href="/help"),
            spacing="6",
        ),

        padding="20px",
        width="100%",
    )


# -----------------------------
# Hero Section
# -----------------------------
def hero_section():

    return rx.center(

        rx.vstack(

            rx.badge(
                "AI Powered Analysis",
                color_scheme="purple",
                variant="soft",
            ),

            rx.heading(
                "AI-Driven Code Reviewer System",
                size="9",
                text_align="center",
            ),

            rx.text(
                "Advanced code review using AST parsing, "
                "PEP8 validation and AI-based optimization.",
                text_align="center",
                color="gray",
            ),

            rx.hstack(
                rx.button("95% Accurate"),
                rx.button("Real-time Analysis", variant="outline"),
                rx.button("Secure & Reliable", variant="outline"),
                spacing="4",
                margin_top="20px",
            ),

            spacing="6",
            align="center",
        ),

        height="80vh",
        width="100%",
        bg="linear-gradient(135deg, #6B73FF 0%, #000DFF 100%)",
        color="white",
    )


# -----------------------------
# Code Analysis Page
# -----------------------------
def analyzer():

    return rx.container(

        navbar(),

        rx.heading("AI Driven Code Reviewer", size="8"),

        rx.text_area(
            placeholder="Paste your Python code here...",
            value=CodeState.code_input,
            on_change=CodeState.set_code_input,
            width="100%",
            height="300px",
        ),

        rx.button(
            "Analyze Code",
            on_click=CodeState.analyze_code,
            margin_top="10px",
        ),

        rx.divider(),

        rx.heading("Detected Errors"),
        rx.markdown(CodeState.error_output),

        rx.heading("AI Style Review"),
        rx.markdown(CodeState.style_output),

        rx.heading("Optimization Suggestions"),
        rx.markdown(CodeState.optimization_output),

        padding="40px",
    )


# -----------------------------
# Other Pages
# -----------------------------
def home():
    return rx.vstack(
        navbar(),
        hero_section(),
        spacing="0",
    )


def history():
    return rx.center(
        rx.heading("Submission History Page Coming Soon..."),
        height="80vh",
    )


def about():
    return rx.center(
        rx.heading("About the AI Code Reviewer"),
        height="80vh",
    )


def help_page():
    return rx.center(
        rx.heading("Help & Documentation"),
        height="80vh",
    )


# -----------------------------
# App Config
# -----------------------------
app = rx.App()

app.add_page(home, route="/")
app.add_page(analyzer, route="/analyzer")
app.add_page(history, route="/history")
app.add_page(about, route="/about")
app.add_page(help_page, route="/help")