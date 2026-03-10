import reflex as rx

# -----------------------------
# State
# -----------------------------
class CodeState(rx.State):

    code_input: str = ""
    result: str = ""

    def set_code_input(self,value: str):
        self.code_input = value

    def analyze_code(self):
        if self.code_input == "":
            self.result = "Please paste some code first."
        else:
            self.result = "AI analysis will appear here."        

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
            rx.link("Analyze Code", href="/analyzer"),
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
def analyze_code():
    return rx.vstack(

        navbar(),

        rx.heading("AI Code Analyzer", size="8"),

        rx.text("Paste your Python code or upload a file to analyze."),

        rx.text_area(
            placeholder="Paste your code here...",
            value=CodeState.code_input,
            on_change=CodeState.set_code_input,
            width="80%",
            height="300px",
        ),

        rx.upload(
            rx.button("Upload Python File"),
            border="1px dashed gray",
            padding="1em",
        ),

        rx.button(
            "Analyze Code",
            on_click=CodeState.analyze_code,
            color_scheme="blue",
            margin_top="20px"
        ),

        rx.divider(),

        rx.heading("Analysis Result", size="6"),

        rx.box(
            rx.text(CodeState.result),
            padding="20px",
            border="1px solid #ccc",
            width="80%"
        ),

        align="center",
        spacing="5",
        padding="40px"
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


def help():
    return rx.center(
        rx.heading("Help & Documentation"),
        height="80vh",
    )


# -----------------------------
# App Config
# -----------------------------
app = rx.App()

app.add_page(home, route="/")
app.add_page(analyze_code, route="/analyzer")
app.add_page(history, route="/history")
app.add_page(about, route="/about")
app.add_page(help, route="/help")