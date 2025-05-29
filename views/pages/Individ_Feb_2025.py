import dash
import pandas as pd
from dash import html, dash_table

# Registrér siden
dash.register_page(__name__, path="/individfeb2025", name="Individ_Feb_2025")

# kun de første 5.000 rækker
df = pd.read_excel('models/raw_data/Individ_Feb_2025.xlsx', nrows=5000)

# eller efter indlæsning
df = df.iloc[:5000]

layout = html.Div(
    className="h-[95vh] my-4 mr-4 bg-white bg-opacity-70 rounded-md grid place-content-start",
    style={"overflow": "scroll", "width": "80vw"},
    children=[
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": c, "id": c} for c in df.columns],
        page_size=300,           
        style_cell={"textAlign": "left"}
    )
])