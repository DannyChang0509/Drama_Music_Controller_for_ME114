"""
Drama Music Controller for NYCU ME114

Designer: 張詠翔
"""
from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3

#GUI window setting
root = Tk()
root.title("抓馬盃音控軟體")
root.geometry("1050x550")

#Init pygame mixer for play music
pygame.mixer.init()


def bgm_play_time():
    if bgm_stopped:
        return
    
    current_time = play.get_length()
    current_time_f = time.strftime('%M:%S', time.gmtime(int(current_time)))
    
    song = './music/' + bgm_box.get(ACTIVE) + '.mp3'
    song_mut = MP3(song)
    
    song_length = song_mut.info.length
    song_length_f = time.strftime('%M:%S', time.gmtime(song_length))
    
    current_time += 1
    
    if int(bgm_time_slider.get()) == int(song_length):
        bgm_status_bar.config(text=f'{song_length_f} of {song_length_f}')
        bgm_stop()
    elif paused:
        pass
    elif int(bgm_time_slider.get()) == int(current_time):
        bgm_time_slider.config(to=int(song_length), value=int(current_time))
    else:
        bgm_time_slider.config(to=int(song_length), value=int(bgm_time_slider.get()))
        
        current_time_f = time.strftime('%M:%S', time.gmtime(int(bgm_time_slider.get())))
        
        bgm_time_slider.config(to=int(song_length), value=int(bgm_time_slider.get())+1)
    
        bgm_status_bar.config(text=f'{current_time_f} of {song_length_f}')
    
    bgm_status_bar.after(1000, bgm_play_time)


def se_play_time():
    if se_stopped:
        return
    
    current_time = pygame.mixer.music.get_pos() / 1000
    current_time_f = time.strftime('%M:%S', time.gmtime(int(current_time)))
    
    song = './music/' + se_box.get(ACTIVE) + '.mp3'
    song_mut = MP3(song)
    
    song_length = song_mut.info.length
    song_length_f = time.strftime('%M:%S', time.gmtime(song_length))
    
    current_time += 1
    
    if int(se_time_slider.get()) == int(song_length):
        se_status_bar.config(text=f'{song_length_f} of {song_length_f}')
        se_stop()
    elif int(se_time_slider.get()) == int(current_time):
        se_time_slider.config(to=int(song_length), value=int(current_time))
    else:
        se_time_slider.config(to=int(song_length), value=int(se_time_slider.get()))
        
        current_time_f = time.strftime('%M:%S', time.gmtime(int(se_time_slider.get())))
        
        se_time_slider.config(to=int(song_length), value=int(se_time_slider.get())+1)
    
        se_status_bar.config(text=f'{current_time_f} of {song_length_f}')
    
    se_status_bar.after(1000, se_play_time)


def bgm_play():
    bgm_stop()
    
    global bgm_stopped
    bgm_stopped = False
    
    bgm = './music/' + bgm_box.get(ACTIVE) + '.mp3'
    global play
    play = pygame.mixer.Sound(bgm)
    play.play()
    
    bgm_status_bar.config(text='')
    bgm_time_slider.config(value=0)
    
    bgm_play_time()


global paused
paused = False


def bgm_pause(is_paused):
    global paused
    paused = is_paused
    
    if paused:
        pygame.mixer.unpause()
        paused = False
    else:
        pygame.mixer.pause()
        paused = True


global bgm_stopped
bgm_stopped = False


def bgm_stop():
    global bgm_stopped
    bgm_stopped = True
    
    pygame.mixer.stop()
    bgm_box.select_clear(ACTIVE)
    
    bgm_status_bar.config(text='')
    bgm_time_slider.config(value=0)


"""
def bgm_next_song():
    bgm_stop()
    
    current = bgm_box.curselection()
    next_one = current[0]+1
    
    bgm = bgm_box.get(next_one)
    pygame.mixer.Sound(bgm).play()
    
    bgm_play_time()
    
    bgm_box.selection_clear(0, END)
    bgm_box.activate(next_one)
    bgm_box.selection_set(next_one, last=None)
    
    bgm_status_bar.config(text='')
    bgm_time_slider.config(value=0)


def bgm_previous_song():
    bgm_stop()
    
    current = bgm_box.curselection()
    next_one = current[0]-1
    
    bgm = bgm_box.get(next_one)
    pygame.mixer.Sound(bgm).play()
    
    bgm_play_time()
    
    bgm_box.selection_clear(0, END)
    bgm_box.activate(next_one)
    bgm_box.selection_set(next_one, last=None)
    
    bgm_status_bar.config(text='')
    bgm_time_slider.config(value=0)
"""


def se_play():
    se_stop()
    
    global se_stopped
    se_stopped = False
    
    se = './music/' + se_box.get(ACTIVE) + '.mp3'
    pygame.mixer.music.load(se)
    pygame.mixer.music.play(loops=0)
    
    se_status_bar.config(text='')
    se_time_slider.config(value=0)
    
    se_play_time()


global se_stopped
se_stopped = False


def se_stop():
    global se_stopped
    se_stopped = True
    
    pygame.mixer.music.stop()
    se_box.select_clear(ACTIVE)
    
    se_status_bar.config(text='')
    se_time_slider.config(value=0)


def add_bgm():
    bgms = filedialog.askopenfilenames(initialdir='./music/', title="Choose a BGM", filetypes=(("mp3 Files", "*.mp3"), ))
    for bgm in bgms:
        tem = bgm.split('/')
        bgm = tem[-1][:-4]
        bgm_box.insert(END, bgm)
        BGM.append(bgm)
    file = open('./music.dat', mode='w')
    file.write('BGM\n')
    for s in BGM:
        file.write(s+'\n')
    file.write('SE\n')
    for s in SE:
        file.write(s+'\n')
    file.close()


def remove_bgm():
    bgm_stop()
    BGM.remove(bgm_box.get(ACTIVE))
    bgm_box.delete(ANCHOR)
    
    file = open('./music.dat', mode='w')
    file.write('BGM\n')
    for s in BGM:
        file.write(s+'\n')
    file.write('SE\n')
    for s in SE:
        file.write(s+'\n')
    file.close()


def bgm_volume(x):
    play.set_volume(bgm_volume_slider.get())
    current_volume = play.get_volume()
    show_bgm_volume.config(text=f'{int(current_volume*100)}%')


def add_se():
    ses = filedialog.askopenfilenames(initialdir='./music/', title="Choose a SE", filetypes=(("mp3 Files", "*.mp3"), ))
    for se in ses:
        tem = se.split('/')
        se = tem[-1][:-4]
        se_box.insert(END, se)
        SE.append(se)
    file = open('./music.dat', mode='w')
    file.write('BGM\n')
    for s in BGM:
        file.write(s+'\n')
    file.write('SE\n')
    for s in SE:
        file.write(s+'\n')
    file.close()


def remove_se():
    se_stop()
    SE.remove(se_box.get(ACTIVE))
    se_box.delete(ANCHOR)
    
    file = open('./music.dat', mode='w')
    file.write('BGM\n')
    for s in BGM:
        file.write(s+'\n')
    file.write('SE\n')
    for s in SE:
        file.write(s+'\n')
    file.close()


def se_volume(x):
    pygame.mixer.music.set_volume(se_volume_slider.get())
    current_volume = pygame.mixer.music.get_volume()
    show_se_volume.config(text=f'{int(current_volume*100)}%')


#Create title
title = Label(root, text="抓馬盃音控軟體", font=('標楷體', 30))
title.pack()

#Create master, bgm, se frame
master_frame = Frame(root)
master_frame.pack(pady=20)

bgm_frame = LabelFrame(master_frame, text='BGM')
bgm_frame.grid(row=0, column=0, padx=10)

se_frame = LabelFrame(master_frame, text='SE')
se_frame.grid(row=0, column=1, padx=10)

#Create music box
bgm_box = Listbox(bgm_frame, width=50)
bgm_box.grid(row=1, column=0, pady=10)

se_box = Listbox(se_frame, width=50)
se_box.grid(row=1, column=0, pady=10)

#Insert music to music box
file = open('./music.dat', mode='r')

music = file.readlines()

BGM = []
SE = []

i = ''

for s in music:
    s = s.strip()
    if s == 'BGM':
        i = 'b'
    elif s =='SE':
        i = 's'
    else:
        if i == 'b':
            bgm_box.insert(END, s)
            BGM.append(s)
        elif i == 's':
            se_box.insert(END, s)
            SE.append(s)
    
file.close()

#Create controllers' frame
bgm_controls_frame = Frame(bgm_frame)
bgm_controls_frame.grid(row=2, column=0, pady=10)

se_controls_frame = Frame(se_frame)
se_controls_frame.grid(row=2, column=0, pady=10)

#Create music managers' frame
bgm_managers_frame = Frame(bgm_frame)
bgm_managers_frame.grid(row=0, column=0, sticky=E, padx=40)

se_managers_frame = Frame(se_frame)
se_managers_frame.grid(row=0, column=0, sticky=E, padx=40)

#Create volume frame
bgm_volume_frame = LabelFrame(bgm_frame, text="BGM Volume")
bgm_volume_frame.grid(row=1, column=1, padx=10)

se_volume_frame = LabelFrame(se_frame, text="SE Volume")
se_volume_frame.grid(row=1, column=1, padx=10)

#Create button images
play_image = PhotoImage(file='./img/play.png').subsample(3)
pause_image = PhotoImage(file='./img/pause.png').subsample(3)
stop_image = PhotoImage(file='./img/stop.png').subsample(3)
add_image = PhotoImage(file='./img/add.png').subsample(10)
remove_image = PhotoImage(file='./img/remove.png').subsample(10)

#Create music managers
add_bgm_btn = Button(bgm_managers_frame, image=add_image, command=add_bgm)
add_bgm_btn.grid(row=0, column=0, padx=3)

remove_bgm_btn = Button(bgm_managers_frame, image=remove_image, command=remove_bgm)
remove_bgm_btn.grid(row=0, column=1, padx=3)

add_se_btn = Button(se_managers_frame, image=add_image, command=add_se)
add_se_btn.grid(row=0, column=0, padx=3)

remove_se_btn = Button(se_managers_frame, image=remove_image, command=remove_se)
remove_se_btn.grid(row=0, column=1, padx=3)

#Create controllers
bgm_play_btn = Button(bgm_controls_frame, image=play_image, command=bgm_play)
bgm_play_btn.grid(row=0, column=1, padx=10)

bgm_pause_btn = Button(bgm_controls_frame, image=pause_image, command=lambda: bgm_pause(paused))
bgm_pause_btn.grid(row=0, column=0, padx=10)

bgm_stop_btn = Button(bgm_controls_frame, image=stop_image, command=bgm_stop)
bgm_stop_btn.grid(row=0, column=2, padx=10)

"""
bgm_next_btn = Button(bgm_controls_frame, text="Next", command=bgm_next_song)
bgm_next_btn.grid(row=0, column=3, padx=5)

bgm_previous_btn = Button(bgm_controls_frame, text="Previous", command=bgm_previous_song)
bgm_previous_btn.grid(row=0, column=4, padx=5)
"""

se_play_btn = Button(se_controls_frame, image=play_image, command=se_play)
se_play_btn.grid(row=0, column=0, padx=10)

se_stop_btn = Button(se_controls_frame, image=stop_image, command=se_stop)
se_stop_btn.grid(row=0, column=1, padx=10)

#Create music position slider
bgm_time_slider = ttk.Scale(bgm_frame, from_=0, to=100, orient=HORIZONTAL, value=0, length=360)
bgm_time_slider.grid(row=3, column=0, padx=10)

se_time_slider = ttk.Scale(se_frame, from_=0, to=100, orient=HORIZONTAL, value=0, length=360)
se_time_slider.grid(row=3, column=0, padx=10)


#Create volume slider
bgm_volume_slider = ttk.Scale(bgm_volume_frame, from_=0, to=1, orient=VERTICAL, command=bgm_volume, value=1, length=150)
bgm_volume_slider.pack()

se_volume_slider = ttk.Scale(se_volume_frame, from_=0, to=1, orient=VERTICAL, command=se_volume, value=1, length=150)
se_volume_slider.pack()


#Create show volume label
show_bgm_volume = Label(bgm_volume_frame, text='100%')
show_bgm_volume.pack(pady=5)

show_se_volume = Label(se_volume_frame, text='100%')
show_se_volume.pack(pady=5)


#Create ststus bar
bgm_status_bar = Label(bgm_frame, text='', bd=1, relief=GROOVE, anchor=E)
bgm_status_bar.grid(row=4, pady=10)

se_status_bar = Label(se_frame, text='', bd=1, relief=GROOVE, anchor=E)
se_status_bar.grid(row=4, pady=10)

#Create schedule frame
schedule_frame = LabelFrame(root, text='排程')
schedule_frame.pack(ipadx=30, ipady=10)

#Create schedule controller
schedule_btn = Button(schedule_frame, text='排程', font=('標楷體', 16))
schedule_btn.pack(side='left', padx=10)

start_btn = Button(schedule_frame, text='開始', font=('標楷體', 16))
start_btn.pack(side='left', padx=10)

schedule_time_slider = ttk.Scale(schedule_frame, from_=0, to=100, orient=HORIZONTAL, value=0, length=600)
schedule_time_slider.pack(side='left', padx=50)

schedule_status_bar = Label(schedule_frame, text='', bd=1, relief=GROOVE, anchor=E)
schedule_status_bar.pack(side='left', padx=10)

#Create designer label
designer = Label(root, text="設計:張詠翔", font=('標楷體', 12), anchor=E)
designer.pack(fill=X, side=BOTTOM)

root.mainloop()
