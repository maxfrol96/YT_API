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
        channel = Channel.get_service().channels().list(id=self.__id, part='snippet').execute()
        return channel

    def to_json(self, file_name):
        channel_dict = self.__dict__
        print(type(channel_dict))
        with open(f'{file_name}', 'w', encoding='windows-1251') as file:
            channel = json.dumps(channel_dict, indent=2, ensure_ascii=False)
            file.write(channel)

    def __str__(self):
        return f'Youtube-канал: {self.name}'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __lt__(self, other):
        return self.subscriber_count > other.subscriber_count


class Video():

    def __init__(self, id):
        self.id = id

    @property
    def title(self):
        video_info = Video.get_service().videos().list(id=self.id, part="snippet").execute()
        return video_info['items'][0]['snippet']['title']

    @property
    def likes(self):
        video_info = Video.get_service().videos().list(id=self.id, part="statistics").execute()
        return video_info['items'][0]['statistics']['likeCount']

    @property
    def views(self):
        video_info = Video.get_service().videos().list(id=self.id, part="statistics").execute()
        return video_info['items'][0]['statistics']['viewCount']


    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def __str__(self):
        return f'{self.title}'

class PLVideo(Video):
    def __init__(self, id, pl_id):
        super().__init__(id)
        self.pl_id = pl_id

    @property
    def pl_title(self):
        playlist = PLVideo.get_service().playlists().list(id=self.pl_id, part='snippet').execute()
        return playlist['items'][0]['snippet']['title']

    def __str__(self):
        return f'{self.title} ({self.pl_title})'






# video = Video('BBotskuyw_M')
# print(video)
# print(video.likes)
# print(video.views)

# id = 'PLPLtdcj9QWBvFSWQmCLwrjA3uL39zmiE6'
# api_key: str = os.getenv('YT_KEY')
# youtube = build('youtube', 'v3', developerKey=api_key)
# video_info = youtube.playlistItems().list(playlistId=id, part="contentDetails", maxResults = 50).execute()
# print(video_info)
# playlist_id = 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD'
# playlist = youtube.playlists().list(id=playlist_id, part='snippet').execute()
# playlist_name = playlist['items'][0]['snippet']['title']
# print(playlist)

print(PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD'))