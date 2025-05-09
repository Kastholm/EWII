from dash import Dash, html, dcc, Input, Output, State, callback_context
import dash
import json
from components.navbar import navbar
from components.gpt import chatbot_assistant, json_file_path, Chat

app = Dash(__name__, use_pages=True)

chat_client = Chat()

app.layout = html.Div([
    dcc.Store(id='chat-visible', data=True),
    # selve chat-boksen
    html.Div(
        children=[chatbot_assistant],     # hele chatbot_assistant – ikke kun .children
        id='chatbot-container',
        style={'display':'flex'}          # initialt vises den (callback kan ændre)
    ),

    # chat-bobble
    html.Div(
        "💬",
        id='chat-bubble',
        className="h-12 w-12 bg-green-500 z-50 rounded-full flex items-center justify-center text-white text-2xl cursor-pointer",
        style={'position':'fixed','bottom':'10rem','right':'10rem','display':'none'}
    ),

    dcc.Location(id="url", refresh=False),
    html.Div([navbar, dash.page_container], className="grid relative bg-gradient-to-r from-[#7bb93d] to-[#c1ed93] grid-cols-[auto_1fr]"),

    # Trigger chatDisplay-callback hvert 2 sek.
    dcc.Interval(id="live-interval", interval=2000, n_intervals=0)
])

# Live-opdatering af chatDisplay (behold som før)
@app.callback(
    Output("chatDisplay", "children"),
    Input("live-interval", "n_intervals")
)
def update_chat(n):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return [
        html.Div(
            (msg.get("question") or msg.get("answer")),
            className=(
                "chat-message text-white max-w-xs rounded-lg px-3 py-1.5 text-sm "
                + ("self-start bg-zinc-500" if "question" in msg else "self-end bg-blue-500")
            )
        )
        for msg in data["chat"]
    ]

# Her fanger vi Send-knap og input, og sender prompt til GPT
@app.callback(
    Output('chatbot-container','style'),
    Output('chat-bubble','style'),
    Output('chat-visible','data'),
    Input('close-chat','n_clicks'),
    Input('chat-bubble','n_clicks'),
    State('chat-visible','data'),
    prevent_initial_call=True
)
def toggle_chat(n_close, n_bubble, visible):
    triggered = callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered == 'close-chat':
        # skjul chat, vis bobble
        return (
            {'display':'none'},
            {'display':'flex','position':'fixed','bottom':'1rem','right':'1rem'},
            False
        )
    else:
        # vis chat, skjul bobble
        return (
            {'display':'flex'},
            {'display':'none'},
            True
        )

# Her er dit send‐callback, placeret efter de andre callbacks
@app.callback(
    Output('chatInput', 'value'),
    Input('sendButton', 'n_clicks'),
    State('chatInput', 'value'),
    prevent_initial_call=True
)

def on_send(n_clicks, prompt):
    if prompt:
        chat_client.send_prompt(prompt)    # skriver både question+answer til JSON
    return ""  # ryd input-boksen

if __name__ == "__main__":
    app.run(debug=True)