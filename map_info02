# 지리정보 02
from flask import Flask
import folium
import pandas as pd



app = Flask(__name__)


@app.route("/") # 웹서버 루트, 사용시 컴퓨터가 웹서버가 됨
def my_root():
    return "Hi, Python Flask!"


@app.route("/map")
def show_map(): # 위 주소와 함수가 연동됨
    map_osm = folium.Map(location=[37.559978, 127.975291], zoom_start=16)  # on street map  오픈소스에서 제공하는 지도
    gd = pd.read_csv("(파일 이름).csv", encoding="CP949", index_col=0, header=0, engine="python")
    for i, store in gd.iterrows():
        folium.Marker(location=[store["위도"], store["경도"]], popup=store["store"],
                      icon=folium.Icon(color="red", icon="star")).add_to(map_osm)
    return map_osm.get_root().render() # 주소를 렌더링해주는 효과


if __name__ == '__main__':
    app.run(port=5000)
