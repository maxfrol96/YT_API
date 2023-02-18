import os
import json
from googleapiclient.discovery import build

class Channel():

    def __init__(self, id):
        self.id = id

    def print_info(self):
        api_key: str = os.getenv('YT_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.id, part='snippet,statistics').execute()
        return json.dumps(channel, indent=2, ensure_ascii=False)

#
red = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
print(red)