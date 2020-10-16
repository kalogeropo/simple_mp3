from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pygame as pg
from mutagen.mp3 import MP3


playlist=[]
pg.mixer.init()

global isStopped
isStopped=False

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
    global isStopped

    if len(playlist)>0:
        isStopped=False
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
    #update status bar slider
    slider.config(value=0)
    status_bar.config(text="")
    global  isStopped
    isStopped =True
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
    # update status bar slider

    if len(playlist)!=0:#check empty playlist
    #current song as a tuple
        # update status bar slider
        slider.config(value=0)
        status_bar.config(text="")
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
            #slider.config(to=song_duration)

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
            #slider.config(to=song_duration)


def previous_song():

    if len(playlist)!=0:#check empty playlist
        # current song as a tuple
        # update status bar slider
        slider.config(value=0)
        status_bar.config(text="")
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
            #slider.config(to=song_duration)


def delete_song():
    short_song_name = song_box.get(ACTIVE)
    for index, sng in enumerate(playlist):
        if short_song_name in sng:
            song_box.delete(ANCHOR)
            playlist.pop(index)
            stop()

def clear_all():
    for item in playlist:
        playlist.remove(item)
    song_box.selection_clear(0, END)
    song_box.delete(0,END)
    stop()

def convertMillis(millisec):
    seconds = (millisec / 1000) % 60
    seconds = int(seconds)
    minutes = (millisec / (1000 * 60)) % 60
    minutes = int(minutes)
    time = str(minutes) + ":" + str(seconds)
    return seconds,minutes,time


def song_dur():
    global isStopped
    #when stopped and played again 2 song_dur running and creates double timing
    if isStopped:
        return 0
    current_time= pg.mixer.music.get_pos()
    temp=current_time/1000 # store the current time in msec to update slider position

    # convert time in min and sec using convertmilis function not time (reasons ;) )
    # at first the result is on msecs
    curr_sec , curr_mins,current_time=convertMillis(current_time)



#determine song duration: easiest way using mutagen module !! possible issue file types.
    song = song_box.get(ACTIVE)
    for index, sng in enumerate(playlist):
        if song in sng:
            song = playlist[index]
    song_d = MP3(song)
    global song_duration
    song_duration =song_d.info.length
    #print(song_duration)
    song_duration_sec ,song_duration_mins,total_duration = convertMillis(song_duration*1000)

    #update time at status_bar, slider position
    # slider.config(to=song_duration)
    print(int(slider.get()),int(temp),total_duration)
    if int(slider.get())==int(song_duration):#check if song ended
        status_bar.config(text="Time elapsed: " + total_duration + " of " + total_duration)
        next_song() #when song ends moves to next one
    elif paused==True:
        pass
    elif int(slider.get())==int(temp):
        slider.config(to=int(song_duration),value=int(temp))
        timeprint = convertMillis(song_duration * 1000)
        status_bar.config(text="Time elapsed: " + timeprint[2] + " of " + total_duration)
    else:
        slider.config(to=int(song_duration),value=int(slider.get()+1))
        cu_time= slider.get()+1
        timeprint = convertMillis(cu_time * 1000)
        status_bar.config(text="Time elapsed: " + timeprint[2] + " of " + total_duration)

    # update song duration after 10000msecs it will rerun the song_dur function
    isStopped = False
    status_bar.after(1000,song_dur)


def slide(coord):
    song = song_box.get(ACTIVE)
    for index, sng in enumerate(playlist):
        if song in sng:
            song = playlist[index]
            pg.mixer.music.load(song)
            pg.mixer.music.play(loops=0, start=int(slider.get()))

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