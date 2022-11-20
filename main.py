import json
import pprint
from api_comm import *
import streamlit as st

st.title("Podcast Summarization")
episode_id = st.sidebar.text_input("Input an episode id:")
button = st.sidebar.button('Download Podcast Summary', on_click=save_transcript, args=(episode_id,))


def get_clean_time(start_ms):
    secs = int((start_ms/1000) % 60)
    mins = int((start_ms/(1000*60)) % 60)
    hrs = int((start_ms/(1000*60*60)) % 24)
    if hrs > 0:
        start_t = f'{hrs:02d}:{mins:02d}:{secs:02d}'
    else:
        start_t = f'{mins:02d}:{secs:02d}'
    return start_t


if button:
    filename = 'data/' + episode_id + '_chapters.json'
    with open(filename, 'r') as f:
        data = json.load(f)

        chapters = data['chapters']
        thumbnail = data['episode_thumbnail']
        podcast_title = data['podcast_title']
        episode_title = data['episode_title']

        st.header(f"{podcast_title} - {episode_title}")
        st.image(thumbnail)

    for cp in chapters:
        with st.expander(cp['gist'] + '-' + get_clean_time(cp['start'])):                                       # on clicking the gist, summary of the particular chapters would be dropped down
            cp['summary']

# with open("data/b801da722fb14e24869191887d0352a2_chapters.json", "r") as f:
#     data = json.load(f)
# chapters = data['chapters']
# pprint.pprint(chapters)

# 1d5c236b44ad417cacb3f78ec71c298b

