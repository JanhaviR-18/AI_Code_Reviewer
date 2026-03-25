import reflex as rx

# ── Design Tokens ─────────────────────────────
BG_BASE   = "#f2f0eb"
BG_CARD   = "#eceae4"
BORDER    = "#1a1a1a"
BORDER_LT = "#d4d0c8"
ACCENT    = "#c0392b"

TEXT_PRIMARY   = "#1a1a1a"
TEXT_SECONDARY = "#5a5a5a"
TEXT_MUTED     = "#757575"

FONT_SERIF = "'Instrument Serif', serif"
FONT_MONO  = "'DM Mono', monospace"
FONT_SANS  = "'DM Sans', sans-serif"


def _footer_link(label: str, href: str) -> rx.Component:
    return rx.link(
        rx.text(
            label,
            font_family=FONT_MONO,
            font_size="10px",
            text_transform="uppercase",
            letter_spacing="0.08em",
            color=TEXT_MUTED,
            transition="color 0.15s",
        ),
        href=href,
        text_decoration="none",
        _hover={"color": TEXT_PRIMARY},
    )
def _footer_link2(label: str, href: str) -> rx.Component:
    return rx.link(
        rx.text(
            label,
            font_family=FONT_MONO,
            font_size="10px",
            text_transform="uppercase",
            letter_spacing="0.08em",
            color=TEXT_PRIMARY,
            transition="color 0.15s",
        ),
        href=href,
        text_decoration="none",
        _hover={"color": TEXT_PRIMARY},
    )


def footer() -> rx.Component:
    return rx.box(

        # Top border line
        rx.box(height="2px", width="100%", background=BORDER),

        rx.box(
            rx.hstack(

                # Left: branding
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            "Code",
                            font_family=FONT_SERIF,
                            font_size="16px",
                            color=TEXT_PRIMARY,
                            letter_spacing="-0.01em",
                        ),
                        rx.text(
                            "Reviewer",
                            font_family=FONT_SERIF,
                            font_size="16px",
                            font_style="italic",
                            color=ACCENT,
                            letter_spacing="-0.01em",
                        ),
                        rx.text(
                            "()",
                            font_family=FONT_SERIF,
                            font_size="16px",
                            color=TEXT_PRIMARY,
                            letter_spacing="-0.01em",
                        ),
                        spacing="0",
                    ),
                    rx.text(
                        "AI-Based Python Code Reviewer and Analyzer",
                        font_family=FONT_SANS,
                        font_size="12px",
                        font_weight="300",
                        color=TEXT_MUTED,
                        max_width="280px",
                        line_height="1.6",
                    ),
                    spacing="2",
                    align="start",
                ),

                rx.spacer(),

                # Right: page navigation
                rx.hstack(
                    rx.text(
                        "Navigate",
                        font_family=FONT_MONO,
                        font_size="9px",
                        text_transform="uppercase",
                        letter_spacing="0.14em",
                        color=TEXT_MUTED,
                    ),
                    rx.hstack(
                        _footer_link2("Home", "/"),
                        _footer_link2("Analyzer", "/analyzer"),
                        _footer_link2("History", "/history"),
                        _footer_link2("About", "/about"),
                        spacing="5",
                        align="center",
                    ),
                    spacing="3",
                    align="center",
                ),

                spacing="8",
                align="center",
                width="100%",
                flex_wrap="wrap",
                gap="32px",
            ),
            padding="40px",
            max_width="900px",
            margin="0 auto",
        ),

        # Bottom bar
        rx.box(
            rx.hstack(
                rx.text(
                    "© 2026 AICodeReview — AI-Driven Code Reviewer",
                    font_family=FONT_MONO,
                    font_size="10px",
                    color=TEXT_MUTED,
                    letter_spacing="0.04em",
                ),
                rx.spacer(),
                rx.text(
                    "Built with: Reflex · Python · Groq · AST",
                    font_family=FONT_MONO,
                    font_size="10px",
                    color=TEXT_MUTED,
                    letter_spacing="0.04em",
                ),
                width="100%",
                align="center",
                flex_wrap="wrap",
                gap="8px",
            ),
            padding="16px 40px",
            border_top=f"1px solid {BORDER_LT}",
            background=BG_CARD,
        ),

        background=BG_BASE,
        width="100%",
    )