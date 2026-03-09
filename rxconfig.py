import reflex as rx

config = rx.Config(
    app_name="AI_Code_Reviewer",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)