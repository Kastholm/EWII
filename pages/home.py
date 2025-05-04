# pages/home.py
import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path="/", name="Hjem")

# --- Data & grafer som før ---
df_2024 = pd.read_json("data/percent_internet_option/internet_distribution_2024.json")
df_2025 = pd.read_json("data/percent_internet_option/internet_distribution_2025.json")

# Beregn totals og nye kunder
total_2025 = int(df_2025["Count"].sum())
total_2024 = int(df_2024["Count"].sum())
new_clients = total_2025 - total_2024

total_payment_2025 = int(df_2025["Payment"].sum())
total_payment_2024 = int(df_2024["Payment"].sum())
earnings = total_payment_2025 - total_payment_2024


fig = px.pie(
    df_2024,
    names="Kontraktnavn",
    values="Count",
    custom_data=["Percent"],
    title="Fordeling af internet November 2024"
)
fig.update_traces(
    textposition="inside",
    texttemplate="%{label}<br>Kunder: %{value}<br>%{customdata[0]:.1f}%",
    hovertemplate="<b>%{label}</b><br>Kunder: %{value}<br>Andel: %{percent:.1%}<extra></extra>"
)

fig2 = px.pie(
    df_2025,
    names="Kontraktnavn",
    values="Count",
    custom_data=["Percent"],
    title="Fordeling af internet Februar 2025"
)
fig2.update_traces(
    textposition="inside",
    texttemplate="%{label}<br>Kunder: %{value}<br>%{customdata[0]:.1f}%",
    hovertemplate="<b>%{label}</b><br>Kunder: %{value}<br>Andel: %{percent:.1%}<extra></extra>"
)

# --- Card-sektion øverst ---
cards = html.Div(
    className="p-4 w-full",
    children=html.Div(
        className="grid grid-cols-12 gap-4",
        children=[
            # Users
            html.Div(
                className="col-span-12 sm:col-span-6 md:col-span-3",
                children=html.Div(
                    className="flex flex-row bg-white shadow-sm rounded p-4",
                    children=[
                        html.Div("👥", className="flex items-center justify-center h-12 w-12 rounded-xl bg-blue-100 text-blue-500 text-2xl"),
                        html.Div(
                            className="flex flex-col flex-grow ml-4",
                            children=[
                                html.Div("Nuværende kunder", className="text-sm text-gray-500"),
                                html.Div(f"{total_2025}", className="font-bold text-lg")
                            ]
                        )
                    ]
                )
            ),
            # Orders (statisk)
            html.Div(
                className="col-span-12 sm:col-span-6 md:col-span-3",
                children=html.Div(
                    className="flex flex-row bg-white shadow-sm rounded p-4",
                    children=[
                        html.Div("🛒", className="flex items-center justify-center h-12 w-12 rounded-xl bg-green-100 text-green-500 text-2xl"),
                        html.Div(
                            className="flex flex-col flex-grow ml-4",
                            children=[
                                html.Div("Orders", className="text-sm text-gray-500"),
                                html.Div("230", className="font-bold text-lg")
                            ]
                        )
                    ]
                )
            ),
            # New Clients
            html.Div(
                className="col-span-12 sm:col-span-6 md:col-span-3",
                children=html.Div(
                    className="flex flex-row bg-white shadow-sm rounded p-4",
                    children=[
                        html.Div("➕", className="flex items-center justify-center h-12 w-12 rounded-xl bg-orange-100 text-orange-500 text-2xl"),
                        html.Div(
                            className="flex flex-col flex-grow ml-4",
                            children=[
                                html.Div("Nye kunder", className="text-sm text-gray-500"),
                                html.Div(f"{new_clients}", className="font-bold text-lg")
                            ]
                        )
                    ]
                )
            ),
            # Revenue (statisk)
            html.Div(
                className="col-span-12 sm:col-span-6 md:col-span-3",
                children=html.Div(
                    className="flex flex-row bg-white shadow-sm rounded p-4",
                    children=[
                        html.Div("💰", className="flex items-center justify-center h-12 w-12 rounded-xl bg-red-100 text-red-500 text-2xl"),
                        html.Div(
                            className="flex flex-col flex-grow ml-4",
                            children=[
                                html.Div("Indtjening", className="text-sm text-gray-500"),
                                html.Div(f"Kr. {earnings}", className="font-bold text-lg")
                            ]
                        )
                    ]
                )
            ),
        ]
    )
)

# --- Hele layoutet ---
layout = html.Div([
    html.H1("Dashboard Hjem", className="p-4"),
    cards,
    html.Div(
        [dcc.Graph(figure=fig), dcc.Graph(figure=fig2)],
        className="grid grid-cols-2 gap-4 p-4"
    )
])
