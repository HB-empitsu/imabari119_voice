import pandas as pd
import requests

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

option = list(data.keys())

# ストリームリットセレクトボックスの作成
chois = st.selectbox("日付を選択", option)

if chois:
    st.subheader(data[chois]["date_week"])
    audio_url = f"{base_url}/mp3/{chois}.mp3"
    st.audio(audio_url, format="audio/mpeg")

    df = pd.DataFrame(data[chois]["hospitals"]).reindex(columns=["name", "medical", "time", "daytime", "address"])

    st.dataframe(df, use_container_width=True, hide_index=True)
