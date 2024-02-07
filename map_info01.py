# 지리정보 01
import folium
import pandas as pd



map_osm = folium.Map(location=[37.559978, 127.975291], zoom_start=16)  #on street map  오픈소스에서 제공하는 지도
map_osm.save("map.html")

gd = pd.read_csv("geo_data.csv", encoding="CP949", index_col=0, header=0, engine="python")
gd.head()

for i, store in gd.iterrows():
    folium.Marker(location=[store["위도"], store["경도"]], popup=store["store"], icon=folium.Icon(color="red", icon="star")).add_to(map_osm)

map_osm.save("map_market.html")
map_osm.show_in_browser()
