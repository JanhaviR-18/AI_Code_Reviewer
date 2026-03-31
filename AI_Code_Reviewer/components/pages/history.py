import reflex as rx
from ..state import State, SubmissionRecord
from ..navbar import navbar
from ..footer import footer

BG_BASE      = "#f2f0eb"
BG_DARK      = "#1a1a1a"
BG_CARD      = "#eceae4"
BG_CARD_DARK = "#2a2a2a"
BG_CODE_DARK = "#0d0d0d"
BORDER_LT    = "#d4d0c8"
BORDER_DK    = "#3a3a3a"
ACCENT       = "#c0392b"

GREEN  = "#2d6a1f"; GREEN_BG = "#e8f0e4"; GREEN_BDR = "#b8d4b0"
GREEN_BG_DK = "#1a2e18"; GREEN_BDR_DK = "#2d5228"
AMBER  = "#8a5a00"; AMBER_BG = "#fdf3e3"; AMBER_BDR = "#e8c97a"
AMBER_BG_DK = "#2e2410"; AMBER_BDR_DK = "#5a4010"
RED    = "#a02020"; RED_BG   = "#fceaea"; RED_BDR   = "#e8b0b0"
RED_BG_DK = "#2e1414"; RED_BDR_DK = "#5a2020"

TEXT_PRIMARY   = "#1a1a1a"
TEXT_SECONDARY = "#5a5a5a"
TEXT_MUTED     = "#9a9a9a"

TEXT_PRIMARY_DK   = "#f2f0eb"
TEXT_SECONDARY_DK = "#9a9a9a"
TEXT_MUTED_DK     = "#6a6a6a"

FONT_SERIF = "'Instrument Serif', serif"
FONT_MONO  = "'DM Mono', monospace"
FONT_SANS  = "'DM Sans', sans-serif"


def _label(text: str, color: str = TEXT_MUTED) -> rx.Component:
    return rx.text(text, font_family=FONT_MONO, font_size="10px",
                   text_transform="uppercase", letter_spacing="0.12em", color=color)


def _score_badge(score: int) -> rx.Component:
    return rx.cond(
        score >= 90,
        rx.box(rx.text(score.to_string() + "/100", font_family=FONT_MONO,
                       font_size="11px", font_weight="500", color=GREEN),
               background=rx.cond(State.is_dark, GREEN_BG_DK, GREEN_BG),
               border=rx.cond(State.is_dark, f"1px solid {GREEN_BDR_DK}", f"1px solid {GREEN_BDR}"),
               padding="3px 10px"),
        rx.cond(
            score >= 55,
            rx.box(rx.text(score.to_string() + "/100", font_family=FONT_MONO,
                           font_size="11px", font_weight="500", color=AMBER),
                   background=rx.cond(State.is_dark, AMBER_BG_DK, AMBER_BG),
                   border=rx.cond(State.is_dark, f"1px solid {AMBER_BDR_DK}", f"1px solid {AMBER_BDR}"),
                   padding="3px 10px"),
            rx.box(rx.text(score.to_string() + "/100", font_family=FONT_MONO,
                           font_size="11px", font_weight="500", color=RED),
                   background=rx.cond(State.is_dark, RED_BG_DK, RED_BG),
                   border=rx.cond(State.is_dark, f"1px solid {RED_BDR_DK}", f"1px solid {RED_BDR}"),
                   padding="3px 10px"),
        ),
    )


def _lang_chip(lang: str) -> rx.Component:
    return rx.box(
        rx.text(lang, font_family=FONT_MONO, font_size="9px",
                color=rx.cond(State.is_dark, TEXT_SECONDARY_DK, TEXT_SECONDARY),
                letter_spacing="0.06em"),
        border=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
        padding="2px 8px",
        background=rx.cond(State.is_dark, BG_CARD_DARK, BG_CARD),
    )


def _detail_panel(record: SubmissionRecord) -> rx.Component:
    return rx.cond(
        State.selected_record_id == record.id,
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.text(record.timestamp, font_family=FONT_MONO,
                                font_size="10px",
                                color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED)),
                        rx.hstack(
                            _lang_chip(record.language),
                            _score_badge(record.score),
                            rx.text(record.score_label, font_family=FONT_MONO,
                                    font_size="10px",
                                    color=rx.cond(State.is_dark, TEXT_SECONDARY_DK, TEXT_SECONDARY)),
                            spacing="2", align="center",
                        ),
                        spacing="1", align="start",
                    ),
                    rx.spacer(),
                    rx.button(
                        rx.text("✕ Close", font_family=FONT_MONO, font_size="10px",
                                text_transform="uppercase", letter_spacing="0.08em",
                                color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED)),
                        on_click=State.close_record,
                        background="transparent",
                        border=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
                        border_radius="0", padding_x="14px", height="32px",
                        cursor="pointer", _hover={"border_color": ACCENT},
                    ),
                    width="100%", align="center",
                ),
                rx.box(height="1px", width="100%",
                       background=rx.cond(State.is_dark, BORDER_DK, BORDER_LT)),
                rx.vstack(
                    _label("Full Code"),
                    rx.box(
                        rx.text(record.full_code, font_family=FONT_MONO,
                                font_size="13px", color="#e8e4dc",
                                white_space="pre-wrap", line_height="1.7"),
                        background=rx.cond(State.is_dark, BG_CODE_DARK, "#1a1a1a"),
                        padding="18px",
                        width="100%", overflow_x="auto",
                    ),
                    spacing="2", align="start", width="100%",
                ),
                rx.grid(
                    rx.vstack(
                        _label("Syntax Check", GREEN),
                        rx.box(
                            rx.text(record.syntax_output, font_family=FONT_MONO,
                                    font_size="13px", color=GREEN,
                                    white_space="pre-wrap", line_height="1.7"),
                            background=rx.cond(State.is_dark, GREEN_BG_DK, GREEN_BG),
                            border=rx.cond(State.is_dark, f"1px solid {GREEN_BDR_DK}", f"1px solid {GREEN_BDR}"),
                            padding="14px", width="100%",
                        ),
                        spacing="2", align="start", width="100%",
                    ),
                    rx.vstack(
                        _label("Detected Issues", AMBER),
                        rx.box(
                            rx.text(record.errors_output, font_family=FONT_MONO,
                                    font_size="13px", color=AMBER,
                                    white_space="pre-wrap", line_height="1.7"),
                            background=rx.cond(State.is_dark, AMBER_BG_DK, AMBER_BG),
                            border=rx.cond(State.is_dark, f"1px solid {AMBER_BDR_DK}", f"1px solid {AMBER_BDR}"),
                            padding="14px", width="100%",
                        ),
                        spacing="2", align="start", width="100%",
                    ),
                    columns="2", spacing="4", width="100%",
                ),
                rx.vstack(
                    _label("AI Suggestions"),
                    rx.box(
                        rx.text(record.ai_output, font_family=FONT_MONO,
                                font_size="13px",
                                color=rx.cond(State.is_dark, TEXT_SECONDARY_DK, TEXT_SECONDARY),
                                white_space="pre-wrap", line_height="1.75"),
                        background=rx.cond(State.is_dark, BG_CARD_DARK, BG_CARD),
                        border=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
                        padding="14px", width="100%",
                    ),
                    spacing="2", align="start", width="100%",
                ),
                rx.cond(
                    record.has_snippets,
                    rx.grid(
                        rx.vstack(
                            _label("Before", RED),
                            rx.box(
                                rx.text(record.before_snippet, font_family=FONT_MONO,
                                        font_size="13px", color=RED,
                                        white_space="pre-wrap", line_height="1.7"),
                                background=rx.cond(State.is_dark, RED_BG_DK, RED_BG),
                                border=rx.cond(State.is_dark, f"1px solid {RED_BDR_DK}", f"1px solid {RED_BDR}"),
                                padding="14px", width="100%",
                            ),
                            spacing="2", align="start", width="100%",
                        ),
                        rx.vstack(
                            _label("After", GREEN),
                            rx.box(
                                rx.text(record.after_snippet, font_family=FONT_MONO,
                                        font_size="13px", color=GREEN,
                                        white_space="pre-wrap", line_height="1.7"),
                                background=rx.cond(State.is_dark, GREEN_BG_DK, GREEN_BG),
                                border=rx.cond(State.is_dark, f"1px solid {GREEN_BDR_DK}", f"1px solid {GREEN_BDR}"),
                                padding="14px", width="100%",
                            ),
                            spacing="2", align="start", width="100%",
                        ),
                        columns="2", spacing="4", width="100%",
                    ),
                    rx.box(),
                ),
                spacing="5", width="100%",
            ),
            padding="22px",
            background=rx.cond(State.is_dark, BG_CARD_DARK, BG_BASE),
            border=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
            border_top="none",
            width="100%",
        ),
        rx.box(),
    )


def _history_row(record: SubmissionRecord) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.text(record.timestamp, font_family=FONT_MONO,
                        font_size="11px",
                        color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED)),
                rx.hstack(
                    _lang_chip(record.language),
                    rx.cond(
                        record.syntax_ok,
                        rx.text("✓ syntax ok", font_family=FONT_MONO,
                                font_size="10px", color=GREEN),
                        rx.text("✗ syntax error", font_family=FONT_MONO,
                                font_size="10px", color=RED),
                    ),
                    rx.text("·", font_family=FONT_MONO,
                            font_size="10px",
                            color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED)),
                    rx.text(record.error_count.to_string() + " issue(s)",
                            font_family=FONT_MONO, font_size="10px",
                            color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED)),
                    spacing="2", align="center",
                ),
                spacing="1", align="start", min_width="170px",
            ),
            rx.box(
                rx.text(record.full_code, font_family=FONT_MONO,
                        font_size="12px",
                        color=rx.cond(State.is_dark, TEXT_SECONDARY_DK, TEXT_SECONDARY),
                        white_space="nowrap", overflow="hidden",
                        text_overflow="ellipsis"),
                flex="1", overflow="hidden", padding_x="20px",
            ),
            rx.hstack(
                _score_badge(record.score),
                rx.cond(
                    State.selected_record_id == record.id,
                    rx.text("▲", font_family=FONT_MONO,
                            font_size="10px", color=ACCENT),
                    rx.text("▼", font_family=FONT_MONO,
                            font_size="10px",
                            color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED)),
                ),
                spacing="3", align="center",
            ),
            spacing="4", align="center", width="100%",
        ),
        padding="16px 20px",
        background=rx.cond(State.is_dark, BG_DARK, BG_BASE),
        border_bottom=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
        transition="background 0.15s",
        cursor="pointer",
        _hover={"background": rx.cond(State.is_dark, BG_CARD_DARK, BG_CARD)},
        on_click=rx.cond(
            State.selected_record_id == record.id,
            State.close_record(),
            State.select_record(record.id),
        ),
        width="100%",
    )


def _history_row_with_detail(record: SubmissionRecord) -> rx.Component:
    return rx.vstack(
        _history_row(record),
        _detail_panel(record),
        width="100%",
    )


def _empty_state() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.text("No submissions yet.", font_family=FONT_SERIF,
                    font_size="22px", font_style="italic",
                    color=rx.cond(State.is_dark, TEXT_SECONDARY_DK, TEXT_SECONDARY)),
            rx.text("Run your first code analysis to see it appear here.",
                    font_family=FONT_SANS, font_size="14px",
                    font_weight="300",
                    color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED)),
            rx.link(
                rx.box(
                    rx.text("Go to Analyzer →", font_family=FONT_MONO,
                            font_size="12px", text_transform="uppercase",
                            letter_spacing="0.08em",
                            color=BG_BASE),  # always light text on dark button
                    background=rx.cond(State.is_dark, "#3a3a3a", TEXT_PRIMARY),  # lighter in dark mode so button is visible
                    padding="12px 22px",
                    margin_top="8px", transition="background 0.15s",
                    _hover={"background": ACCENT},
                ),
                href="/analyzer", text_decoration="none",
            ),
            spacing="3", align="center",
        ),
        padding_y="80px",
    )


def history() -> rx.Component:
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
                rx.box(
                    rx.hstack(
                        rx.vstack(
                            rx.text("Submission History", font_family=FONT_SERIF,
                                    font_size="38px", font_weight="400",
                                    font_style="italic",
                                    color=rx.cond(State.is_dark, TEXT_PRIMARY_DK, TEXT_PRIMARY),
                                    letter_spacing="-0.02em", line_height="1.1"),
                            rx.text("Click any row to expand the full code and AI solution.",
                                    font_family=FONT_SANS, font_size="14px",
                                    font_weight="300",
                                    color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED)),
                            spacing="2", align="start",
                        ),
                        rx.spacer(),
                        rx.cond(
                            State.history.length() > 0,
                            rx.button(
                                rx.text("Clear All", font_family=FONT_MONO,
                                        font_size="10px", text_transform="uppercase",
                                        letter_spacing="0.08em", color=RED),
                                on_click=State.clear_history,
                                background="transparent",
                                border=rx.cond(State.is_dark, f"1px solid {RED_BDR_DK}", f"1px solid {RED_BDR}"),
                                border_radius="0", padding_x="16px",
                                height="34px", cursor="pointer",
                                _hover={"background": rx.cond(State.is_dark, RED_BG_DK, RED_BG)},
                            ),
                            rx.box(),
                        ),
                        width="100%", align="center",
                    ),
                    padding_bottom="28px",
                    border_bottom=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
                    width="100%",
                ),

                rx.cond(
                    State.history.length() > 0,
                    rx.box(
                        rx.hstack(
                            rx.text("Timestamp / Language", font_family=FONT_MONO,
                                    font_size="9px", text_transform="uppercase",
                                    letter_spacing="0.1em",
                                    color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED),
                                    min_width="170px"),
                            rx.text("Code Preview", font_family=FONT_MONO,
                                    font_size="9px", text_transform="uppercase",
                                    letter_spacing="0.1em",
                                    color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED),
                                    flex="1", padding_x="20px"),
                            rx.text("Score", font_family=FONT_MONO,
                                    font_size="9px", text_transform="uppercase",
                                    letter_spacing="0.1em",
                                    color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED)),
                            width="100%", spacing="4",
                        ),
                        padding="10px 20px",
                        background=rx.cond(State.is_dark, BG_CARD_DARK, BG_CARD),
                        border=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
                        border_bottom="none",
                        width="100%",
                    ),
                    rx.box(),
                ),
                rx.cond(
                    State.history.length() > 0,
                    rx.box(
                        rx.vstack(
                            rx.foreach(State.history, _history_row_with_detail),
                            spacing="0", width="100%",
                        ),
                        border=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
                        width="100%",
                    ),
                    _empty_state(),
                ),
                spacing="5", width="100%", max_width="900px",
            ),
            padding="48px 24px",
        ),
        footer(),
        background=rx.cond(State.is_dark, BG_DARK, BG_BASE),
        min_height="100vh",
        width="100%",
        transition="background 0.2s",
    )