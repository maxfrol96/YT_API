from main import Video, PLVideo, Playlist

def test_Video():
    video = Video('BBotskuyw_M')
    assert video.title == 'Пушкин: наше все?'
    broken_video = Video('D5SKbtnK54')
    assert broken_video.title == None
    assert broken_video.id == 'D5SKbtnK54'

def test_PLvideo():
    pl_video = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
    assert pl_video.title == 'Пушкин: наше все?'
    assert  pl_video.pl_title == 'Литература'

def test_Playlist():
    pl = Playlist('PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
    assert pl.url == 'https://www.youtube.com/playlist?list=PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD'
    assert pl.show_best_video() == 'https://youtu.be/1ot9xIG9lKc'
