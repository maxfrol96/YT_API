from main import Video, PLVideo

def test_Video():
    video = Video('BBotskuyw_M')
    assert video.title == 'Пушкин: наше все?'

def test_PLvideo():
    pl_video = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
    assert pl_video.title == 'Пушкин: наше все?'
    assert  pl_video.pl_title == 'Литература'
