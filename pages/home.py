# pages/home.py
import datetime
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

total_rykker_2025 = int(df_2025["RykkerSaldoSum"].sum())
total_rykker_2024 = int(df_2024["RykkerSaldoSum"].sum())
rykker_val = total_rykker_2025 - total_rykker_2024

total_payment_2025 = int(df_2025["Payment"].sum())
total_payment_2024 = int(df_2024["Payment"].sum())
earnings = total_payment_2025 - total_payment_2024

total_prem_wifi_2024 = int(df_2024["PremiumWifiCount"].sum())
total_prem_wifi_2025 = int(df_2025["PremiumWifiCount"].sum())
new_prem_customers = total_prem_wifi_2025 - total_prem_wifi_2024

total_access_point_2024 = int(df_2024["AccessPointCount"].sum())
total_access_point_2025 = int(df_2025["AccessPointCount"].sum())
new_acess_points = total_access_point_2025 - total_access_point_2024

total_rykker_1_2024 = int(df_2024["AntalRykker1Sum"].sum())
total_rykker_2_2024 = int(df_2024["AntalRykker2Sum"].sum())
amount_rykker_2024 = total_rykker_1_2024  + total_rykker_2_2024 

total_rykker_1_2025 = int(df_2025["AntalRykker1Sum"].sum())
total_rykker_2_2025 = int(df_2025["AntalRykker2Sum"].sum())
amount_rykker_2025 = total_rykker_1_2025  + total_rykker_2_2025 

new_rykker = amount_rykker_2025 - amount_rykker_2024

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

fig.update_layout(
    height=310,        
    margin=dict(t=80,b=40)
)
fig2.update_layout(
    height=310, 
    margin=dict(t=80,b=40)
)


import datetime
from dash import html, dcc

# År og måneder
years = [{'label': str(y), 'value': y} for y in range(2020, 2026)]
months = [
    {'label': 'Jan', 'value': 1},
    {'label': 'Feb', 'value': 2},
    {'label': 'Mar', 'value': 3},
    {'label': 'Apr', 'value': 4},
    {'label': 'Maj', 'value': 5},
    {'label': 'Jun', 'value': 6},
    {'label': 'Jul', 'value': 7},
    {'label': 'Aug', 'value': 8},
    {'label': 'Sep', 'value': 9},
    {'label': 'Okt', 'value': 10},
    {'label': 'Nov', 'value': 11},
    {'label': 'Dec', 'value': 12},
]

calendars = html.Div(
    children=[
        html.H1(
            "Vælg periode for kundedata",
            className="text-md font-semibold mb-6"
        ),

        html.Div(
            className="flex items-center space-x-12 mb-4",
            children=[

                # Fra
                html.Div(
                    className="flex items-center space-x-2",
                    children=[
                        html.Label("Fra:", className="text-lg font-medium"),
                        dcc.Dropdown(
                            id='year-dropdown-1',
                            options=years,
                            value=datetime.date.today().year,
                            clearable=False,
                            className="w-24"
                        ),
                        dcc.Dropdown(
                            id='month-dropdown-1',
                            options=months,
                            value=datetime.date.today().month,
                            clearable=False,
                            className="w-20"
                        )
                    ]
                ),

                # Til
                html.Div(
                    className="flex items-center space-x-2",
                    children=[
                        html.Label("Til:", className="text-lg font-medium"),
                        dcc.Dropdown(
                            id='year-dropdown-2',
                            options=years,
                            value=datetime.date.today().year,
                            clearable=False,
                            className="w-24"
                        ),
                        dcc.Dropdown(
                            id='month-dropdown-2',
                            options=months,
                            value=datetime.date.today().month,
                            clearable=False,
                            className="w-20"
                        )
                    ]
                ),
            ]
        )
    ],
    className="flex flex-col rounded-t-md p-6 w-full mx-auto bg-white"
)




# --- Card-sektion øverst ---
cards = html.Div(
    className="p-4 w-full  m-auto",
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
            # New Clients
            html.Div(
                className="col-span-12 sm:col-span-6 md:col-span-3",
                children=html.Div(
                    className="flex flex-row bg-white shadow-sm rounded p-4",
                    children=[
                        html.Div("👥", className="flex items-center justify-center h-12 w-12 rounded-xl bg-orange-100 text-orange-500 text-2xl"),
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
            # Orders (statisk)
            html.Div(
                className="col-span-12 sm:col-span-6 md:col-span-3",
                children=html.Div(
                    className="flex flex-row bg-white shadow-sm rounded p-4",
                    children=[
                        html.Div("🧾", className="flex items-center justify-center h-12 w-12 rounded-xl bg-green-100 text-green-500 text-2xl"),
                        html.Div(
                            className="flex flex-col flex-grow ml-4",
                            children=[
                                html.Div("Rykker saldo", className="text-sm text-gray-500"),
                                html.Div(f"Kr. {total_rykker_2025}", className="font-bold text-lg")
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
            # Revenue (statisk)
            html.Div(
                className="col-span-12 sm:col-span-6 md:col-span-3",
                children=html.Div(
                    className="flex flex-row bg-white shadow-sm rounded p-4",
                    children=[
                        html.Div("🛜", className="flex items-center justify-center h-12 w-12 rounded-xl bg-red-100 text-red-500 text-2xl"),
                        html.Div(
                            className="flex flex-col flex-grow ml-4",
                            children=[
                                html.Div("Nye Premium WiFi", className="text-sm text-gray-500"),
                                html.Div(f"{new_prem_customers}", className="font-bold text-lg")
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
                        html.Div("📶", className="flex items-center justify-center h-12 w-12 rounded-xl bg-blue-100 text-red-500 text-2xl"),
                        html.Div(
                            className="flex flex-col flex-grow ml-4",
                            children=[
                                html.Div("Nye Access points", className="text-sm text-gray-500"),
                                html.Div(f"{new_acess_points}", className="font-bold text-lg")
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
                        html.Div("💵", className="flex items-center justify-center h-12 w-12 rounded-xl bg-green-100 text-red-500 text-2xl"),
                        html.Div(
                            className="flex flex-col flex-grow ml-4",
                            children=[
                                html.Div("Nye rykkere", className="text-sm text-gray-500"),
                                html.Div(f"{new_rykker}", className="font-bold text-lg")
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
                        html.Div("", className="flex items-center justify-center h-12 w-12 rounded-xl bg-green-100 text-red-500 text-2xl"),
                        html.Div(
                            className="flex flex-col flex-grow ml-4",
                            children=[
                                html.Div("", className="text-sm text-gray-500"),
                                html.Div("", className="font-bold text-lg")
                            ]
                        )
                    ]
                )
            ),
        ]
    )
)

# --- Hele layoutet ---
layout = html.Div(
    [
        calendars,
        cards,
        html.Div(
            [dcc.Graph(figure=fig), dcc.Graph(figure=fig2)],
            className="grid grid-cols-2 gap-4 p-4 m-auto"
        )
    ],
    className="h-[95vh] my-4 mr-4 bg-white bg-opacity-70 rounded-md grid place-content-start"
)
