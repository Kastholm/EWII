import dash
import pandas as pd
from dash import html, dash_table

# Registrér siden
dash.register_page(__name__, path="/churnnov2024", name="Churn_Nov_2024")

# kun de første 5.000 rækker
df = pd.read_excel('data/Churn_nov_2024.xlsx', nrows=5000)

# eller efter indlæsning
df = df.iloc[:5000]

layout = html.Div([
    dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": c, "id": c} for c in df.columns],
        page_size=300,              # sæt selv antal rækker per side
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left"}
    )
])