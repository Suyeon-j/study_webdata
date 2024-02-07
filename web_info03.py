# 지리정보 03_카카오api
import requests
import folium
from flask import Flask, request, render_template

app = Flask(__name__)


def search_places(keyword):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    params = {'query': keyword}
    headers = {'Authorization': 'KakaoAK (ID)'} # 카카오 api키
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    places = data['documents']
    return places


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        if keyword:
            places = search_places(keyword)
            if places:
                # 중심 위치 설정
                map_center = [float(places[0]['y']), float(places[0]['x'])]
                # 지도 생성
                m = folium.Map(location=map_center, zoom_start=13)

                # 결과 마커 표시
                for place in places:
                    name = place['place_name']
                    ID = place['id']
                    lat = float(place['y'])
                    lng = float(place['x'])

                    # 카카오 지도 검색 링크 생성
                    url = 'https://map.kakao.com/link/map/{}'.format(ID)
                    # 마커에 하이퍼링크 추가
                    popup_content = '<div style="text-align: center;"><a href="{}">{}</a></div>'.format(url, name)
                    marker = folium.Marker([lat, lng], popup=folium.Popup(popup_content, max_width=300))
                    marker.add_to(m)
                return m.get_root().render()
            else:
                return '검색 결과가 없습니다.'
        else:
            return '검색어를 입력하세요.'
    else:
        return render_template('index.html')


if __name__ == '__main__':
    # http://localhost:5000
    app.run(port=5000)
