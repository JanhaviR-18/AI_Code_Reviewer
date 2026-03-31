import reflex as rx
from .state import State

# ── Design Tokens ─────────────────────────────
BG_BASE      = "#f2f0eb"
BG_DARK      = "#1a1a1a"
BG_CARD      = "#eceae4"
BG_CARD_DARK = "#2a2a2a"
BORDER       = "#1a1a1a"
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

LANGUAGES = ["Python", "C", "C++", "Java", "JavaScript", "SQL"]


def _footer_link(label: str, href: str) -> rx.Component:
    return rx.link(
        rx.text(
            label,
            font_family=FONT_MONO,
            font_size="10px",
            text_transform="uppercase",
            letter_spacing="0.08em",
            color=rx.cond(State.is_dark, TEXT_SECONDARY_DK, TEXT_SECONDARY),
            transition="color 0.15s",
        ),
        href=href,
        text_decoration="none",
        _hover={"color": ACCENT},
    )


def _lang_tag(name: str) -> rx.Component:
    return rx.box(
        rx.text(
            name,
            font_family=FONT_MONO,
            font_size="9px",
            letter_spacing="0.06em",
            color=rx.cond(State.is_dark, TEXT_SECONDARY_DK, TEXT_SECONDARY),
        ),
        padding="3px 10px",
        border=rx.cond(State.is_dark, f"1px solid {BORDER_DK}", f"1px solid {BORDER_LT}"),
        background=rx.cond(State.is_dark, BG_CARD_DARK, BG_CARD),
    )


def _quick_action(icon: str, label: str, href: str, accent: bool = False) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.text(icon, font_size="11px"),
            rx.text(
                label,
                font_family=FONT_MONO,
                font_size="10px",
                text_transform="uppercase",
                letter_spacing="0.07em",
                color=ACCENT if accent else rx.cond(State.is_dark, TEXT_PRIMARY_DK, TEXT_PRIMARY),
            ),
            spacing="2",
            align="center",
        ),
        href=href,
        text_decoration="none",
        opacity="1",
        transition="opacity 0.15s",
        _hover={"opacity": "0.65"},
    )


def footer() -> rx.Component:
    return rx.box(

        # ── Top border ────────────────────────────
        rx.box(
            height="2px",
            width="100%",
            background=rx.cond(State.is_dark, BORDER_DK, BORDER),
        ),

        # ── Main footer body ──────────────────────
        rx.box(
            rx.hstack(

                # ── Left: branding + tagline + languages ──
                rx.vstack(
                    rx.hstack(
                        rx.text("Code", font_family=FONT_SERIF, font_size="16px",
                                color=rx.cond(State.is_dark, TEXT_PRIMARY_DK, TEXT_PRIMARY),
                                letter_spacing="-0.01em"),
                        rx.text("Reviewer", font_family=FONT_SERIF, font_size="16px",
                                font_style="italic", color=ACCENT, letter_spacing="-0.01em"),
                        rx.text("()", font_family=FONT_SERIF, font_size="16px",
                                color=rx.cond(State.is_dark, TEXT_PRIMARY_DK, TEXT_PRIMARY),
                                letter_spacing="-0.01em"),
                        spacing="0",
                    ),
                    rx.text(
                        "Paste code. Get instant AI-powered feedback on syntax, "
                        "bugs, style and time complexity.",
                        font_family=FONT_SANS,
                        font_size="12px",
                        font_weight="300",
                        color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED),
                        max_width="300px",
                        line_height="1.65",
                    ),
                    rx.vstack(
                        rx.text(
                            "Supports",
                            font_family=FONT_MONO,
                            font_size="9px",
                            text_transform="uppercase",
                            letter_spacing="0.14em",
                            color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED),
                        ),
                        rx.hstack(
                            *[_lang_tag(lang) for lang in LANGUAGES],
                            spacing="2",
                            flex_wrap="wrap",
                        ),
                        spacing="2",
                        align="start",
                    ),
                    spacing="4",
                    align="start",
                ),

                rx.spacer(),

                # ── Right: Navigate + Quick Actions (both horizontal) ──
                rx.vstack(
                    # Navigate row
                    rx.vstack(
                        rx.text(
                            "Navigate",
                            font_family=FONT_MONO,
                            font_size="9px",
                            text_transform="uppercase",
                            letter_spacing="0.14em",
                            color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED),
                        ),
                        rx.hstack(
                            _footer_link("Home", "/"),
                            _footer_link("Analyzer", "/analyzer"),
                            _footer_link("Assistant", "/assistant"),
                            _footer_link("History", "/history"),
                            _footer_link("About", "/about"),
                            spacing="5",
                            align="center",
                            flex_wrap="wrap",
                        ),
                        spacing="3",
                        align="start",
                    ),

                    # Quick Actions row
                    rx.vstack(
                        rx.text(
                            "Quick Actions",
                            font_family=FONT_MONO,
                            font_size="9px",
                            text_transform="uppercase",
                            letter_spacing="0.14em",
                            color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED),
                        ),
                        rx.hstack(
                            _quick_action("+", "Analyze Code", "/analyzer"),
                            _quick_action("?", "Ask Assistant", "/assistant"),
                            _quick_action("*", "View History", "/history"),
                            spacing="5",
                            align="center",
                            flex_wrap="wrap",
                        ),
                        spacing="3",
                        align="start",
                    ),

                    spacing="5",
                    align="start",
                ),

                spacing="8",
                align="start",
                width="100%",
                flex_wrap="wrap",
                gap="40px",
            ),
            padding="44px 40px 36px",
            max_width="960px",
            margin="0 auto",
        ),

        # ── Bottom bar ────────────────────────────
        rx.box(
            rx.hstack(
                rx.text(
                    "© 2026 AICodeReview — AI-Driven Code Reviewer",
                    font_family=FONT_MONO,
                    font_size="10px",
                    color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED),
                    letter_spacing="0.04em",
                ),
                rx.spacer(),
                rx.text(
                    "Built with: Reflex · Python · Groq · AST",
                    font_family=FONT_MONO,
                    font_size="10px",
                    color=rx.cond(State.is_dark, TEXT_MUTED_DK, TEXT_MUTED),
                    letter_spacing="0.04em",
                ),
                width="100%",
                align="center",
                flex_wrap="wrap",
                gap="8px",
            ),
            padding="16px 40px",
            border_top=rx.cond(
                State.is_dark,
                f"1px solid {BORDER_DK}",
                f"1px solid {BORDER_LT}",
            ),
            background=rx.cond(State.is_dark, BG_CARD_DARK, BG_CARD),
        ),

        background=rx.cond(State.is_dark, BG_DARK, BG_BASE),
        width="100%",
        transition="background 0.2s",
    )