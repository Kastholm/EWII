import dash
from dash import html

dash.register_page(__name__, path="/oversigt", name="Oversigt")

layout = html.Div([
    html.H1("hello")
])
