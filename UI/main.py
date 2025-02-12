import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import json

# Загружаем данные из JSON
with open("dice_data.json", "r") as f:
    dice_data = json.load(f)

# Получаем список доступных переменных и сценариев
available_variables = list(dice_data.keys())
default_variable = available_variables[0]

# Берем сценарии из первой попавшейся переменной (они одинаковые для всех)
available_scenarios = list(dice_data[default_variable].keys())

# Создаём приложение Dash
app = dash.Dash(__name__)

# Макет приложения
app.layout = html.Div(
    style={'textAlign': 'center'},
    children=[
        html.H1("RICE MAP [proto]"),
        
        # Выпадающий список для выбора переменной
        dcc.Dropdown(
            id="variable-selector",
            options=[{"label": var.replace("_", " ").capitalize(), "value": var} for var in available_variables],
            value=default_variable,  # Значение по умолчанию
            clearable=False,
            style={"width": "50%", "margin": "10px auto"},
        ),

        # Выпадающий список для выбора сценария
        dcc.Dropdown(
            id="scenario-selector",
            options=[{"label": scenario.upper(), "value": scenario} for scenario in available_scenarios],
            value=available_scenarios[0],  # Значение по умолчанию
            clearable=False,
            style={"width": "50%", "margin": "10px auto"},
        ),

        html.Div(
            style={"position": "relative", "width": "800px", "margin": "20px auto"},
            children=[
                # Карта
                html.Img(
                    src="/assets/world_map.jpg",  # Файл карты должен быть в папке assets/
                    style={"width": "100%", "height": "auto"},
                ),
                # Красные точки (регионы)
                html.Div(id="russia", className="region-point", style={"top": "15%", "left": "50%"}),
                html.Div(id="usa", className="region-point", style={"top": "30%", "left": "15%"}),
                html.Div(id="china", className="region-point", style={"top": "33%", "left": "70%"}),
                html.Div(id="india", className="region-point", style={"top": "40%", "left": "63%"}),
            ],
        ),

        # График
        dcc.Graph(id="country-graph"),
    ],
)

# Обработчик клика на точку
@app.callback(
    Output("country-graph", "figure"),
    [
        Input("russia", "n_clicks"),
        Input("usa", "n_clicks"),
        Input("china", "n_clicks"),
        Input("india", "n_clicks"),
        Input("variable-selector", "value"),
        Input("scenario-selector", "value"),
    ],
)
def update_graph(russia_clicks, usa_clicks, china_clicks, india_clicks, selected_variable, selected_scenario):
    ctx = dash.callback_context
    if not ctx.triggered:
        return go.Figure()

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # Инициализируем регион по умолчанию
    region = "Global"

    # Определяем, какой регион был кликнут
    if button_id == "russia":
        region = "Russia"
    elif button_id == "usa":
        region = "USA"
    elif button_id == "china":
        region = "China"
    elif button_id == "india":
        region = "India"

    # Проверяем, есть ли выбранная переменная и сценарий в данных
    if selected_variable not in dice_data or selected_scenario not in dice_data[selected_variable]:
        return go.Figure()

    # Берём данные по выбранной переменной и сценарию
    values = dice_data[selected_variable][selected_scenario]
    years = list(range(2020, 2020 + len(values) * 5, 5))

    # Строим график
    fig = go.Figure(
        data=go.Scatter(x=years, y=values, mode="lines+markers", name=selected_variable)
    )
    fig.update_layout(title=f"{selected_variable.replace('_', ' ').capitalize()} ({region}, {selected_scenario.upper()})", 
                      xaxis_title="Годы", yaxis_title="Значение")
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)