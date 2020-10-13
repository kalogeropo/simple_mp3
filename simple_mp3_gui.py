from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pygame as pg
from mutagen.mp3 import MP3


playlist=[]
pg.mixer.init()
def add_song():
    song = filedialog.askopenfilename(initialdir = "C:/Users/nrkal/Music/",title = "choose song")
    # add_full_path to playlist
    if song not in playlist:
        playlist.append(song)
    # beautify song name
        song = song.split('/')
        song = song[-1]
    # add to on screen playlist
        song_box.insert(END,song)
    else:
        print("duplicate")

def add_multiple_songs():
    songs = filedialog.askopenfilenames(initialdir = "C:/Users/nrkal/Music/",title = "choose songs")
    # add_full_path to playlist
    for song in songs:
        if song not in playlist:
            playlist.append(song)
    # beautify song name
            song = song.split('/')
            song = song[-1]
    # add to on screen playlist
            song_box.insert(END,song)
        else:
            print("duplicate")
#play the song which is active on the listbox
#!!!!!!!!!!!!!!!issue if i clear the list and hit play it plays the last selectected song!!!!!
def play():

    if len(playlist)>0:
        short_song_name = song_box.get(ACTIVE)
        print(short_song_name)
        for index ,sng in enumerate(playlist):
            if short_song_name in sng:
                song = playlist[index]
        pg.mixer.music.load(song)
        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play(loops=0)
        #show song duration in status bar
        song_dur()

def stop():
    pg.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        pg.mixer.music.unpause()
        paused = False
    else:
        pg.mixer.music.pause()
        paused =True

def next_song():
    if len(playlist)!=0:#check empty playlist
    #current song as a tuple
        nxt=song_box.curselection()
        #indexing the next song
        nxt_index = nxt[0] + 1
        if nxt_index < len(playlist) :
        #update active bar on songs_box
            song_box.selection_clear(0,END)
            song = playlist[nxt_index]
            song_box.activate(nxt_index)
            song_box.selection_set(nxt_index, last=None)
        #play
            pg.mixer.music.load(song)
            pg.mixer.music.set_volume(0.3)
            pg.mixer.music.play(loops=0)
            song_dur()
        else:
            nxt_index=0
            # update active bar on songs_box
            song_box.selection_clear(0, END)
            song = playlist[nxt_index]
            song_box.activate(nxt_index)
            song_box.selection_set(nxt_index, last=None)
            # play
            pg.mixer.music.load(song)
            pg.mixer.music.set_volume(0.3)
            pg.mixer.music.play(loops=0)
            song_dur()


def previous_song():

    if len(playlist)!=0:#check empty playlist
        # current song as a tuple
        nxt = song_box.curselection()
        # indexing the next song
        nxt_index = nxt[0] - 1
        if nxt_index == 0:
            nxt_index=len(playlist)-1
        if nxt_index < len(playlist):
            # update active bar on songs_box
            song_box.selection_clear(0, END)
            song = playlist[nxt_index]
            song_box.activate(nxt_index)
            song_box.selection_set(nxt_index, last=None)
            # play
            pg.mixer.music.load(song)
            pg.mixer.music.set_volume(0.3)
            pg.mixer.music.play(loops=0)
            song_dur()



def delete_song():
    short_song_name = song_box.get(ACTIVE)
    for index, sng in enumerate(playlist):
        if short_song_name in sng:
            song_box.delete(ANCHOR)
            playlist.pop(index)
            pg.mixer.music.stop()

def clear_all():
    for item in playlist:
        playlist.remove(item)
    song_box.selection_clear(0, END)
    song_box.delete(0,END)
    pg.mixer.music.stop()

def convertMillis(millisec):
    seconds = (millisec / 1000) % 60
    seconds = int(seconds)
    minutes = (millisec / (1000 * 60)) % 60
    minutes = int(minutes)
    return seconds,minutes

def song_dur():
    current_time= pg.mixer.music.get_pos()
    #convert time in min and sec using convertmilis function not time (reasons ;) )
    #at first the result is on msecs
    curr_sec , curr_mins=convertMillis(current_time)
    current_time = str(curr_mins) + ":" + str(curr_sec)

#determine song duration: easiest way using mutagen module !! possible issue file types.
    song = song_box.get(ACTIVE)
    for index, sng in enumerate(playlist):
        if song in sng:
            song = playlist[index]
    song_d = MP3(song)
    song_duration =song_d.info.length
    #print(song_duration)
    song_duration_sec ,song_duration_mins = convertMillis(song_duration*1000)
    #print(str(song_duration_mins) + " : " + str(song_duration_sec))
    total_duration = str(song_duration_mins) + " : " + str(song_duration_sec)
    status_bar.config(text="Time elapsed: "+current_time + " of " + total_duration )
    # update song duration after 1000msecs it will rerun the song_dur function
    status_bar.after(1000,song_dur)

def slide(coord):
    pass

#init and create the player window
root = Tk()
root.title("Simple mp3 player")
root.geometry("500x300")

#playlist box
song_box = Listbox(root,bg="black", fg="white",width = 60,selectbackground = "green", selectforeground= "black")
song_box.pack(pady=20)

#buttons label
nxt_btn = "Next"
pl_btn = "Play"
st_btn = "Stop"
prv_btn = "Previous"
pau_btn = "Pause"

#Control box

ctr_frame = Frame(root)
ctr_frame.pack()

next_btn = Button(ctr_frame,text =nxt_btn,command = next_song)
play_btn = Button(ctr_frame,text =pl_btn,command=play)
stop_btn = Button(ctr_frame,text =st_btn,command=stop)
previous_btn = Button(ctr_frame,text =prv_btn,command = previous_song)
pause_btn = Button(ctr_frame,text =pau_btn,command = lambda: pause(paused))

next_btn.grid(row=0,column=0,padx=5)
play_btn.grid(row=0,column=1,padx=5)
stop_btn.grid(row=0,column=2,padx=5)
previous_btn.grid(row=0,column=3,padx=5)
pause_btn.grid(row=0,column=4,padx=5)

#define menu

menu = Menu(root)
root.config(menu=menu)

#add song

add_song_menu = Menu(menu)
menu.add_cascade(label = "Add Songs",menu=add_song_menu)
add_song_menu.add_command(label = "Add One Song To Qeue", command = add_song)

#add multiple songs
add_song_menu.add_command(label = "Add Songs To Qeue", command = add_multiple_songs)

#delete songs and clear playlist
add_song_menu.add_command(label = "Delete Song From Qeue", command = delete_song)
add_song_menu.add_command(label="Clear All", command = clear_all)

#status bar
status_bar= Label(root,text='',bd=1,relief=GROOVE,anchor= E)
status_bar.pack(fill=X,side = BOTTOM,ipady=2)

#music slider
slider = ttk.Scale(root, from_=0, to = 100, orient=HORIZONTAL, length = 300, command = slide,value=0)
slider.pack(fill=X,pady =20)

root.mainloop()