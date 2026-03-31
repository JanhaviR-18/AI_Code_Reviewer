import reflex as rx
from .components.pages.index import index
from .components.pages.analyzer import analyzer
from .components.pages.about import about
from .components.pages.history import history
from .components.pages.assistant import assistant

FONT_URL = (
    "https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500"
    "&family=Instrument+Serif:ital@0;1"
    "&family=DM+Sans:wght@300;400;500&display=swap"
)

app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=False,
        radius="none",
        accent_color="red",
    ),
    stylesheets=[FONT_URL],
    style={
        "font_family": "'DM Sans', sans-serif",
        "background_color": "#f2f0eb",
        "margin": "0",
        "padding": "0",
        "box_sizing": "border-box",
    },
)

app.add_page(index,     route="/")
app.add_page(analyzer,  route="/analyzer")
app.add_page(assistant, route="/assistant")
app.add_page(about,     route="/about")
app.add_page(history,   route="/history")