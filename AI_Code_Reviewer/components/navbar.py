import reflex as rx

# ── Design Tokens ─────────────────────────────
BG_BASE    = "#f2f0eb"
BORDER     = "#1a1a1a"
ACCENT     = "#c0392b"

TEXT_PRIMARY   = "#1a1a1a"
TEXT_SECONDARY = "#5a5a5a"
TEXT_MUTED     = "#9a9a9a"

FONT_SERIF   = "'Instrument Serif', serif"
FONT_MONO    = "'DM Mono', monospace"
FONT_SANS    = "'DM Sans', sans-serif"


def _nav_link(label: str, href: str) -> rx.Component:
    return rx.link(
        rx.text(
            label,
            font_family=FONT_MONO,
            font_size="11px",
            text_transform="uppercase",
            letter_spacing="0.08em",
            color=TEXT_SECONDARY,
            transition="color 0.15s",
        ),
        href=href,
        text_decoration="none",
        _hover={"color": TEXT_PRIMARY},
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
                        font_size="19px",
                        color=TEXT_PRIMARY,
                        letter_spacing="-0.01em",
                    ),
                    rx.text(
                        "Reviewer",
                        font_family=FONT_SERIF,
                        font_size="19px",
                        font_style="italic",
                        color=ACCENT,
                        letter_spacing="-0.01em",
                    ),
                      rx.text(
                        "()",
                        font_family=FONT_SERIF,
                        font_size="19px",
                        color=TEXT_PRIMARY,
                        letter_spacing="-0.01em",
                    ),
                    spacing="0",
                ),
                href="/",
                text_decoration="none",
            ),

            rx.spacer(),

            # Nav links
            rx.hstack(
                _nav_link("Home", "/"),
                _nav_link("Analyzer", "/analyzer"),
                _nav_link("History", "/history"),
                _nav_link("About", "/about"),
                spacing="7",
                align="center",
            ),

            width="100%",
            align="center",
            padding="0 40px",
            height="54px",
        ),

        width="100%",
        background=BG_BASE,
        border_bottom=f"2px solid {BORDER}",
        position="sticky",
        top="0",
        z_index="100",
    )