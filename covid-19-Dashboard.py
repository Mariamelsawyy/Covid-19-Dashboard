import dash
import dash_bootstrap_components as dbc
from dash import dcc,html, Input, Output #input , output for the callbacks
import plotly.express as px # for charts and graphs
import pandas as pd

# Loading data
def load_data():
    data= pd.read_csv(r"ur_file_path.csv")

    data['Date'] = pd.to_datetime(data['Date'])
    data = data.dropna()
    return data
data = load_data()

countries = sorted(data['Country/Region'].unique())


# Creating a web APP
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# APP layput & Design

app.layout = dbc.Container([
    
    # Title
    dbc.Row([
        dbc.Col(
            html.H1("Global COVID-19 Dashboard", className="text-center my-4"),
            width=12
        )
    ]),

    # Subtitle
    dbc.Row([
        dbc.Col(
            html.P(
                "Visualizing global COVID-19 trends over time by country and case type.",
                className="text-center mb-4"
            ),
            width=12
        )
    ]),

    # Controls Row
    dbc.Row([

        # Country dropdown
        dbc.Col([
            html.Label("Select Country"),
            dcc.Dropdown(
                id="country-dropdown",
                options=[{"label": c, "value": c} for c in countries],
                value="Egypt",
                clearable=False
            )
        ], width=4),

        # Metric selection
        dbc.Col([
            html.Label("Select Metric"),
            dcc.RadioItems(
                id="metric-radio",
                options=[
                    {"label": "Confirmed", "value": "Confirmed"},
                    {"label": "Deaths", "value": "Deaths"},
                    {"label": "Recovered", "value": "Recovered"}
                ],
                value="Confirmed",
                inline=True
            )
        ], width=4),

        # Date range slider
        dbc.Col([
            html.Label("Select Date Range"),
            dcc.DatePickerRange(
                id="date-picker",
                start_date=data['Date'].min(),
                end_date=data['Date'].max()
            )
        ], width=4),
    ], className="mb-4"),

    # Main graph
    dbc.Row([
        dbc.Col(
            dcc.Graph(id="covid-trend-graph"),
            width=12
        )
    ])

], fluid=True)


# Callback to update graph
@app.callback(
    Output("covid-trend-graph", "figure"),
    Input("country-dropdown", "value"),
    Input("metric-radio", "value"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
)
def update_graph(country, metric, start_date, end_date):

    filtered = data[
        (data["Country/Region"] == country) &
        (data["Date"] >= start_date) &
        (data["Date"] <= end_date)
    ]

    fig = px.line(
        filtered,
        x="Date",
        y=metric,
        title=f"{metric} Cases Over Time in {country}",
        labels={"Date": "Date", metric: f"Number of {metric} Cases"}
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111111",
        plot_bgcolor="#111111"
    )

    return fig


if __name__ =="__main__":
    app.run(debug=True)
