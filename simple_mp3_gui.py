from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import pygame as pg
from mutagen.mp3 import MP3
import os

playlist=[]
pg.mixer.init()
pg.mixer.music.set_volume(0.2)

global isStopped
isStopped=False
global isPlaying
isPlaying = False

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

#play the song which is active on the listbox
#!!!!!!!!!!!!!!!issue if i clear the list and hit play it plays the last selectected song!!!!!
def play():
    global isStopped
    global isPlaying
    if len(playlist)>0:
        isStopped=False
        if isPlaying:
            return
        isPlaying=True
        short_song_name = song_box.get(ACTIVE)
        #print(short_song_name)
        for index ,sng in enumerate(playlist):
            if short_song_name in sng:
                song = playlist[index]
        nxt=song_box.curselection()
        #print(nxt)
        #play stop play stop issue fixed
        if len(nxt)==0:
            nxt=[index]
        song_box.selection_clear(0, END)
        song_box.activate(nxt[0])
        song_box.selection_set(nxt[0], last=None)

        pg.mixer.music.load(song)
        pg.mixer.music.play(loops=0)
        #show song duration in status bar
        song_dur()

def stop():
    #update status bar slider
    slider.config(value=0)
    status_bar.config(text="")
    global  isStopped
    isStopped =True
    global  isPlaying
    isPlaying=False
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

def play_indx(nxt_index):
    song_box.selection_clear(0, END)
    song = playlist[nxt_index]
    song_box.activate(nxt_index)
    song_box.selection_set(nxt_index, last=None)
    # play
    pg.mixer.music.load(song)
    pg.mixer.music.play(loops=0)

def next_song():

    if len(playlist)!=0:#check empty playlist
    #current song as a tuple

    # update status bar slider
        slider.config(value=0)
        status_bar.config(text="")
        nxt=song_box.curselection()
        #indexing the next song
        nxt_index = nxt[0]
        if nxt_index < len(playlist)-1 :
            nxt_index = nxt[0] + 1
        #update active bar on songs_box
            play_indx(nxt_index)
        else:
            nxt_index=0
            play_indx(nxt_index)


def previous_song():

    if len(playlist)!=0:#check empty playlist
        # current song as a tuple
        # update status bar slider
        slider.config(value=0)
        status_bar.config(text="")
        nxt = song_box.curselection()
        # indexing the next song
        nxt_index = nxt[0] - 1
        if nxt_index < 0:
            nxt_index=len(playlist)-1
        if nxt_index < len(playlist):
            play_indx(nxt_index)


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
        #print(item)
    #print(playlist)
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
    #print(int(slider.get()),int(temp),total_duration)
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

def adj_vol():
    vol = volume_text_box.get()
    if vol == "":
        vol=0
    #print(vol)
    vol = int(vol)/100
    if vol>=0 and vol<=1:
        pg.mixer.music.set_volume(vol)
    else:
        pg.mixer.music.set_volume(1)

def save_pl():
    file= filedialog.asksaveasfile(title="save a playlist",
                                   mode='w',
                                   defaultextension='.txt',
                                   initialdir = "C:/Users/nrkal/PycharmProjects/simple_mp3/playlists/")
    if file is None:
        return
    #print(str(playlist))
    for item in playlist:
        file.write('%s \n' %item)

def load_pl():
    songs=[]
    file = filedialog.askopenfilename(initialdir = "C:/Users/nrkal/PycharmProjects/simple_mp3/playlists/",
                                      title = "Import Playlist")
    with open(file,mode='r') as fd:
        songs=fd.read()
        songs=songs.split("\n")
        fd.close()
        #clean up songs
    for song in songs:
        if song =="":
            songs.remove(song)

    #print(songs)
    if file is None:
        return
    for song in songs:
        if song not in playlist:
            playlist.append(song)
            # beautify song name
            song = song.split('/')
            song = song[-1]
            # add to on screen playlist
            song_box.insert(END, song)



#init and create the player window
root = Tk()
root.title("Simple mp3 player")
root.geometry("300x360")

#playlist box
song_box = Listbox(root,bg="black", fg="grey",width = 60,selectbackground = "green", selectforeground= "black")
song_box.pack(pady=20)

#buttons label
nxt_btn = "Next"
pl_btn = "Play"
st_btn = "Stop"
prv_btn = "Previous"
pau_btn = "Pause"

#button icons
b_path="C:/Users/nrkal/PycharmProjects/simple_mp3/icons"
if os.path.exists(b_path):
    nxt_img_btn= PhotoImage(file="C:/Users/nrkal/PycharmProjects/simple_mp3/icons/next.png")
    pau_img_btn = PhotoImage(file="C:/Users/nrkal/PycharmProjects/simple_mp3/icons/pause.png")
    pl_img_btn = PhotoImage(file="C:/Users/nrkal/PycharmProjects/simple_mp3/icons/play-button.png")
    prv_img_btn =PhotoImage(file= "C:/Users/nrkal/PycharmProjects/simple_mp3/icons/back.png")
    st_img_btn= PhotoImage(file="C:/Users/nrkal/PycharmProjects/simple_mp3/icons/stop.png")
    vol_set_img = PhotoImage(file="C:/Users/nrkal/PycharmProjects/simple_mp3/icons/speaker.png")

ctr_frame = Frame(root)
ctr_frame.pack()



if os.path.exists(b_path):
    next_btn = Button(ctr_frame, image=nxt_img_btn, command=next_song)
    play_btn = Button(ctr_frame, image=pl_img_btn, command=play)
    stop_btn = Button(ctr_frame, image=st_img_btn, command=stop)
    pause_btn = Button(ctr_frame, image=pau_img_btn, command=lambda: pause(paused))
    previous_btn = Button(ctr_frame, image=prv_img_btn, command=previous_song)
    volume_set = Button(image=vol_set_img, command=adj_vol)

else:
    next_btn = Button(ctr_frame,text =nxt_btn,command = next_song)
    play_btn = Button(ctr_frame,text =pl_btn,command=play)
    stop_btn = Button(ctr_frame,text =st_btn,command=stop)
    pause_btn = Button(ctr_frame,text =pau_btn,command = lambda: pause(paused))
    previous_btn = Button(ctr_frame,text =prv_btn,command = previous_song)
    volume_set = Button(text="SET", command=adj_vol)

next_btn.grid(row=0,column=0,padx=5)
play_btn.grid(row=0,column=1,padx=5)
stop_btn.grid(row=0,column=2,padx=5)
pause_btn.grid(row=0,column=3,padx=5)
previous_btn.grid(row=0,column=4,padx=5)


#define menu

menu = Menu(root)
root.config(menu=menu)

#add song

add_song_menu = Menu(menu)
menu.add_cascade(label = "File",menu=add_song_menu)
add_song_menu.add_command(label = "Add One Song To Qeue", command = add_song)

#add multiple songs
add_song_menu.add_command(label = "Add Songs To Qeue", command = add_multiple_songs)

#delete songs and clear playlist
add_song_menu.add_command(label = "Delete Song From Qeue", command = delete_song)
add_song_menu.add_command(label="Clear All", command = clear_all)

add_song_menu.add_command(label="Save PlayList", command = save_pl)
add_song_menu.add_command(label="Load PlayList", command = load_pl)


#status bar
status_bar= Label(root,text='',bd=1,relief=GROOVE,anchor= E)
status_bar.pack(fill=X,side = BOTTOM,ipady=2)

#music slider
slider = ttk.Scale(root, from_=0, to = 100, orient=HORIZONTAL, length = 300, command = slide,value=0)
slider.pack(fill=X,pady =20)

#add volume textbox
vol_init = StringVar()
vol_init.set(int(pg.mixer.music.get_volume()*100))

#text="Input values between 0 or 100"

volume_text_box = Entry(root,textvariable = vol_init,width = 5)
volume_text_label= Label(text="VOLUME: ")
volume_text_label.pack(side=LEFT,padx=5)
volume_text_box.pack(side=LEFT,padx=5)
volume_set.pack(side=LEFT,padx=10)




root.mainloop()