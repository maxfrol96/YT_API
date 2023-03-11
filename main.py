import os
import json
from datetime import datetime, timedelta
from googleapiclient.discovery import build


class MixinYT():

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


class Channel(MixinYT):

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


class Video(MixinYT):

    def __init__(self, id):
        self.id = id

    @property
    def title(self):
        try:
            video_info = Video.get_service().videos().list(id=self.id, part="snippet").execute()
            return video_info['items'][0]['snippet']['title']
        except:
            return None

    @property
    def likes(self):
        try:
            video_info = Video.get_service().videos().list(id=self.id, part="statistics").execute()
            return video_info['items'][0]['statistics']['likeCount']
        except:
            return None

    @property
    def views(self):
        try:
            video_info = Video.get_service().videos().list(id=self.id, part="statistics").execute()
            return video_info['items'][0]['statistics']['viewCount']
        except:
            return None



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


class Playlist(MixinYT):
    def __init__(self, id):
        self.id = id

    @property
    def title(self):
        playlist = Playlist.get_service().playlists().list(id=self.id, part='snippet').execute()
        return playlist['items'][0]['snippet']['title']

    @property
    def url(self):
        return f'https://www.youtube.com/playlist?list={self.id}'

    def video_list(self):
        playlist = Playlist.get_service().playlistItems().list(playlistId=self.id, part="contentDetails", maxResults=50).execute()
        video_list = []
        for item in playlist['items']:
            video_list.append(item['contentDetails']['videoId'])
        return video_list

    def total_duration(self):
        video_list = self.video_list()
        total_duration = timedelta(seconds=0)
        for item in video_list:
            video = Playlist.get_service().videos().list(id=item, part="contentDetails").execute()
            duration = video['items'][0]['contentDetails']['duration']
            duration_time = datetime.strptime(duration, 'PT%HH%MM%SS') - datetime.strptime("00:00:00","%H:%M:%S")
            total_duration += duration_time
        return total_duration


    def show_best_video(self):
        video_list = self.video_list()
        best_video = ''
        likes = 0
        for item in video_list:
            video = Video(item)
            if int(video.likes) > likes:
                likes = int(video.likes)
                best_video = item
        return f'https://youtu.be/{best_video}'





# pl=Playlist('PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
# print(pl.url)
# print(pl.video_list())
# print(pl.show_best_video())
# print(pl.total_duration())

video = Video('D5SKbtnK5f4')
print(video.likes)
print(video.title)
print(video.id)
# id = '1ot9xIG9lKc'
# api_key: str = os.getenv('YT_KEY')
# youtube = build('youtube', 'v3', developerKey=api_key)
# video_info = youtube.videos().list(id=id, part="contentDetails").execute()
# print(video_info)
# #
# pl_info = youtube.playlistItems().list(playlistId=id, part="contentDetails", maxResults = 50).execute()
# print(pl_info)


# video_info = youtube.playlistItems().list(playlistId=id, part="contentDetails", maxResults = 50).execute()
# print(video_info)
# d = 'PT1H48M25S'
# d = datetime.strptime(d, 'PT%HH%MM%SS').time()
# print(d)

# time_string = "1530:46"
# time_object = datetime.strptime(time_string, "%H:%M:%S").time()
# print(time_object)
# timeobj = time(8,48,45)
# print(timeobj)