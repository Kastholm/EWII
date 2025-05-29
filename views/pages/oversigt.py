import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import calendar
import locale

# Set locale to Danish for proper date formatting
try:
    locale.setlocale(locale.LC_TIME, 'da_DK.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'da_DK')
    except:
        print("Danish locale not available, using default")

# Register the page
dash.register_page(__name__, path="/oversigt", name="Oversigt")


def get_sample_data():

    meetings_data = [
        {"time": "09:00", "title": "Team Standup", "duration": "30 min", "type": "møde"},
        {"time": "10:30", "title": "Kundepræsentation", "duration": "1 time", "type": "præsentation"},
        {"time": "14:00", "title": "Projektgennemgang", "duration": "45 min", "type": "gennemgang"},
        {"time": "15:30", "title": "1:1 med leder", "duration": "30 min", "type": "en-til-en"},
        {"time": "16:30", "title": "Design Workshop", "duration": "1,5 timer", "type": "workshop"},
    ]
    
    # Sample metrics data
    metrics_data = {
        "total_projects": 12,
        "completed_tasks": 87,
        "pending_reviews": 5,
        "team_members": 8
    }
    
    # Sample chart data
    performance_data = pd.DataFrame({
        'Måned': ['Jan', 'Feb', 'Mar', 'Apr', 'Maj', 'Jun'],
        'Afsluttet': [23, 45, 56, 78, 32, 67],
        'I gang': [12, 19, 23, 15, 28, 21],
        'Planlagt': [8, 12, 15, 18, 22, 25]
    })
    
    return meetings_data, metrics_data, performance_data

def get_greeting():
    current_hour = datetime.now().hour
    if current_hour < 12:
        return "God morgen"
    elif current_hour < 17:
        return "God eftermiddag"
    else:
        return "God aften"

def create_metric_card(title, value, icon, color):
    return html.Div([
        html.Div([
            html.I(className=f"fas fa-{icon} text-lg text-{color}-500"),
        ], className="flex items-center justify-center w-8 bg-gray-100 rounded-md mb-4"),
        html.Div([
            html.H3(str(value), className="text-lg font-bold text-gray-900 text-center"),
            html.P(title, className="text-xs text-gray-600 text-center leading-tight"),
        ])
    ], className="bg-white p-3 rounded-lg shadow-sm border border-gray-200 flex-1 min-w-0")

def create_meeting_card(meeting):
    type_colors = {
        "møde": "blue",
        "præsentation": "green",
        "gennemgang": "yellow",
        "en-til-en": "purple",
        "workshop": "red"
    }
    color = type_colors.get(meeting["type"], "gray")
    
    return html.Div([
        html.Div([
            html.Div([
                html.Span(meeting["time"], className="text-xs font-bold text-gray-900"),
                html.Span(meeting["duration"], className="text-xs text-gray-500"),
            ], className="flex justify-between items-center mb-1"),
            html.H4(meeting["title"], className="text-xs font-medium text-gray-800 mb-1 truncate"),
            html.Span(meeting["type"].title(), 
                     className=f"inline-block px-1.5 py-0.5 text-xs rounded bg-{color}-100 text-{color}-800")
        ], className="p-2")
    ], className="bg-white rounded-md border border-gray-200 mb-1.5")

def create_quick_stat(value, label, color):
    return html.Div([
        html.Span(value, className=f"text-lg font-bold text-{color}-600"),
        html.Span(label, className="text-xs text-gray-600 ml-1")
    ], className=f"flex items-center justify-center p-2 bg-{color}-50 rounded-md")


meetings_data, metrics_data, performance_data = get_sample_data()


performance_fig = go.Figure()
performance_fig.add_trace(go.Bar(
    name='Afsluttet',
    x=performance_data['Måned'],
    y=performance_data['Afsluttet'],
    marker_color='#10B981'
))
performance_fig.add_trace(go.Bar(
    name='I gang',
    x=performance_data['Måned'],
    y=performance_data['I gang'],
    marker_color='#F59E0B'
))
performance_fig.add_trace(go.Bar(
    name='Planlagt',
    x=performance_data['Måned'],
    y=performance_data['Planlagt'],
    marker_color='#6B7280'
))

performance_fig.update_layout(
    title="Projektoversigt",
    xaxis_title="",
    yaxis_title="",
    barmode='group',
    height=180,
    margin=dict(l=10, r=10, t=30, b=10),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(size=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    showlegend=True
)


productivity_fig = go.Figure()
productivity_fig.add_trace(go.Scatter(
    x=performance_data['Måned'],
    y=performance_data['Afsluttet'],
    mode='lines+markers',
    name='Trend',
    line=dict(color='#3B82F6', width=2),
    marker=dict(size=4)
))

productivity_fig.update_layout(
    title="Produktivitetstrend",
    xaxis_title="",
    yaxis_title="",
    height=180,
    margin=dict(l=10, r=10, t=30, b=10),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(size=10),
    showlegend=False
)

layout = html.Div([

    html.Div([
        html.Div([
            html.H1([
                html.Span(f"{get_greeting()}, ", className="text-gray-600"),
                html.Span("Ewii Medarbejder", className="text-gray-900 font-bold")
            ], className="text-xl leading-tight"),
            html.P(datetime.now().strftime("%A, %d. %B %Y"), 
                  className="text-sm text-gray-600 text-right"),
        ], className="flex-1 text-right"),
        
        html.Div([
            html.Div(id="live-time", className="text-lg text-right font-mono text-gray-700 font-bold"),
            dcc.Interval(id="time-interval", interval=1000, n_intervals=0)
        ], className="flex-1 text-right")
    ], className="flex items-center justify-between mb-3"),
    

    html.Div([
        create_metric_card("Projekter", metrics_data["total_projects"], "folder", "blue"),
        create_metric_card("Afsluttede", metrics_data["completed_tasks"], "check-circle", "green"),
        create_metric_card("Afventer", metrics_data["pending_reviews"], "clock", "yellow"),
        create_metric_card("Team", metrics_data["team_members"], "users", "purple"),
    ], className="flex gap-2 mb-3"),
    

    html.Div([
   
        html.Div([
            html.Div([
                dcc.Graph(figure=performance_fig, config={'displayModeBar': False})
            ], className="bg-white p-2 rounded-lg shadow-sm border border-gray-200 mb-2"),
            
            html.Div([
                dcc.Graph(figure=productivity_fig, config={'displayModeBar': False})
            ], className="bg-white p-2 rounded-lg shadow-sm border border-gray-200")
        ], className="flex-1 mr-2 gap-4"),
        
     
        html.Div([
            html.H3("Dagens program", className="text-sm font-semibold text-gray-900 mb-2"),
            html.Div([
                create_meeting_card(meeting) for meeting in meetings_data
            ], className="overflow-y-auto max-h-80"),
        ], className="bg-white p-3 rounded-lg shadow-sm border border-gray-200 flex-1")
    ], className="flex flex-1 gap-4 min-h-0")
    
], 
style={"width": "80vw", "margin-top": "16px"},
className="h-[95vh] max-w-[80vw] bg-white bg-opacity-70 rounded-md p-6 gap-4 flex flex-col justify-center place-content-center")


@callback(
    Output('live-time', 'children'),
    Input('time-interval', 'n_intervals')
)
def update_time(n):
    return datetime.now().strftime("%H:%M:%S")

print("Super kompakt dansk dashboard oprettet!")
print("Layout forbedringer:")
print("- Flexbox layout for optimal pladsudnyttelse")
print("- Minimum 2 elementer per vandret række")
print("- Alle elementer synlige uden scrolling")
print("- Optimeret til maksimal informationstæthed")
print("- Responsivt design med flex-egenskaber")