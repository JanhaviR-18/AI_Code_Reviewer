import reflex as rx
from ..state import State, SubmissionRecord
from ..navbar import navbar
from ..footer import footer

# ── Design Tokens ─────────────────────────────
BG_BASE   = "#f2f0eb"
BG_CARD   = "#eceae4"
BORDER    = "#1a1a1a"
BORDER_LT = "#d4d0c8"
ACCENT    = "#c0392b"

GREEN  = "#2d6a1f"
AMBER  = "#8a5a00"
RED    = "#a02020"

TEXT_PRIMARY   = "#1a1a1a"
TEXT_SECONDARY = "#5a5a5a"
TEXT_MUTED     = "#757575"

FONT_SERIF = "'Instrument Serif', serif"
FONT_MONO  = "'DM Mono', monospace"
FONT_SANS  = "'DM Sans', sans-serif"


def _score_badge(score: int) -> rx.Component:
    return rx.cond(
        score >= 90,
        rx.box(
            rx.text(score.to_string() + "/100",
                    font_family=FONT_MONO, font_size="10px",
                    font_weight="500", color=GREEN),
            background="#e8f0e4",
            border="1px solid #b8d4b0",
            padding="3px 10px",
        ),
        rx.cond(
            score >= 55,
            rx.box(
                rx.text(score.to_string() + "/100",
                        font_family=FONT_MONO, font_size="10px",
                        font_weight="500", color=AMBER),
                background="#fdf3e3",
                border="1px solid #e8c97a",
                padding="3px 10px",
            ),
            rx.box(
                rx.text(score.to_string() + "/100",
                        font_family=FONT_MONO, font_size="10px",
                        font_weight="500", color=RED),
                background="#fceaea",
                border="1px solid #e8b0b0",
                padding="3px 10px",
            ),
        ),
    )


def _history_row(record: SubmissionRecord) -> rx.Component:
    return rx.box(
        rx.hstack(
            # Timestamp + status
            rx.vstack(
                rx.text(
                    record.timestamp,
                    font_family=FONT_MONO,
                    font_size="10px",
                    color=TEXT_MUTED,
                ),
                rx.hstack(
                    rx.cond(
                        record.syntax_ok,
                        rx.text("✓ syntax ok",
                                font_family=FONT_MONO, font_size="9px", color=GREEN),
                        rx.text("✗ syntax error",
                                font_family=FONT_MONO, font_size="9px", color=RED),
                    ),
                    rx.text("·", font_family=FONT_MONO,
                            font_size="9px", color=TEXT_MUTED),
                    rx.text(
                        record.error_count.to_string() + " issue(s)",
                        font_family=FONT_MONO, font_size="9px", color=TEXT_MUTED,
                    ),
                    spacing="2", align="center",
                ),
                spacing="1",
                align="start",
                min_width="150px",
            ),

            # Code snippet
            rx.box(
                rx.text(
                    record.code_snippet,
                    font_family=FONT_MONO,
                    font_size="12px",
                    color=TEXT_SECONDARY,
                    white_space="nowrap",
                    overflow="hidden",
                    text_overflow="ellipsis",
                ),
                flex="1",
                overflow="hidden",
                padding_x="24px",
            ),

            # Score badge
            _score_badge(record.score),

            spacing="4",
            align="center",
            width="100%",
        ),
        padding="16px 20px",
        border_bottom=f"1px solid {BORDER_LT}",
        transition="background 0.15s",
        _hover={"background": BG_CARD},
        width="100%",
    )


def _empty_state() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.text(
                "No submissions yet.",
                font_family=FONT_SERIF,
                font_size="22px",
                font_style="italic",
                color=TEXT_SECONDARY,
            ),
            rx.text(
                "Run your first code analysis to see it appear here.",
                font_family=FONT_SANS,
                font_size="13px",
                font_weight="300",
                color=TEXT_MUTED,
            ),
            rx.link(
                rx.box(
                    rx.text(
                        "Go to Analyzer →",
                        font_family=FONT_MONO,
                        font_size="11px",
                        text_transform="uppercase",
                        letter_spacing="0.08em",
                        color=BG_BASE,
                    ),
                    background=TEXT_PRIMARY,
                    padding="11px 22px",
                    margin_top="8px",
                    transition="background 0.15s",
                    _hover={"background": ACCENT},
                ),
                href="/analyzer",
                text_decoration="none",
            ),
            spacing="3",
            
        ),
        align="center",
        padding_y="80px",
    )


def history() -> rx.Component:
    return rx.box(

        rx.html("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');
        body { background: #f2f0eb; }
        </style>
        """),

        navbar(),

        rx.center(
            rx.vstack(

                # ── Header row ─────────────────────────
                rx.box(
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                "Submission History",
                                font_family=FONT_SERIF,
                                font_size="36px",
                                font_weight="400",
                                font_style="italic",
                                color=TEXT_PRIMARY,
                                letter_spacing="-0.02em",
                                line_height="1.1",
                            ),
                          
                            spacing="2",
                            align="start",
                        ),
                        rx.spacer(),
                        rx.cond(
                            State.history.length() > 0,
                            rx.button(
                                rx.text(
                                    "Clear All",
                                    font_family=FONT_MONO,
                                    font_size="10px",
                                    text_transform="uppercase",
                                    letter_spacing="0.08em",
                                    color=RED,
                                ),
                                on_click=State.clear_history,
                                background="transparent",
                                border=f"1px solid #e8b0b0",
                                border_radius="0",
                                padding_x="16px",
                                height="34px",
                                cursor="pointer",
                                transition="background 0.15s",
                                _hover={"background": "#fceaea"},
                            ),
                            rx.box(),
                        ),
                        width="100%",
                        align="center",
                    ),
                    padding_bottom="28px",
                    border_bottom=f"1px solid {BORDER_LT}",
                    width="100%",
                ),

                
                # ── Table header ───────────────────────
                rx.cond(
                    State.history.length() > 0,
                    rx.box(
                        rx.hstack(
                            rx.text(
                                "Timestamp",
                                font_family=FONT_MONO,
                                font_size="9px",
                                text_transform="uppercase",
                                letter_spacing="0.1em",
                                color=TEXT_MUTED,
                                min_width="150px",
                            ),
                            rx.text(
                                "Code Snippet",
                                font_family=FONT_MONO,
                                font_size="9px",
                                text_transform="uppercase",
                                letter_spacing="0.1em",
                                color=TEXT_MUTED,
                                flex="1",
                                padding_x="24px",
                            ),
                            rx.text(
                                "Score",
                                font_family=FONT_MONO,
                                font_size="9px",
                                text_transform="uppercase",
                                letter_spacing="0.1em",
                                color=TEXT_MUTED,
                            ),
                            width="100%",
                            spacing="4",
                        ),
                        padding="10px 20px",
                        background=BG_CARD,
                        border=f"1px solid {BORDER_LT}",
                        border_bottom="none",
                        width="100%",
                    ),
                    rx.box(),
                ),

                # ── History rows ───────────────────────
                rx.cond(
                    State.history.length() > 0,
                    rx.box(
                        rx.vstack(
                            rx.foreach(State.history, _history_row),
                            spacing="0",
                            width="100%",
                        ),
                        border=f"1px solid {BORDER_LT}",
                        width="100%",
                    ),
                    _empty_state(),
                ),

                spacing="5",
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