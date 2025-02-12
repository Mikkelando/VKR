import folium
import pandas as pd
import plotly.express as px
import json

# Загружаем данные по регионам
regions_data = pd.read_csv("regions.csv")

# Загружаем GeoJSON c континентами (можно заменить на границы стран)
with open("world_regions.geojson", "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

# Создаём карту
m = folium.Map(location=[20, 0], zoom_start=2)

# Функция для генерации графиков
def generate_plot(continent):
    subset = regions_data[regions_data["region"] == continent]
    if subset.empty:
        return "Нет данных"

    fig = px.line(subset, x="year", y="value", title=f"Данные для {continent}")
    return fig.to_html(full_html=False)

# Добавляем регионы на карту
for feature in geojson_data["features"]:
    region_name = feature["properties"]["name"]
    popup_content = generate_plot(region_name)

    folium.GeoJson(
        feature,
        name=region_name,
        style_function=lambda x: {"fillColor": "blue", "color": "black", "weight": 1, "fillOpacity": 0.3},
        highlight_function=lambda x: {"fillColor": "yellow", "color": "black", "weight": 2, "fillOpacity": 0.5},
        tooltip=region_name,
        popup=folium.Popup(html=popup_content, max_width=500)
    ).add_to(m)

# Сохраняем карту
m.save("interactive_continents_map.html")

print("Карта успешно создана! Открой interactive_continents_map.html в браузере.")