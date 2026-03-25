import reflex as rx
from ..state import State
from ..navbar import navbar
from ..footer import footer

# ── Design Tokens ─────────────────────────────
BG_BASE   = "#f2f0eb"
BG_CARD   = "#eceae4"
BG_CODE   = "#1a1a1a"
BORDER    = "#1a1a1a"
BORDER_LT = "#d4d0c8"
ACCENT    = "#c0392b"

GREEN     = "#2d6a1f"
GREEN_BG  = "#e8f0e4"
GREEN_BDR = "#b8d4b0"

AMBER     = "#8a5a00"
AMBER_BG  = "#fdf3e3"
AMBER_BDR = "#e8c97a"

RED       = "#a02020"
RED_BG    = "#fceaea"
RED_BDR   = "#e8b0b0"

TEXT_PRIMARY   = "#1a1a1a"
TEXT_SECONDARY = "#5a5a5a"
TEXT_MUTED     = "#757575"

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
        color=TEXT_MUTED,
    )


def _chip(text, bg, border, color) -> rx.Component:
    return rx.box(
        rx.text(
            text,
            font_family=FONT_MONO,
            font_size="10px",
            letter_spacing="0.04em",
            color=color,
        ),
        background=bg,
        border=f"1px solid {border}",
        padding="4px 10px",
    )


def _result_block(icon: str, label: str, value, bg: str, border: str, color: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(icon, font_size="12px"),
                _section_label(label),
                spacing="2",
                align="center",
            ),
            rx.box(
                rx.text(
                    value,
                    font_family=FONT_MONO,
                    font_size="12px",
                    color=color,
                    white_space="pre-wrap",
                    line_height="1.7",
                    width="100%",
                ),
                background=bg,
                border=f"1px solid {border}",
                padding="14px",
                width="100%",
                min_height="64px",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        width="100%",
    )


def _score_panel() -> rx.Component:
    return rx.box(
        rx.vstack(
            _section_label("Quality Score"),
            rx.hstack(
                rx.cond(
                    State.style_score >= 90,
                    rx.text(
                        State.style_score.to_string(),
                        font_family=FONT_SERIF,
                        font_size="56px",
                        font_style="italic",
                        color=GREEN,
                        line_height="1",
                    ),
                    rx.cond(
                        State.style_score >= 55,
                        rx.text(
                            State.style_score.to_string(),
                            font_family=FONT_SERIF,
                            font_size="56px",
                            font_style="italic",
                            color=AMBER,
                            line_height="1",
                        ),
                        rx.text(
                            State.style_score.to_string(),
                            font_family=FONT_SERIF,
                            font_size="56px",
                            font_style="italic",
                            color=RED,
                            line_height="1",
                        ),
                    ),
                ),
                rx.vstack(
                    rx.text(
                        "/ 100",
                        font_family=FONT_MONO,
                        font_size="11px",
                        color=TEXT_MUTED,
                    ),
                    rx.text(
                        State.score_label,
                        font_family=FONT_MONO,
                        font_size="10px",
                        text_transform="uppercase",
                        letter_spacing="0.06em",
                        color=TEXT_SECONDARY,
                    ),
                    spacing="1",
                    align="start",
                    padding_top="8px",
                ),
                spacing="3",
                align="end",
            ),
            # Score bar
            rx.box(
                rx.box(
                    height="2px",
                    width=State.style_score.to_string() + "%",
                    background=TEXT_PRIMARY,
                    transition="width 0.5s ease",
                ),
                height="2px",
                background=BORDER_LT,
                width="100%",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        padding="20px 24px",
        background=BG_CARD,
        border=f"1px solid {BORDER_LT}",
        width="100%",
    )


def _before_after() -> rx.Component:
    return rx.cond(
        State.has_snippets,
        rx.box(
            rx.vstack(
                
                rx.grid(
                    # Before
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.box(
                                    width="8px", height="8px",
                                    background=RED_BG,
                                    border=f"1px solid {RED_BDR}",
                                ),
                                rx.text(
                                    "Before",
                                    font_family=FONT_MONO,
                                    font_size="9px",
                                    text_transform="uppercase",
                                    letter_spacing="0.1em",
                                    color=RED,
                                ),
                                spacing="2", align="center",
                            ),
                            rx.box(
                                rx.text(
                                    State.before_snippet,
                                    font_family=FONT_MONO,
                                    font_size="12px",
                                    color=RED,
                                    white_space="pre-wrap",
                                    line_height="1.7",
                                ),
                                background=RED_BG,
                                border=f"1px solid {RED_BDR}",
                                padding="14px",
                                width="100%",
                            ),
                            spacing="3",
                            align="start",
                            width="100%",
                        ),
                        width="100%",
                    ),
                    # After
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.box(
                                    width="8px", height="8px",
                                    background=GREEN_BG,
                                    border=f"1px solid {GREEN_BDR}",
                                ),
                                rx.text(
                                    "After",
                                    font_family=FONT_MONO,
                                    font_size="9px",
                                    text_transform="uppercase",
                                    letter_spacing="0.1em",
                                    color=GREEN,
                                ),
                                spacing="2", align="center",
                            ),
                            rx.box(
                                rx.text(
                                    State.after_snippet,
                                    font_family=FONT_MONO,
                                    font_size="12px",
                                    color=GREEN,
                                    white_space="pre-wrap",
                                    line_height="1.7",
                                ),
                                background=GREEN_BG,
                                border=f"1px solid {GREEN_BDR}",
                                padding="14px",
                                width="100%",
                            ),
                            spacing="3",
                            align="start",
                            width="100%",
                        ),
                        width="100%",
                    ),
                    columns="2",
                    spacing="4",
                    width="100%",
                ),
                spacing="4",
                width="100%",
            ),
            padding="20px 24px",
            border=f"1px solid {BORDER_LT}",
            width="100%",
        ),
        rx.box(),
    )


def analyzer() -> rx.Component:
    return rx.box(

        rx.html("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');
        body { background: #f2f0eb; }
        textarea { resize: vertical !important; }
        </style>
        """),

        navbar(),

        rx.center(
            rx.vstack(

                # ── Page header ────────────────────────
                rx.box(
                    rx.vstack(
                        rx.text(
                            "Code Analyzer",
                            font_family=FONT_SERIF,
                            font_size="36px",
                            font_weight="400",
                            font_style="italic",
                            color=TEXT_PRIMARY,
                            letter_spacing="-0.02em",
                            line_height="1.1",
                        ),
                        rx.text(
                            "Paste Python code. Get instant AI-powered feedback.",
                            font_family=FONT_SANS,
                            font_size="14px",
                            font_weight="300",
                            color=TEXT_SECONDARY,
                        ),
                        spacing="2",
                        align="start",
                    ),
                    padding_bottom="28px",
                    border_bottom=f"1px solid {BORDER_LT}",
                    width="100%",
                ),

                # ── Code editor ────────────────────────
                rx.vstack(
                    rx.hstack(
                        _section_label("Python Code Input"),
                        rx.spacer(),
                        rx.cond(
                            State.user_code != "",
                            rx.text(
                                "● ready",
                                font_family=FONT_MONO,
                                font_size="9px",
                                color=GREEN,
                                letter_spacing="0.06em",
                            ),
                            rx.text(
                                "○ empty",
                                font_family=FONT_MONO,
                                font_size="9px",
                                color=TEXT_MUTED,
                                letter_spacing="0.06em",
                            ),
                        ),
                        width="100%",
                    ),
                    rx.text_area(
                        value=State.user_code,
                        on_change=State.set_user_code,
                        placeholder="# Paste your Python code here...",
                        height="260px",
                        width="100%",
                        font_family=FONT_MONO,
                        font_size="13px",
                        background=BG_CODE,
                        color="#e8e4dc",
                        border="none",
                        border_radius="0",
                        padding="18px",
                        outline="none",
                        _focus={"outline": f"2px solid {ACCENT}"},
                        _placeholder={"color": "#4a4a4a"},
                    ),
                    spacing="3",
                    width="100%",
                ),

                # ── Buttons ────────────────────────────
                rx.hstack(
                    rx.button(
                        rx.cond(
                            State.is_loading,
                            rx.hstack(
                                rx.spinner(size="2", color=BG_BASE),
                                rx.text(
                                    "Analyzing…",
                                    font_family=FONT_MONO,
                                    font_size="11px",
                                    text_transform="uppercase",
                                    letter_spacing="0.08em",
                                    color=BG_BASE,
                                ),
                                spacing="2", align="center",
                            ),
                            rx.text(
                                " Analyze Code",
                                font_family=FONT_MONO,
                                font_size="11px",
                                text_transform="uppercase",
                                letter_spacing="0.08em",
                                color=BG_BASE,
                            ),
                        ),
                        on_click=State.analyze_code,
                        background=ACCENT,
                        border="none",
                        border_radius="0",
                        height="42px",
                        padding_x="24px",
                        cursor="pointer",
                        transition="background 0.15s",
                        _hover={"background": TEXT_PRIMARY},
                    ),
                    
                    spacing="3",
                ),

                # ── Score ──────────────────────────────
                _score_panel(),

                # ── Syntax + Issues ────────────────────
                rx.grid(
                    _result_block(
                        "✓", "Syntax Check",
                        State.syntax_output,
                        GREEN_BG, GREEN_BDR, GREEN,
                    ),
                    _result_block(
                        "⚠", "Detected Issues",
                        State.errors_output,
                        AMBER_BG, AMBER_BDR, AMBER,
                    ),
                    columns="2",
                    spacing="4",
                    width="100%",
                ),

                # ── AI Suggestions ─────────────────────
                rx.vstack(
                    rx.hstack(
                        _section_label("AI Suggestions"),
                        spacing="2",
                    ),
                    rx.text_area(
                        value=State.ai_output,
                        is_read_only=True,
                        height="180px",
                        width="100%",
                        font_family=FONT_MONO,
                        font_size="12px",
                        color=TEXT_SECONDARY,
                        background=BG_CARD,
                        border=f"1px solid {BORDER_LT}",
                        border_radius="0",
                        padding="14px",
                        line_height="1.7",
                    ),
                    spacing="3",
                    width="100%",
                ),

                # ── Before / After ─────────────────────
                _before_after(),

                spacing="6",
                width="100%",
                max_width="860px",
            ),
            padding="48px 24px",
        ),

        footer(),

        background=BG_BASE,
        min_height="100vh",
        width="100%",
    )