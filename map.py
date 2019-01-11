import folium
import pandas as pd

df = pd.read_csv("volcanoes.txt")
lat = list(df["LAT"])
long = list(df["LON"])
elevation = list(df["ELEV"])


def color_producer(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"


map = folium.Map(location=[38.58,-99.007], zoom_start=6, tiles= "Mapbox Bright")
fg_volcanoes = folium.FeatureGroup(name="Volcanoes")
for lat, long, elevation in zip(lat, long, elevation):
    fg_volcanoes.add_child(folium.CircleMarker(location=[lat, long], radius=8, popup=str(elevation) + " m",
                                     fill_color=color_producer(elevation), color='grey', fill_opacity= 0.7))

fg_population = folium.FeatureGroup(name="Population")

fg_population.add_child(folium.GeoJson(data=open("world.json", 'r', encoding='utf-8-sig').read(),
                            style_function=lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                            else 'orange' if 10000000< x['properties']['POP2005'] < 20000000 else 'yellow'}))

map.add_child(fg_volcanoes)
map.add_child(fg_population)
map.add_child(folium.LayerControl())

map.save("map.html")
