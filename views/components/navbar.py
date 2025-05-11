from dash import Dash, html, dcc
import dash

navbar = html.Div(
    className="flex flex-col bg-white shadow-md bg-opacity-[60] min-w-56 h-[95vh] m-4 p-4 rounded-md",
    children=[
        # Altid synlige links
        html.Img(
            src="https://w7.pngwing.com/pngs/1003/600/png-transparent-ewii-fuel-cells-kif-kolding-k%C3%B8benhavn-car-electric-vehicle-car-angle-text-trademark.png",
            className="h-12 w-auto mb-6 mr-auto ml-4 "
        ),        
        dcc.Link("Home", href="/", className="block px-4 py-2 rounded hover:bg-gray-200"),
        dcc.Link("Oversigt", href="/oversigt", className="block px-4 py-2 rounded hover:bg-gray-200"),

        # Collapsible “Data sider” sektion
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
                    className="pl-6 mt-2 flex flex-col space-y-1",
                    children=[
                        dcc.Link(
                            page["name"],
                            href=page["path"],
                            className="block px-2 py-1 rounded hover:bg-gray-200 transition"
                        )
                        for page in dash.page_registry.values()
                        if page["path"] not in ["/", "/oversigt"]
                    ]
                )
            ]
        )
    ]
)