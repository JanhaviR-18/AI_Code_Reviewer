import reflex as rx
from ..navbar import navbar
from ..footer import footer
from ..state import State

# ── Design Tokens ─────────────────────────────
BG_BASE   = "#f2f0eb"
BG_DARK   = "#1a1a1a"
BG_CARD   = "#eceae4"
BG_CARD_DARK = "#2a2a2a"
BORDER    = "#1a1a1a"
BORDER_LT = "#d4d0c8"
BORDER_DARK = "#3a3a3a"
ACCENT    = "#c0392b"

TEXT_PRIMARY   = "#1a1a1a"
TEXT_SECONDARY = "#5a5a5a"
TEXT_MUTED     = "#757575"

TEXT_PRIMARY_DARK   = "#f2f0eb"
TEXT_SECONDARY_DARK = "#9a9a9a"
TEXT_MUTED_DARK     = "#6a6a6a"

FONT_SERIF = "'Instrument Serif', serif"
FONT_MONO  = "'DM Mono', monospace"
FONT_SANS  = "'DM Sans', sans-serif"


def _eyebrow(text: str) -> rx.Component:
    return rx.text(
        text,
        font_family=FONT_MONO,
        font_size="10px",
        text_transform="uppercase",
        letter_spacing="0.14em",
        color=ACCENT,
    )


def _feature_row(num: str, title: str, desc: str) -> rx.Component:
    return rx.hstack(
        rx.text(
            num,
            font_family=FONT_MONO,
            font_size="10px",
            color=rx.cond(State.is_dark, TEXT_MUTED_DARK, TEXT_MUTED),
            min_width="28px",
        ),
        rx.vstack(
            rx.text(
                title,
                font_family=FONT_SANS,
                font_size="14px",
                font_weight="500",
                color=rx.cond(State.is_dark, TEXT_PRIMARY_DARK, TEXT_PRIMARY),
            ),
            rx.text(
                desc,
                font_family=FONT_SANS,
                font_size="13px",
                font_weight="300",
                color=rx.cond(State.is_dark, TEXT_SECONDARY_DARK, TEXT_SECONDARY),
                line_height="1.6",
            ),
            spacing="1",
            align="start",
        ),
        padding="18px 0",
        border_bottom=rx.cond(
            State.is_dark,
            f"1px solid {BORDER_DARK}",
            f"1px solid {BORDER_LT}",
        ),
        width="100%",
        spacing="5",
        align="start",
    )


def index() -> rx.Component:
    return rx.box(

        rx.html("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');
        body { margin: 0; }
        </style>
        """),

        navbar(),

        # ── HERO ──────────────────────────────────
        rx.center(
            rx.vstack(
                _eyebrow("AI · Python · Code Analysis"),

                rx.vstack(
                    rx.text(
                        "Review Code.",
                        font_family=FONT_SERIF,
                        font_size=["36px", "52px", "62px"],
                        font_weight="400",
                        color=rx.cond(State.is_dark, TEXT_PRIMARY_DARK, TEXT_PRIMARY),
                        line_height="1.05",
                        letter_spacing="-0.02em",
                    ),
                    rx.text(
                        "Improve Instantly.",
                        font_family=FONT_SERIF,
                        font_size=["36px", "52px", "62px"],
                        font_weight="400",
                        font_style="italic",
                        color=ACCENT,
                        line_height="1.05",
                        letter_spacing="-0.02em",
                    ),
                    spacing="0",
                ),

                rx.text(
                    "Paste your Python code and get instant feedback — "
                    "syntax errors, logic bugs, PEP8 violations "
                    "and smart optimizations.",
                    font_family=FONT_SANS,
                    font_size="15px",
                    font_weight="300",
                    color=rx.cond(State.is_dark, TEXT_SECONDARY_DARK, TEXT_SECONDARY),
                    line_height="1.7",
                    max_width="480px",
                    text_align="center",
                ),

                rx.hstack(
                    rx.link(
                        rx.box(
                            rx.text(
                                "Start Analyzing →",
                                font_family=FONT_MONO,
                                font_size="11px",
                                text_transform="uppercase",
                                letter_spacing="0.08em",
                                color=rx.cond(State.is_dark, BG_DARK, BG_BASE),
                            ),
                            background=rx.cond(State.is_dark, TEXT_PRIMARY_DARK, TEXT_PRIMARY),
                            padding="12px 24px",
                            transition="background 0.15s",
                            _hover={"background": ACCENT},
                        ),
                        href="/analyzer",
                        text_decoration="none",
                    ),
                    spacing="4",
                    justify="center",
                ),

                spacing="6",
                align="center",
                max_width="860px",
                width="100%",
            ),
            padding="72px 40px 60px",
            border_bottom=rx.cond(
                State.is_dark,
                f"1px solid {BORDER_DARK}",
                f"1px solid {BORDER_LT}",
            ),
            width="100%",
        ),

        # ── FEATURES ──────────────────────────────
        rx.center(
            rx.box(
                rx.hstack(
                    # Left: label
                    rx.box(
                        rx.text(
                            "What it does",
                            font_family=FONT_MONO,
                            font_size="9px",
                            text_transform="uppercase",
                            letter_spacing="0.14em",
                            color=rx.cond(State.is_dark, TEXT_MUTED_DARK, TEXT_MUTED),
                        ),
                        width="180px",
                        padding_top="22px",
                        flex_shrink="0",
                    ),

                    # Right: feature list
                    rx.vstack(
                        _feature_row("01", "Syntax Check",
                            "Catch syntax errors with line-precise AST parsing."),
                        _feature_row("02", "Bug Detection",
                            "Spot undefined variables, unused imports, unreachable code."),
                        _feature_row("03", "PEP8 Style Review",
                            "Score your code against Python's official style guide."),
                        _feature_row("04", "AI Optimization",
                            "Get AI-powered before/after snippets to make your code cleaner."),
                        spacing="0",
                        width="100%",
                    ),

                    spacing="6",
                    align="start",
                    width="100%",
                ),
                max_width="860px",
                width="100%",
            ),
            padding="40px 40px 48px",
            border_bottom=rx.cond(
                State.is_dark,
                f"1px solid {BORDER_DARK}",
                f"1px solid {BORDER_LT}",
            ),
            width="100%",
        ),

        # ── HOW IT WORKS ──────────────────────────
        rx.center(
            rx.box(
                rx.hstack(
                    rx.box(
                        rx.text(
                            "How it works",
                            font_family=FONT_MONO,
                            font_size="9px",
                            text_transform="uppercase",
                            letter_spacing="0.14em",
                            color=rx.cond(State.is_dark, TEXT_MUTED_DARK, TEXT_MUTED),
                        ),
                        width="180px",
                        flex_shrink="0",
                        padding_top="4px",
                    ),
                    rx.hstack(
                        rx.vstack(
                            rx.text("01", font_family=FONT_MONO,
                                    font_size="10px", color=ACCENT),
                            rx.text("Paste Code",
                                    font_family=FONT_SANS, font_size="13px",
                                    font_weight="500",
                                    color=rx.cond(State.is_dark, TEXT_PRIMARY_DARK, TEXT_PRIMARY)),
                            rx.text("Drop any Python snippet into the editor.",
                                    font_family=FONT_SANS, font_size="12px",
                                    font_weight="300",
                                    color=rx.cond(State.is_dark, TEXT_SECONDARY_DARK, TEXT_SECONDARY)),
                            spacing="2", align="start",
                        ),

                        rx.vstack(
                            rx.text("02", font_family=FONT_MONO,
                                    font_size="10px", color=ACCENT),
                            rx.text("Run Analysis",
                                    font_family=FONT_SANS, font_size="13px",
                                    font_weight="500",
                                    color=rx.cond(State.is_dark, TEXT_PRIMARY_DARK, TEXT_PRIMARY)),
                            rx.text("AST + AI kick in simultaneously.",
                                    font_family=FONT_SANS, font_size="12px",
                                    font_weight="300",
                                    color=rx.cond(State.is_dark, TEXT_SECONDARY_DARK, TEXT_SECONDARY)),
                            spacing="2", align="start",
                        ),

                        rx.vstack(
                            rx.text("03", font_family=FONT_MONO,
                                    font_size="10px", color=ACCENT),
                            rx.text("Read Feedback",
                                    font_family=FONT_SANS, font_size="13px",
                                    font_weight="500",
                                    color=rx.cond(State.is_dark, TEXT_PRIMARY_DARK, TEXT_PRIMARY)),
                            rx.text("Syntax, bugs, score, AI suggestions.",
                                    font_family=FONT_SANS, font_size="12px",
                                    font_weight="300",
                                    color=rx.cond(State.is_dark, TEXT_SECONDARY_DARK, TEXT_SECONDARY)),
                            spacing="2", align="start",
                        ),
                        spacing="4",
                        align="start",
                    ),
                    spacing="6",
                    align="start",
                    width="100%",
                ),
                max_width="860px",
                width="100%",
            ),
            padding="40px 40px 60px",
            width="100%",
        ),

        footer(),

        background=rx.cond(State.is_dark, BG_DARK, BG_BASE),
        min_height="100vh",
        transition="background 0.2s",
    )