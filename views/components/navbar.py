from dash import Dash, html, dcc
import dash

# Debug print

pages = [
    {
        "name": "Aktive kunder Feb 2025",
        "path": "/activefeb2025"
    },
    {
        "name": "Aktive kunder Nov 2024",
        "path": "/activenov2024"
    },
    {
        "name": "Churn kunder Feb 2025",
        "path": "/churnfeb2025" 
    },
    {
        "name": "Churn kunder Nov 2024",
        "path": "/churnnov2024"
    },
    {
        "name": "Individ kunder Feb 2025",
        "path": "/individfeb2025"
    },
    {
        "name": "Individ kunder Nov 2024",
        "path": "/individnov2024"
    }
]

navbar = html.Div( 
    className="flex flex-col bg-white shadow-md bg-opacity-[60] min-w-56 h-[95vh] m-4 p-4 rounded-md",
    children=[
        # Altid synlige links
        html.Img(
            src="https://eu.eu-supply.com/img/brandings/Ewii_left.png",
            className="h-12 w-auto mb-6 mr-auto ml-4 "
        ),        
        dcc.Link("Home", href="/", className="block px-4 py-2 rounded hover:bg-gray-200"),
        dcc.Link("Oversigt", href="/oversigt", className="block px-4 py-2 rounded hover:bg-gray-200"),

        # Collapsible "Data sider" sektion
        html.Details(
            className="group mt-4",
            children=[
                html.Summary(
                    className=(
                        "flex items-center justify-between px-4 py-2 rounded "
                        "cursor-pointer hover:bg-gray-200 transition"
                    ),
                    children=[
                        html.Span("Data sider"),
                        # Pil-ikon som roterer når sektionen er åben
                        html.Span(
                            "▶",
                            className="transform transition-transform duration-200 group-open:rotate-90"
                        ),
                    ]
                ),
                # Indrykket liste af data-sider
                html.Div(
                    className="pl-6 mt-2 flex flex-col text-sm space-y-1",
                    children=[
                        dcc.Link(
                            page["name"],
                            href=page["path"],
                            className="block px-2 py-1 rounded hover:bg-gray-200 transition"
                        )
                        for page in pages
                    ]
                )
            ]
        )
    ]
)