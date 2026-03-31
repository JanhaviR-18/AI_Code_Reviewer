import reflex as rx
from ..navbar import navbar
from ..footer import footer
from ..state import State

# ── Design Tokens ─────────────────────────────
BG_BASE      = "#f2f0eb"
BG_DARK      = "#1a1a1a"
BG_CARD      = "#eceae4"
BG_CARD_DARK = "#2a2a2a"
BORDER_LT    = "#d4d0c8"
BORDER_DK    = "#3a3a3a"
ACCENT       = "#c0392b"

TEXT_PRIMARY   = "#1a1a1a"
TEXT_SECONDARY = "#5a5a5a"
TEXT_MUTED     = "#757575"

TEXT_PRIMARY_DK   = "#f2f0eb"
TEXT_SECONDARY_DK = "#9a9a9a"
TEXT_MUTED_DK     = "#6a6a6a"

FONT_SERIF = "'Instrument Serif', serif"
FONT_MONO  = "'DM Mono', monospace"
FONT_SANS  = "'DM Sans', sans-serif"


def _section_label(text: str) -> rx.Component:
    return rx.text(
        text,
        font_family=FONT_MONO,
        font_size="9px",
        text_transform="uppercase",
        letter_spacing="0.14em",
        color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_PRIMARY),
    )


def _what_row(num: str, title: str, desc: str) -> rx.Component:
    return rx.hstack(
        rx.text(
            num,
            font_family=FONT_MONO,
            font_size="10px",
            color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED),
            min_width="28px",
            padding_top="2px",
        ),
        rx.vstack(
            rx.text(
                title,
                font_family=FONT_SANS,
                font_size="14px",
                font_weight="500",
                color=rx.cond(State.is_dark, TEXT_PRIMARY_DK, TEXT_PRIMARY),
            ),
            rx.text(
                desc,
                font_family=FONT_SANS,
                font_size="13px",
                font_weight="300",
                color=rx.cond(State.is_dark, TEXT_SECONDARY_DK, TEXT_SECONDARY),
                line_height="1.65",
            ),
            spacing="1",
            align="start",
        ),
        padding="18px 0",
        border_bottom=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
        width="100%",
        spacing="5",
        align="start",
    )


def _tech_chip(name: str, detail: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(
                name,
                font_family=FONT_MONO,
                font_size="11px",
                font_weight="500",
                color=rx.cond(State.is_dark, TEXT_PRIMARY_DK, TEXT_PRIMARY),
                letter_spacing="0.04em",
            ),
            rx.text(
                detail,
                font_family=FONT_SANS,
                font_size="11px",
                font_weight="300",
                color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED),
            ),
            spacing="1",
            align="start",
        ),
        padding="14px 18px",
        background=rx.cond(State.is_dark, BG_CARD_DARK, BG_CARD),
        border=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
        transition="border-color 0.15s",
        _hover={"border_color": ACCENT},
        min_width="140px",
    )


def _outcome_item(text: str) -> rx.Component:
    return rx.hstack(
        rx.box(
            width="6px",
            height="6px",
            background=ACCENT,
            flex_shrink="0",
            margin_top="6px",
        ),
        rx.text(
            text,
            font_family=FONT_SANS,
            font_size="13px",
            font_weight="300",
            color=rx.cond(State.is_dark, TEXT_SECONDARY_DK, TEXT_SECONDARY),
            line_height="1.65",
        ),
        spacing="3",
        align="start",
        width="100%",
    )


def about() -> rx.Component:
    return rx.box(

        rx.html("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');
        body { margin: 0; }
        </style>
        """),

        navbar(),

        rx.center(
            rx.vstack(

                # ── Page header ────────────────────────
                rx.box(
                    rx.vstack(
                        rx.text(
                            "AI Code Reviewer",
                            font_family=FONT_SERIF,
                            font_size="38px",
                            font_weight="400",
                            font_style="italic",
                            color=ACCENT,
                            letter_spacing="-0.02em",
                            line_height="1.1",
                        ),
                        rx.text(
                            "An intelligent code analysis tool that combines Python AST parsing "
                            "with AI-powered suggestions to help students write cleaner, "
                            "safer and better-structured code.",
                            font_family=FONT_SANS,
                            font_size="15px",
                            font_weight="300",
                            color=rx.cond(State.is_dark, TEXT_SECONDARY_DK, TEXT_SECONDARY),
                            line_height="1.75",
                            max_width="580px",
                        ),
                        spacing="4",
                        align="start",
                    ),
                    padding_bottom="36px",
                    border_bottom=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
                    width="100%",
                ),

                # ── Problem statement ──────────────────
                rx.box(
                    rx.hstack(
                        rx.box(
                            _section_label("Problem"),
                            width="180px",
                            flex_shrink="0",
                            padding_top="4px",
                        ),
                        rx.text(
                            "Reviewing code manually for correctness, coding style and optimization "
                            "is time-consuming — especially in academic environments where students "
                            "submit large volumes of assignments. Instructors spend significant effort "
                            "on repetitive feedback that could be automated and students miss out on "
                            "instant, actionable guidance.",
                            font_family=FONT_SANS,
                            font_size="14px",
                            font_weight="300",
                            color=rx.cond(State.is_dark, TEXT_SECONDARY_DK, TEXT_SECONDARY),
                            line_height="1.75",
                        ),
                        spacing="6",
                        align="start",
                        width="100%",
                    ),
                    padding="32px 0",
                    border_bottom=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
                    width="100%",
                ),

                # ── What it does ───────────────────────
                rx.box(
                    rx.hstack(
                        rx.box(
                            _section_label("What it does"),
                            width="180px",
                            flex_shrink="0",
                            padding_top="22px",
                        ),
                        rx.vstack(
                            _what_row("01", "Error Detection",
                                "Identifies syntax errors and undefined variables using Python's "
                                "Abstract Syntax Tree (AST) parser with line-precise feedback."),
                            _what_row("02", "Bug Detection",
                                "Detects logical issues including unused imports, unreachable code, "
                                "and infinite loops — with plain-English explanations for each."),
                            _what_row("03", "Coding Style Review",
                                "Checks adherence to PEP8 guidelines — indentation, naming conventions, "
                                "function length — and scores submissions based on compliance."),
                            _what_row("04", "AI Optimization",
                                "Uses Groq API model to recommend alternative data structures, algorithmic "
                                "improvements and cleaner patterns with before/after code snippets."),
                            _what_row("05", "Automated Feedback",
                                "Reduces manual evaluation effort for instructors by delivering "
                                "categorized, instant feedback on every submission."),
                            spacing="0",
                            width="100%",
                        ),
                        spacing="6",
                        align="start",
                        width="100%",
                    ),
                    padding="32px 0",
                    border_bottom=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
                    width="100%",
                ),

                # ── Outcomes ───────────────────────────
                rx.box(
                    rx.hstack(
                        rx.box(
                            _section_label("Outcomes"),
                            width="180px",
                            flex_shrink="0",
                            padding_top="4px",
                        ),
                        rx.vstack(
                            _outcome_item("Students paste or upload code and instantly receive actionable insights."),
                            _outcome_item("Users can track submission history and feedback across sessions."),
                            _outcome_item("Code quality scores give a clear, objective measure of improvement."),
                            _outcome_item("Before/after snippets teach better coding patterns in context."),
                            spacing="3",
                            width="100%",
                        ),
                        spacing="6",
                        align="start",
                        width="100%",
                    ),
                    padding="32px 0",
                    border_bottom=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
                    width="100%",
                ),

                # ── Tech stack ─────────────────────────
                rx.box(
                    rx.hstack(
                        rx.box(
                            _section_label("Tech Stack"),
                            width="180px",
                            flex_shrink="0",
                            padding_top="4px",
                        ),
                        rx.hstack(
                            _tech_chip("Reflex", "UI framework"),
                            _tech_chip("Python", "Core language"),
                            _tech_chip("AST", "Code parsing"),
                            _tech_chip("Groq", "AI suggestions"),
                            _tech_chip("PEP8", "Style analysis"),
                            spacing="3",
                        ),
                        spacing="6",
                        align="start",
                        width="100%",
                    ),
                    padding="32px 0 8px",
                    width="100%",
                ),

                spacing="0",
                align="start",
                max_width="860px",
                width="100%",
            ),
            padding="48px 24px",
        ),

        footer(),

        background=rx.cond(State.is_dark, BG_DARK, BG_BASE),
        min_height="100vh",
        width="100%",
        transition="background 0.2s",
    )