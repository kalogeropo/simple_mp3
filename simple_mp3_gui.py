from tkinter import *
from tkinter import filedialog
import pygame as pg


playlist=[]
pg.mixer.init()
def add_song():
    song = filedialog.askopenfilename(initialdir = "E:/Tango Music/",title = "choose song")
    # add_full_path to playlist
    if song not in playlist:
        playlist.append(song)
    # beautify song name
        song = song.split('/')
        song = song[-1]
    # add to on screen playlist
        song_box.insert(END,song)
        print(playlist)

def add_multiple_songs():
    songs = filedialog.askopenfilenames(initialdir = "E:/Tango Music/",title = "choose songs")
    # add_full_path to playlist
    for song in songs:
        if song not in playlist:
            playlist.append(song)
    # beautify song name
            song = song.split('/')
            song = song[-1]
    # add to on screen playlist
            song_box.insert(END,song)
    print(playlist)

#play the song which is active on the listbox
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
    #current song as a tuple
    nxt=song_box.curselection()
    #indexing the next song
    nxt_index = nxt[0] + 1
    if nxt_index < len(playlist):
    #update active bar on songs_box
        song_box.selection_clear(0,END)
        song = playlist[nxt_index]
        song_box.activate(nxt_index)
        song_box.selection_set(nxt_index, last=None)
    #play
        pg.mixer.music.load(song)
        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play(loops=0)
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



def previous_song():
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
root.mainloop()