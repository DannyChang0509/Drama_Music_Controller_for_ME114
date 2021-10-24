"""
Drama Music Controller for NYCU ME114

Designer: 張詠翔
"""
from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
import pygame

#GUI window setting
root = Tk()
root.title("Drama Music Controller")
root.geometry("1050x500")

#Init pygame mixer for play music
pygame.mixer.init()


def bgm_play():
    bgm = bgm_box.get(ACTIVE)
    pygame.mixer.Sound(bgm).play()


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


global stopped
stopped = False


def bgm_stop():
    global stopped
    stopped = True
    
    pygame.mixer.stop()
    bgm_box.select_clear(ACTIVE)


"""
def bgm_next_song():
    current = bgm_box.curselection()
    next_one = current[0]+1
    
    bgm = bgm_box.get(next_one)
    pygame.mixer.Sound(bgm).play()
    
    bgm_box.selection_clear(0, END)
    bgm_box.activate(next_one)
    bgm_box.selection_set(next_one, last=None)


def bgm_previous_song():
    current = bgm_box.curselection()
    next_one = current[0]-1
    
    bgm = bgm_box.get(next_one)
    pygame.mixer.Sound(bgm).play()
    
    bgm_box.selection_clear(0, END)
    bgm_box.activate(next_one)
    bgm_box.selection_set(next_one, last=None)
"""


def se_play():
    se = se_box.get(ACTIVE)
    pygame.mixer.music.load(se)
    pygame.mixer.music.play(loops=0)


def se_stop():
    pygame.mixer.music.stop()
    se_box.select_clear(ACTIVE)


def add_bgm():
    bgms = filedialog.askopenfilenames(initialdir='./music/', title="Choose a BGM", filetypes=(("mp3 Files", "*.mp3"), ))
    for bgm in bgms:
        bgm_box.insert(END, bgm)


def remove_bgm():
    bgm_stop()
    bgm_box.delete(ANCHOR)


def bgm_slide():
    pass


def bgm_volume():
    pass


def add_se():
    ses = filedialog.askopenfilenames(initialdir='./music/', title="Choose a SE", filetypes=(("mp3 Files", "*.mp3"), ))
    for se in ses:
        se_box.insert(END, se)


def remove_se():
    se_stop()
    se_box.delete(ANCHOR)


def se_slide():
    pass


def se_volume():
    pass


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
bgm_time_slider = ttk.Scale(bgm_frame, from_=0, to=100, orient=HORIZONTAL, command=bgm_slide, value=0, length=360)
bgm_time_slider.grid(row=3, column=0, padx=10)

se_time_slider = ttk.Scale(se_frame, from_=0, to=100, orient=HORIZONTAL, command=se_slide, value=0, length=360)
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

#Create designer label
designer = Label(root, text="設計:張詠翔", font=('標楷體', 12))
designer.pack(side='right')

root.mainloop()
