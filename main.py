import os
import json
from googleapiclient.discovery import build

class Channel():

    def __init__(self, id):
        self.__id = id
        self.name = Channel.print_info(self)['items'][0]['snippet']['title']
        self.description = Channel.print_info(self)['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + self.__id
        self.subscriber_count = Channel.print_info(self)['items'][0]['statistics']['subscriberCount']
        self.video_count = Channel.print_info(self)['items'][0]['statistics']['videoCount']
        self.view_count = Channel.print_info(self)['items'][0]['statistics']['viewCount']

    @property
    def id(self):
        return self.__id

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


    def print_info(self):
        channel = Channel.get_service().channels().list(id=self.__id, part='snippet,statistics').execute()
        return channel

    def to_json(self, file_name):
        channel_dict = self.__dict__
        print(type(channel_dict))
        with open(f'{file_name}', 'w', encoding='windows-1251') as file:
            for key in channel_dict:
                file.write(f'{key}: ')
                file.write(f'{channel_dict[key]}\n')



