import datetime

import pandas as pd
import requests
from streamlit_folium import st_folium

import folium
import streamlit as st

base_url = st.secrets["url"]

@st.cache_data
def load_data():
    url = f"{base_url}/data.json"

    r = requests.get(url)
    r.raise_for_status()

    data = r.json()

    return data


st.set_page_config(page_title="今治市救急当番病院案内")
st.title("今治市救急当番病院案内")


data = load_data()

today = datetime.date.today()

option = list(data.keys())

start = datetime.datetime.strptime(option[0], r"%Y-%m-%d").date()
end = datetime.datetime.strptime(option[-1], r"%Y-%m-%d").date()

# 日付入力ウィジェットを表示
selected_date = st.date_input("日付を選択してください", value=today, min_value=start, max_value=end)


if selected_date:
    chois = selected_date.strftime(r"%Y-%m-%d")

    if chois in option:
        st.subheader(data[chois]["date_week"])
        audio_url = f"{base_url}/mp3/{chois}.mp3"
        st.audio(audio_url, format="audio/mpeg")

        df = pd.DataFrame(data[chois]["hospitals"]).reindex(
            columns=["name", "medical", "time", "daytime", "address", "lat", "lon"]
        )

        st.dataframe(
            df[["name", "medical", "time", "daytime", "address"]],
            column_config={
                "name": "医療機関名",
                "medical": "診療科目",
                "time": "診療時間",
                "daytime": "電話番号",
                "address": "住所",
            },
            use_container_width=True,
            hide_index=True,
        )

        m = folium.Map(
            location=[df["lat"].mean(), df["lon"].mean()],
            tiles="https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png",
            attr='&copy; <a href="https://maps.gsi.go.jp/development/ichiran.html">国土地理院</a>',
            zoom_start=12,
        )

        for _, r in df.iterrows():
            folium.Marker(
                location=[r["lat"], r["lon"]],
                popup=folium.Popup(f'<p>{r["name"]}</p>', max_width=300),
                tooltip=r["name"],
            ).add_to(m)

        st_data = st_folium(m, width=700, height=500, returned_objects=[])
    else:
        st.write("データが見つかりません")
