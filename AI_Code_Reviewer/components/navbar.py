import reflex as rx
from .state import State

BG_BASE  = "#f2f0eb"
BG_DARK  = "#1a1a1a"
BORDER   = "#1a1a1a"
ACCENT   = "#c0392b"

TEXT_PRIMARY   = "#1a1a1a"
TEXT_SECONDARY = "#5a5a5a"

FONT_SERIF = "'Instrument Serif', serif"
FONT_MONO  = "'DM Mono', monospace"


def _nav_link(label: str, href: str) -> rx.Component:
    # Use Reflex's built-in router to get the current page path
    is_active = State.router.page.path == href
    return rx.link(
        rx.box(
            rx.text(
                label,
                font_family=FONT_MONO,
                font_size="11px",
                text_transform="uppercase",
                letter_spacing="0.08em",
                color=rx.cond(
                    is_active,
                    ACCENT,
                    rx.cond(State.is_dark, "#9a9a9a", TEXT_SECONDARY),
                ),
                transition="color 0.15s",
            ),
            # Active underline indicator
            border_bottom=rx.cond(
                is_active,
                f"1.5px solid {ACCENT}",
                "1.5px solid transparent",
            ),
            padding_bottom="2px",
        ),
        href=href,
        text_decoration="none",
        _hover={"opacity": "0.75"},
    )


def _theme_toggle() -> rx.Component:
    return rx.box(
        rx.cond(
            State.is_dark,
            rx.text("☀", font_size="14px", color="#f2f0eb"),
            rx.text("☾", font_size="14px", color=TEXT_PRIMARY),
        ),
        on_click=State.toggle_theme,
        padding="6px 10px",
        border=rx.cond(
            State.is_dark,
            "1.5px solid #3a3a3a",
            f"1.5px solid {BORDER}",
        ),
        cursor="pointer",
        transition="all 0.15s",
        _hover={"background": rx.cond(State.is_dark, "#2a2a2a", "#eceae4")},
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            # Logo
            rx.link(
                rx.hstack(
                    rx.text(
                        "Code",
                        font_family=FONT_SERIF,
                        font_size="24px",
                        color=rx.cond(State.is_dark, BG_BASE, TEXT_PRIMARY),
                        letter_spacing="-0.01em",
                    ),
                    rx.text(
                        "Reviewer",
                        font_family=FONT_SERIF,
                        font_size="24px",
                        font_style="italic",
                        color=ACCENT,
                        letter_spacing="-0.01em",
                    ),
                    rx.text(
                        "()",
                        font_family=FONT_SERIF,
                        font_size="24px",
                        color=rx.cond(State.is_dark, BG_BASE, TEXT_PRIMARY),
                        letter_spacing="-0.01em",
                    ),
                    spacing="0",
                ),
                href="/",
                text_decoration="none",
            ),

            rx.spacer(),

            rx.hstack(
                _nav_link("Home", "/"),
                _nav_link("Analyzer", "/analyzer"),
                _nav_link("Assistant", "/assistant"),
                _nav_link("History", "/history"),
                _nav_link("About", "/about"),
                spacing="7",
                align="center",
            ),

            rx.box(width="16px"),
            _theme_toggle(),

            width="100%",
            align="center",
            padding="0 40px",
            height="54px",
        ),

        width="100%",
        background=rx.cond(State.is_dark, BG_DARK, BG_BASE),
        border_bottom=rx.cond(
            State.is_dark,
            "2px solid #2a2a2a",
            f"2px solid {BORDER}",
        ),
        position="sticky",
        top="0",
        z_index="100",
        transition="background 0.2s",
    )