import PySimpleGUI as sg
import pygame
import random
import os
import ctypes

myappid = 'Bean.YTDownloader.Downloader.1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

bmc_logo = os.path.realpath(__file__).replace("beansound.py","bmc-button.png")
icon_logo = os.path.realpath(__file__).replace("beansound.py","ciconmusic.ico")

pygame.init()
pygame.mixer.init()

sg.theme("LightBrown4")

song_list = []

layout = [
    [sg.Text("Bean Sound", font="bold, 14")],
    [sg.FolderBrowse("Select Folder", target=(1,1), key="dirselect"), sg.InputText("Select A Folder and Click 'Load Songs'",key="songdirect")],
    [sg.Button("Load Songs", key="dirload")],
    [sg.Listbox(values=song_list, size=(60,10), key="songs")],
    [sg.Text("                                                                             ", key="stitle")],
    [sg.Text("00:00", key='current'), sg.ProgressBar(max_value=100, orientation="h", size=(25,10), key="pbar"), sg.Text("00:00", key="total")],
    [sg.Slider(range=(0,20), default_value=10, orientation="h", key="volume", enable_events=True)],
    [sg.Button("Play", key="play"), sg.Button("Pause", key="pause"), sg.Button("HELP!", key="help")],
]

window = sg.Window(title="Bean Sound Player", layout=layout, element_justification="c", icon=icon_logo)

ctime = window["current"]
cstime = window["total"]
pbutton = window["pause"]
wsongs = window["songs"]
ctitle = window["stitle"]

ttime = 1
volume = 10
num_pause = 0
minutes = 0.0
seconds = 0.0
pause_pos = 0

def set_volume(pos):
    global volume
    volume = float(pos)/20
    pygame.mixer.music.set_volume(volume)

def random_song():
    global ttime, minutes, seconds
    random_song = random.choice(song_list)
    song_path = str(values["songdirect"])+"/"+str(random_song)
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    csong = pygame.mixer.Sound(song_path)
    ttime = int(csong.get_length())
    og = str(float(ttime/60))
    splits = og.split(".")
    minutes = splits[0]
    temp_seconds = float("."+splits[-1][:2])
    seconds = int(str((60*temp_seconds).__round__(0)).replace(".0",""))
    if seconds < 10:
        seconds = str(0)+str(seconds)
    cstime.update(" {}:{} ".format(minutes, seconds))
    ctitle.update(str(random_song))
    current_time = (float(pygame.mixer.music.get_pos())/float(1000)).__round__(0)
    og = str(float(current_time/60))
    splits = og.split(".")
    minutes = splits[0]
    temp_seconds = float("."+splits[-1][:2])
    seconds = int(str((60*temp_seconds).__round__(0)).replace(".0",""))
    if seconds < 10:
        seconds = str(0)+str(seconds)
    pbar_time = 100*(current_time/float(ttime))
    ctime.update(" {}:{} ".format(minutes, seconds))
    window["pbar"].update(pbar_time)

def play_song():
    global ttime, minutes, seconds
    song_file = str(values["songdirect"])+"/"+str(values["songs"][0])
    pygame.mixer.music.load(song_file)
    pygame.mixer.music.play()
    csong = pygame.mixer.Sound(song_file)
    ttime = int(csong.get_length())
    og = str(float(ttime/60))
    splits = og.split(".")
    minutes = splits[0]
    temp_seconds = float("."+splits[-1][:2])
    seconds = int(str((60*temp_seconds).__round__(0)).replace(".0",""))
    if seconds < 10:
        seconds = str(0)+str(seconds)
    cstime.update(" {}:{} ".format(minutes, seconds))
    ctitle.update(str(values["songs"][0]))
    current_time = (float(pygame.mixer.music.get_pos())/float(1000)).__round__(0)
    og = str(float(current_time/60))
    splits = og.split(".")
    minutes = splits[0]
    temp_seconds = float("."+splits[-1][:2])
    seconds = int(str((60*temp_seconds).__round__(0)).replace(".0",""))
    if seconds < 10:
        seconds = str(0)+str(seconds)
    pbar_time = 100*(current_time/float(ttime))
    ctime.update(" {}:{} ".format(minutes, seconds))
    window["pbar"].update(pbar_time)
    return minutes, seconds

def pause_unpause():
    global num_pause, pause_pos
    if num_pause == 0:
        pygame.mixer.music.pause()
        pause_pos = int(pygame.mixer.music.get_pos())
        print(pause_pos)
        pbutton.update("Resume")
        num_pause = 1
    else:
        pygame.mixer.music.unpause()
        pause_pos = int(pygame.mixer.music.get_pos())
        print(pause_pos)
        pbutton.update("Pause")
        num_pause = 0

def help_window():
    help_layout = [
        [sg.Text("How to Use Bean Sound", font="bold, 14")],
        [sg.Text("Version 1.00")],
        [sg.Text("Bean Sound is a lightweight MP3 and audio-player that well... plays audio!")],
        [sg.Text("Simply select a folder and click 'Load Songs'")],
        [sg.Text("Bean Sound will auto detect all audio files in that folder.")],
        [sg.Text("After that, click on a song then play!")],
        [sg.Text("Bean Sound currently has a few features such as pause/unpause, autoplay, and volume control.")],
        [sg.Text("See the GitHub page for future features and more info.")],
        [sg.Text("")],
        [sg.Text("Love Bean Sound?")],
        [sg.Text("Click this bright yellow button to support my work! :)")],
        [sg.Image(filename=bmc_logo, background_color=None, enable_events=True, key="bmc")],
        [sg.Button("Close", key="close")]
    ]

    def buymecoffee():
        os.system("start https://www.buymeacoffee.com/ztechdata")

    help_win = sg.Window(layout=help_layout, title="Help", icon=icon_logo, element_justification="c")

    while True:
        event, values = help_win.Read()
        if event == sg.WIN_CLOSED or event == "close":
            help_win.close()
            break
        if event == "bmc":
            buymecoffee()

pbar_time = 0.0
while True:
    event, values = window.Read(timeout=500)
    if event == sg.WIN_CLOSED:
        break
    if event == "play":
        try:
            play_song()
        except pygame.error:
            sg.popup("Sorry! This song cant be played!", title="Whoops!", icon=icon_logo)
    if event == "volume":
        pos = values["volume"]
        set_volume(pos)
    if event == "pause":
        pause_unpause()
    if event == "dirload":
        if values["songdirect"] == "Select A Folder and Click 'Load Songs'" or values["songdirect"] == "":
            sg.popup("Please select a valid directory.", title="Whoops!", icon=icon_logo)
            dir_list = []
        else:
            dir_list = os.listdir(values["songdirect"])
        for item in dir_list:
            music_ext = ('.mp3','.wav','m4a','.flac','.wma','.aac')
            if item.endswith(music_ext) and item not in song_list:
                song_list.append(item)
        if len(song_list) == 0:
            sg.popup("Looks like there are no supported files here!", title="Whoops!", icon=icon_logo)
        wsongs.update(song_list)
    if pbar_time > 99.9:
        random_song()
    if event == "help":
        help_window()

    current_time = (float(pygame.mixer.music.get_pos())/float(1000)).__round__(0)
    print(num_pause)
    og = str(float(current_time/60))
    splits = og.split(".")
    minutes = splits[0]
    if minutes == "-0":
        minutes = "0"
    temp_seconds = float("."+splits[-1][:2])
    seconds = int(str((60*temp_seconds).__round__(0)).replace(".0",""))
    if seconds < 10:
        seconds = str(0)+str(seconds)
    pbar_time = 100*(current_time/float(ttime))
    ctime.update(" {}:{} ".format(minutes, seconds))
    window["pbar"].update(pbar_time)
    
    if pause_pos != num_pause:
        pause_pos = num_pause
