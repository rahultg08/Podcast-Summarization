import requests                                             # making use of API
from api_key import API_KEY, API_KEY_LISTENNOTES
import json
import time
import pprint                                               # pretty print to make more lookable                                  

transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
listennotes_episode_endpoint = "https://listen-api.listennotes.com/api/v2/episodes"

headers = {'authorization': API_KEY}
headers_listennotes = {'X-listenAPI-Key': API_KEY_LISTENNOTES}


def get_episode_url(episode_id):
    url = listennotes_episode_endpoint + '/' + episode_id
    response = requests.request('GET', url, headers=headers_listennotes)
    data = response.json()
    # pprint.pprint(data)
    audio_url = data['audio']
    episode_thumbnail = data['thumbnail']
    podcast_title = data['podcast']['title']
    episode_title = data['title']
    return audio_url, episode_thumbnail, podcast_title, episode_title


def transcribe(audio_url, auto_chapters):
    transcript_request = {
        'audio_url': audio_url, 'auto_chapters': auto_chapters
    }
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    return transcript_response.json()['id']


def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()


def get_transcription_result_url(url, auto_chapters):
    transcribe_id = transcribe(url, auto_chapters)
    while True:
        data = poll(transcribe_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
        print("Waiting for 60 seconds")
        time.sleep(60)


def save_transcript(episode_id):
    audio_url, episode_thumbnail, episode_title, podcast_title = get_episode_url(episode_id)
    data, error = get_transcription_result_url(audio_url, auto_chapters=True)
    if data:
        filename = 'data/' + episode_id + '.txt'
        with open(filename, 'w') as f:
            f.write(data['text'])
        chapters_file = 'data/' + episode_id + '_chapters.json'
        with open(chapters_file, 'w') as f:
            chapters = data['chapters'] 
            episode_data = {'chapters': chapters, 'episode_thumbnail': episode_thumbnail,
                            'podcast_title': podcast_title, 'episode_title': episode_title}

            json.dump(episode_data, f)
            print("Transcript saved! Success")
            return True
    elif error:
        print("Error!", error)
        return False
    
    # pprint.pprint(data)
