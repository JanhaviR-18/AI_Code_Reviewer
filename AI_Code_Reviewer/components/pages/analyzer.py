import reflex as rx
from ..state import State, SUPPORTED_LANGUAGES
from ..navbar import navbar
from ..footer import footer

# ── Design Tokens ─────────────────────────────
BG_BASE   = "#f2f0eb"
BG_DARK   = "#1a1a1a"
BG_CARD   = "#eceae4"
BG_CARD_DARK = "#2a2a2a"
BG_CODE   = "#1a1a1a"
BG_CODE_DARK = "#0d0d0d"
BORDER    = "#1a1a1a"
BORDER_LT = "#d4d0c8"
BORDER_DK = "#3a3a3a"
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

BLUE      = "#1e3a5f"
BLUE_BG   = "#e8f0fb"
BLUE_BDR  = "#b0c8e8"

# Dark mode variants for result blocks
GREEN_BG_DK  = "#1a2e18"
GREEN_BDR_DK = "#2d5228"
AMBER_BG_DK  = "#2e2410"
AMBER_BDR_DK = "#5a4010"
RED_BG_DK    = "#2e1414"
RED_BDR_DK   = "#5a2020"
BLUE_BG_DK   = "#101e30"
BLUE_BDR_DK  = "#1e3a5f"

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
    return rx.text(
        text,
        font_family=FONT_MONO,
        font_size="11px",
        text_transform="uppercase",
        letter_spacing="0.14em",
        color=color,
    )


def _result_block(icon: str, label: str, value, bg_light: str, border_light: str, bg_dark: str, border_dark: str, color: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(icon, font_size="14px"),
                _label(label, color),
                spacing="2", align="center",
            ),
            rx.box(
                rx.text(
                    value,
                    font_family=FONT_MONO,
                    font_size="14px",
                    color=color,
                    white_space="pre-wrap",
                    line_height="1.75",
                    width="100%",
                ),
                background=rx.cond(State.is_dark, bg_dark, bg_light),
                border=rx.cond(
                    State.is_dark,
                    f"1px solid {border_dark}",
                    f"1px solid {border_light}",
                ),
                padding="16px",
                width="100%",
                min_height="72px",
            ),
            spacing="3", align="start", width="100%",
        ),
        width="100%",
    )


def _score_panel() -> rx.Component:
    return rx.box(
        rx.vstack(
            _label(
                "Quality Score",
                rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED),
            ),
            rx.hstack(
                rx.cond(
                    State.style_score >= 90,
                    rx.text(State.style_score.to_string(),
                            font_family=FONT_SERIF, font_size="64px",
                            font_style="italic", color=GREEN, line_height="1"),
                    rx.cond(
                        State.style_score >= 55,
                        rx.text(State.style_score.to_string(),
                                font_family=FONT_SERIF, font_size="64px",
                                font_style="italic", color=AMBER, line_height="1"),
                        rx.text(State.style_score.to_string(),
                                font_family=FONT_SERIF, font_size="64px",
                                font_style="italic", color=RED, line_height="1"),
                    ),
                ),
                rx.vstack(
                    rx.text("/ 100", font_family=FONT_MONO,
                            font_size="13px",
                            color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED)),
                    rx.text(State.score_label, font_family=FONT_MONO,
                            font_size="11px", text_transform="uppercase",
                            letter_spacing="0.06em",
                            color=rx.cond(State.is_dark, TEXT_SECONDARY_DK, TEXT_SECONDARY)),
                    spacing="1", align="start", padding_top="10px",
                ),
                spacing="4", align="end",
            ),
            rx.box(
                rx.box(
                    height="2px",
                    width=State.style_score.to_string() + "%",
                    background=ACCENT,
                    transition="width 0.5s ease",
                ),
                height="2px",
                background=rx.cond(State.is_dark, BORDER_DK, BORDER_LT),
                width="100%",
            ),
            spacing="3", align="start", width="100%",
        ),
        padding="22px 26px",
        background=rx.cond(State.is_dark, BG_CARD_DARK, BG_CARD),
        border=rx.cond(
            State.is_dark,
            f"1px solid {BORDER_DK}",
            f"1px solid {BORDER_LT}",
        ),
        width="100%",
    )


def _time_complexity_panel() -> rx.Component:
    return rx.cond(
        State.has_complexity,
        rx.box(
            rx.vstack(
                _label("Time Complexity", BLUE),
                rx.hstack(
                    # Original complexity box
                    rx.box(
                        rx.vstack(
                            _label("Original", RED),
                            rx.text(
                                State.time_complexity_original,
                                font_family=FONT_MONO,
                                font_size="24px",
                                font_weight="500",
                                color=RED,
                            ),
                            spacing="2", align="start",
                        ),
                        padding="16px 20px",
                        background=rx.cond(State.is_dark, RED_BG_DK, RED_BG),
                        border=rx.cond(
                            State.is_dark,
                            f"1px solid {RED_BDR_DK}",
                            f"1px solid {RED_BDR}",
                        ),
                        flex="1",
                    ),
                    rx.center(
                        rx.text("→", font_family=FONT_MONO,
                                font_size="22px",
                                color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED)),
                        padding_x="16px",
                    ),
                    # Optimized complexity box
                    rx.box(
                        rx.vstack(
                            _label("Optimized", GREEN),
                            rx.text(
                                State.time_complexity_optimized,
                                font_family=FONT_MONO,
                                font_size="24px",
                                font_weight="500",
                                color=GREEN,
                            ),
                            spacing="2", align="start",
                        ),
                        padding="16px 20px",
                        background=rx.cond(State.is_dark, GREEN_BG_DK, GREEN_BG),
                        border=rx.cond(
                            State.is_dark,
                            f"1px solid {GREEN_BDR_DK}",
                            f"1px solid {GREEN_BDR}",
                        ),
                        flex="1",
                    ),
                    spacing="0", align="center", width="100%",
                ),
                # Explanation line (shown when present)
                rx.cond(
                    State.time_complexity_explanation != "",
                    rx.text(
                        State.time_complexity_explanation,
                        font_family=FONT_MONO,
                        font_size="12px",
                        color=rx.cond(State.is_dark, TEXT_SECONDARY_DK, TEXT_SECONDARY),
                        line_height="1.6",
                        padding_top="4px",
                    ),
                    rx.box(),
                ),
                spacing="3", width="100%",
            ),
            padding="20px 24px",
            border=rx.cond(
                State.is_dark,
                f"1px solid {BLUE_BDR_DK}",
                f"1px solid {BLUE_BDR}",
            ),
            background=rx.cond(State.is_dark, BLUE_BG_DK, BLUE_BG),
            width="100%",
        ),
        rx.box(),
    )


def _before_after() -> rx.Component:
    return rx.cond(
        State.has_snippets,
        rx.box(
            rx.vstack(
                rx.hstack(
                    _label("Original / Optimized Code"),
                    rx.box(
                        rx.text("AI Optimized", font_family=FONT_MONO,
                                font_size="10px", color=ACCENT,
                                letter_spacing="0.06em"),
                        border=f"1px solid {ACCENT}",
                        padding="2px 10px",
                    ),
                    spacing="3", align="center",
                ),
                rx.grid(
                    # Before snippet
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.box(width="8px", height="8px",
                                       background=rx.cond(State.is_dark, RED_BG_DK, RED_BG),
                                       border=rx.cond(State.is_dark, f"1px solid {RED_BDR_DK}", f"1px solid {RED_BDR}")),
                                rx.text("Original", font_family=FONT_MONO,
                                        font_size="10px", text_transform="uppercase",
                                        letter_spacing="0.1em", color=RED),
                                spacing="2", align="center",
                            ),
                            rx.box(
                                rx.text(State.before_snippet,
                                        font_family=FONT_MONO, font_size="13px",
                                        color=RED, white_space="pre-wrap",
                                        line_height="1.75"),
                                background=rx.cond(State.is_dark, RED_BG_DK, RED_BG),
                                border=rx.cond(State.is_dark, f"1px solid {RED_BDR_DK}", f"1px solid {RED_BDR}"),
                                padding="14px", width="100%",
                            ),
                            spacing="3", align="start", width="100%",
                        ),
                        width="100%",
                    ),
                    # After snippet
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.box(width="8px", height="8px",
                                       background=rx.cond(State.is_dark, GREEN_BG_DK, GREEN_BG),
                                       border=rx.cond(State.is_dark, f"1px solid {GREEN_BDR_DK}", f"1px solid {GREEN_BDR}")),
                                rx.text("Optimized", font_family=FONT_MONO,
                                        font_size="10px", text_transform="uppercase",
                                        letter_spacing="0.1em", color=GREEN),
                                spacing="2", align="center",
                            ),
                            rx.box(
                                rx.text(State.after_snippet,
                                        font_family=FONT_MONO, font_size="13px",
                                        color=GREEN, white_space="pre-wrap",
                                        line_height="1.75"),
                                background=rx.cond(State.is_dark, GREEN_BG_DK, GREEN_BG),
                                border=rx.cond(State.is_dark, f"1px solid {GREEN_BDR_DK}", f"1px solid {GREEN_BDR}"),
                                padding="14px", width="100%",
                            ),
                            spacing="3", align="start", width="100%",
                        ),
                        width="100%",
                    ),
                    columns="2", spacing="4", width="100%",
                ),
                spacing="4", width="100%",
            ),
            padding="20px 24px",
            border=rx.cond(
                State.is_dark,
                f"1px solid {BORDER_DK}",
                f"1px solid {BORDER_LT}",
            ),
            width="100%",
        ),
        rx.box(),
    )


def analyzer() -> rx.Component:
    return rx.box(

        rx.html("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');
        body { margin: 0; }
        textarea { resize: vertical !important; }
        select {
            appearance: none;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%239a9a9a'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 12px center;
            padding-right: 32px !important;
            cursor: pointer;
        }
        </style>
        """),

        navbar(),

        rx.center(
            rx.vstack(

                # ── Header ─────────────────────────────
                rx.box(
                    rx.vstack(
                        rx.text("Code Analyzer",
                                font_family=FONT_SERIF, font_size="40px",
                                font_weight="400", font_style="italic",
                                color=rx.cond(State.is_dark, TEXT_PRIMARY_DK, TEXT_PRIMARY),
                                letter_spacing="-0.02em",
                                line_height="1.1"),
                        rx.text(
                            "Select a language, paste or upload code, and get instant AI feedback.",
                            font_family=FONT_SANS, font_size="15px",
                            font_weight="300",
                            color=rx.cond(State.is_dark, TEXT_SECONDARY_DK, TEXT_SECONDARY)),
                        spacing="2", align="start",
                    ),
                    padding_bottom="28px",
                    border_bottom=rx.cond(
                        State.is_dark,
                        f"1px solid {BORDER_DK}",
                        f"1px solid {BORDER_LT}",
                    ),
                    width="100%",
                ),

                # ── Language row ───────────────────────
                rx.hstack(
                    rx.vstack(
                        _label("Language"),
                        rx.select(
                            SUPPORTED_LANGUAGES,
                            value=State.language,
                            on_change=State.set_language,
                            font_family=FONT_MONO,
                            font_size="13px",
                            color=rx.cond(State.is_dark, TEXT_PRIMARY_DK, TEXT_PRIMARY),
                            background=rx.cond(State.is_dark, BG_CARD_DARK, BG_CARD),
                            border=rx.cond(
                                State.is_dark,
                                f"1px solid {BORDER_DK}",
                                f"1px solid {BORDER_LT}",
                            ),
                            border_radius="0",
                            padding="10px 14px",
                            height="44px",
                            width="200px",
                            _focus={"outline": f"2px solid {ACCENT}"},
                        ),
                        spacing="2", align="start",
                    ),
                    spacing="6", align="end", width="100%",
                ),

                # ── Code editor ────────────────────────
                rx.vstack(
                    rx.hstack(
                        _label("Code Input"),
                        rx.spacer(),
                        rx.cond(
                            State.user_code != "",
                            rx.text("● ready", font_family=FONT_MONO,
                                    font_size="10px", color=GREEN,
                                    letter_spacing="0.06em"),
                            rx.text("○ empty", font_family=FONT_MONO,
                                    font_size="10px",
                                    color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED),
                                    letter_spacing="0.06em"),
                        ),
                        width="100%",
                    ),
                    rx.text_area(
                        value=State.user_code,
                        on_change=State.set_user_code,
                        placeholder="# Paste your code here…",
                        height="280px",
                        width="100%",
                        font_family=FONT_MONO,
                        font_size="14px",
                        background=rx.cond(State.is_dark, BG_CODE_DARK, BG_CODE),
                        color="#e8e4dc",
                        border="none",
                        border_radius="0",
                        padding="18px",
                        outline="none",
                        _focus={"outline": f"2px solid {ACCENT}"},
                        _placeholder={"color": "#4a4a4a"},
                    ),
                    spacing="3", width="100%",
                ),

                # ── Upload ─────────────────────────────
                rx.hstack(
                    rx.text("or upload a file:", font_family=FONT_MONO,
                            font_size="10px",
                            color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED),
                            text_transform="uppercase", letter_spacing="0.08em"),
                    rx.upload(
                        rx.box(
                            rx.text(
                                "↑ .py / .c / .cpp / .java / .js / .sql",
                                font_family=FONT_MONO,
                                font_size="10px",
                                color=rx.cond(State.is_dark, TEXT_SECONDARY_DK, TEXT_SECONDARY),
                                text_transform="uppercase",
                                letter_spacing="0.06em",
                            ),
                            padding="6px 14px",
                            border=rx.cond(
                                State.is_dark,
                                f"1px solid {BORDER_DK}",
                                f"1px solid {BORDER_LT}",
                            ),
                            background=rx.cond(State.is_dark, BG_CARD_DARK, BG_CARD),
                            display="flex",
                            align_items="center",
                            cursor="pointer",
                            transition="border-color 0.15s",
                            _hover={"border_color": ACCENT},
                        ),
                        on_drop=State.handle_upload(
                            rx.upload_files(upload_id="code_upload")
                        ),
                        id="code_upload",
                        multiple=False,
                        accept={
                            "text/x-python":   [".py"],
                            "text/x-csrc":     [".c"],
                            "text/x-c++src":   [".cpp"],
                            "text/x-java":     [".java"],
                            "text/javascript": [".js"],
                            "application/sql": [".sql"],
                        },
                    ),
                    rx.cond(
                        State.upload_error != "",
                        rx.text(State.upload_error, font_family=FONT_MONO,
                                font_size="11px", color=RED),
                        rx.box(),
                    ),
                    spacing="3", align="center",
                ),

                # ── Buttons ────────────────────────────
                rx.hstack(
                    rx.button(
                        rx.cond(
                            State.is_loading,
                            rx.hstack(
                                rx.spinner(size="2", color=BG_BASE),
                                rx.text("Analyzing…", font_family=FONT_MONO,
                                        font_size="12px", text_transform="uppercase",
                                        letter_spacing="0.08em", color=BG_BASE),
                                spacing="2", align="center",
                            ),
                            rx.text("⚡ Analyze Code", font_family=FONT_MONO,
                                    font_size="12px", text_transform="uppercase",
                                    letter_spacing="0.08em", color=BG_BASE),
                        ),
                        on_click=State.analyze_code,
                        background=ACCENT,
                        border="none", border_radius="0",
                        height="44px", padding_x="26px",
                        cursor="pointer",
                        transition="background 0.15s",
                        _hover={"background": TEXT_PRIMARY},
                    ),
                   
                    spacing="3",
                ),

                # ── Score Panel ────────────────────────
                _score_panel(),

                # ── Syntax + Issues grid ───────────────
                rx.grid(
                    _result_block("✓", "Syntax Check",
                                  State.syntax_output,
                                  GREEN_BG, GREEN_BDR,
                                  GREEN_BG_DK, GREEN_BDR_DK,
                                  GREEN),
                    _result_block("⚠", "Detected Issues",
                                  State.errors_output,
                                  AMBER_BG, AMBER_BDR,
                                  AMBER_BG_DK, AMBER_BDR_DK,
                                  AMBER),
                    columns="2", spacing="4", width="100%",
                ),

                

                # ── AI Suggestions ─────────────────────
                rx.vstack(
                    _label("AI Suggestions"),
                    rx.text_area(
                        value=State.ai_output,
                        is_read_only=True,
                        height="200px", width="100%",
                        font_family=FONT_MONO, font_size="14px",
                        color=rx.cond(State.is_dark, TEXT_SECONDARY_DK, TEXT_SECONDARY),
                        background=rx.cond(State.is_dark, BG_CARD_DARK, BG_CARD),
                        border=rx.cond(
                            State.is_dark,
                            f"1px solid {BORDER_DK}",
                            f"1px solid {BORDER_LT}",
                        ),
                        border_radius="0", padding="16px",
                        line_height="1.75",
                    ),
                    spacing="3", width="100%",
                ),
                # ── Time Complexity Panel ──────────────
                _time_complexity_panel(),
                # ── Before / After ─────────────────────
                _before_after(),

                spacing="6", width="100%", max_width="900px",
            ),
            
            padding="48px 24px",
        ),

        footer(),
        background=rx.cond(State.is_dark, BG_DARK, BG_BASE),
        min_height="100vh",
        width="100%",
        transition="background 0.2s",
    )