import reflex as rx
from ..state import State
from ..navbar import navbar
from ..footer import footer

BG_BASE      = "#f2f0eb"
BG_DARK      = "#1a1a1a"
BG_CARD      = "#eceae4"
BG_CARD_DARK = "#2a2a2a"
BORDER_LT    = "#d4d0c8"
BORDER_DK    = "#3a3a3a"
ACCENT       = "#c0392b"

GREEN  = "#2d6a1f"; GREEN_BG = "#e8f0e4"; GREEN_BDR = "#b8d4b0"
GREEN_BG_DK = "#1a2e18"; GREEN_BDR_DK = "#2d5228"
BLUE   = "#1e3a5f"; BLUE_BG  = "#e8f0fb"; BLUE_BDR  = "#b0c8e8"

TEXT_PRIMARY   = "#1a1a1a"
TEXT_SECONDARY = "#5a5a5a"
TEXT_MUTED     = "#9a9a9a"

TEXT_PRIMARY_DK   = "#f2f0eb"
TEXT_SECONDARY_DK = "#9a9a9a"
TEXT_MUTED_DK     = "#6a6a6a"

FONT_SERIF = "'Instrument Serif', serif"
FONT_MONO  = "'DM Mono', monospace"
FONT_SANS  = "'DM Sans', sans-serif"

# ── User bubble background: dark in light mode, lighter in dark mode ──
USER_BUBBLE_BG_DARK = "#3a3a3a"   # visible on dark page background


def _label(text: str, color: str = TEXT_MUTED) -> rx.Component:
    return rx.text(text, font_family=FONT_MONO, font_size="10px",
                   text_transform="uppercase", letter_spacing="0.14em", color=color)


def _user_bubble(msg: dict) -> rx.Component:
    return rx.box(
        rx.text(
            msg["content"],
            font_family=FONT_SANS,
            font_size="14px",
            # FIX: text color must contrast against bubble bg in both modes
            color=rx.cond(State.is_dark, TEXT_PRIMARY_DK, BG_BASE),
            line_height="1.7",
            white_space="pre-wrap",
        ),
        # FIX: use a visible bg in dark mode instead of hardcoded #1a1a1a
        background=rx.cond(State.is_dark, USER_BUBBLE_BG_DARK, TEXT_PRIMARY),
        padding="12px 16px",
        max_width="75%",
        align_self="flex-end",
        margin_left="auto",
    )


def _assistant_bubble(msg: dict) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.box(
                rx.text("()", font_family=FONT_MONO, font_size="11px",
                        font_weight="500", color=BG_BASE, line_height="1"),
                background=ACCENT,
                padding="3px 6px",
                border_radius="2px",
                flex_shrink="0",
                margin_top="2px",
            ),
            rx.text(
                msg["content"],
                font_family=FONT_SANS,
                font_size="14px",
                color=rx.cond(State.is_dark, TEXT_PRIMARY_DK, TEXT_PRIMARY),
                line_height="1.75",
                white_space="pre-wrap",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        background=rx.cond(State.is_dark, BG_CARD_DARK, BG_CARD),
        border=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
        padding="12px 16px",
        max_width="85%",
        align_self="flex-start",
    )


def _message_bubble(msg: dict) -> rx.Component:
    return rx.cond(
        msg["role"] == "user",
        _user_bubble(msg),
        _assistant_bubble(msg),
    )


def _context_badge() -> rx.Component:
    return rx.cond(
        State.last_analyzed_code != "",
        rx.hstack(
            rx.box(width="6px", height="6px", background=GREEN,
                   border_radius="50%", flex_shrink="0"),
            rx.text(
                "Context: last analyzed " + State.last_analyzed_language + " code is loaded",
                font_family=FONT_MONO, font_size="10px", color=GREEN,
                letter_spacing="0.04em",
            ),
            spacing="2", align="center",
            padding="6px 12px",
            background=rx.cond(State.is_dark, GREEN_BG_DK, GREEN_BG),
            border=rx.cond(State.is_dark, f"1px solid {GREEN_BDR_DK}", f"1px solid {GREEN_BDR}"),
        ),
        rx.hstack(
            rx.box(width="6px", height="6px", background=TEXT_MUTED,
                   border_radius="50%", flex_shrink="0"),
            rx.text(
                "No code analyzed yet — run an analysis first to give the assistant context",
                font_family=FONT_MONO, font_size="10px",
                color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED),
                letter_spacing="0.04em",
            ),
            spacing="2", align="center",
            padding="6px 12px",
            background=rx.cond(State.is_dark, BG_CARD_DARK, BG_CARD),
            border=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
        ),
    )


def _empty_chat() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.text("Ask me anything about your code.",
                    font_family=FONT_SERIF, font_size="20px",
                    font_style="italic",
                    color=rx.cond(State.is_dark, TEXT_SECONDARY_DK, TEXT_SECONDARY)),
            rx.text(
                "I remember the last code you analyzed. Try asking:\n"
                "\"What does this code do?\", \"How can I optimize it?\", "
                "\"Explain the time complexity\"",
                font_family=FONT_SANS, font_size="13px",
                font_weight="300",
                color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED),
                text_align="center", line_height="1.7",
                max_width="480px",
            ),
            spacing="3", align="center",
        ),
        padding_y="60px",
        width="100%",
    )


def assistant() -> rx.Component:
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

                # ── Header ─────────────────────────────
                rx.box(
                    rx.hstack(
                        rx.vstack(
                            rx.text("AI Assistant",
                                    font_family=FONT_SERIF, font_size="40px",
                                    font_weight="400", font_style="italic",
                                    color=rx.cond(State.is_dark, TEXT_PRIMARY_DK, TEXT_PRIMARY),
                                    letter_spacing="-0.02em", line_height="1.1"),
                            rx.text(
                                "Your coding assistant with memory of your last analyzed code.",
                                font_family=FONT_SANS, font_size="15px",
                                font_weight="300",
                                color=rx.cond(State.is_dark, TEXT_SECONDARY_DK, TEXT_SECONDARY),
                            ),
                            spacing="2", align="start",
                        ),
                        rx.spacer(),
                        rx.cond(
                            State.assistant_messages.length() > 0,
                            rx.button(
                                rx.text("Clear Chat", font_family=FONT_MONO,
                                        font_size="10px", text_transform="uppercase",
                                        letter_spacing="0.08em",
                                        color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED)),
                                on_click=State.clear_assistant,
                                background="transparent",
                                border=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
                                border_radius="0", padding_x="16px",
                                height="34px", cursor="pointer",
                                _hover={"border_color": ACCENT},
                            ),
                            rx.box(),
                        ),
                        width="100%", align="center",
                    ),
                    padding_bottom="24px",
                    border_bottom=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
                    width="100%",
                ),

                # ── Context badge ──────────────────────
                _context_badge(),

                # ── Chat window ────────────────────────
                rx.box(
                    rx.cond(
                        State.assistant_messages.length() > 0,
                        rx.vstack(
                            rx.foreach(State.assistant_messages, _message_bubble),
                            rx.cond(
                                State.assistant_loading,
                                rx.box(
                                    rx.hstack(
                                        rx.spinner(size="2"),
                                        rx.text("Thinking…", font_family=FONT_MONO,
                                                font_size="11px",
                                                color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED)),
                                        spacing="2", align="center",
                                    ),
                                    padding="12px 16px",
                                ),
                                rx.box(),
                            ),
                            spacing="4",
                            align="start",
                            width="100%",
                            padding="20px",
                        ),
                        _empty_chat(),
                    ),
                    border=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
                    # FIX: chat window should use card background, not page background
                    # so it's visually distinct from the page in both light and dark mode
                    background=rx.cond(State.is_dark, BG_CARD_DARK, BG_BASE),
                    min_height="420px",
                    max_height="520px",
                    overflow_y="auto",
                    width="100%",
                ),

                # ── Input row ──────────────────────────
                rx.hstack(
                    rx.text_area(
                        value=State.assistant_input,
                        on_change=State.set_assistant_input,
                        placeholder="Ask about your code, request explanations, optimizations…",
                        height="72px",
                        font_family=FONT_SANS,
                        font_size="14px",
                        background=rx.cond(State.is_dark, BG_CARD_DARK, BG_CARD),
                        color=rx.cond(State.is_dark, TEXT_PRIMARY_DK, TEXT_PRIMARY),
                        border=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
                        border_radius="0",
                        padding="12px 16px",
                        outline="none",
                        _focus={"outline": f"2px solid {ACCENT}"},
                        _placeholder={"color": rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED)},
                        flex="1",
                        resize="none",
                    ),
                    rx.button(
                        rx.cond(
                            State.assistant_loading,
                            rx.spinner(size="2", color=BG_BASE),
                            rx.text("Send →", font_family=FONT_MONO,
                                    font_size="12px", text_transform="uppercase",
                                    letter_spacing="0.08em", color=BG_BASE),
                        ),
                        on_click=State.send_assistant_message,
                        background=ACCENT,
                        border="none", border_radius="0",
                        height="72px", padding_x="26px",
                        cursor="pointer",
                        transition="background 0.15s",
                        _hover={"background": rx.cond(State.is_dark, TEXT_PRIMARY_DK, TEXT_PRIMARY)},
                    ),
                    spacing="0",
                    width="100%",
                    align="stretch",
                ),

                rx.text(
                    "The assistant remembers the last 8 messages and your most recently analyzed code.",
                    font_family=FONT_MONO, font_size="10px",
                    color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED),
                    letter_spacing="0.04em",
                    text_align="center",
                ),

                spacing="5",
                width="100%",
                max_width="900px",
            ),
            padding="48px 24px",
        ),

        footer(),
        background=rx.cond(State.is_dark, BG_DARK, BG_BASE),
        min_height="100vh",
        width="100%",
        transition="background 0.2s",
    )