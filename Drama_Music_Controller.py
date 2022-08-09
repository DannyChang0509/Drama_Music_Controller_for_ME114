"""
Drama Music Controller for NYCU ME114

Designer: 張詠翔
"""
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3

# GUI window setting
root = Tk()
root.title("抓馬盃音控軟體")
root.geometry("1050x550")

# Init pygame mixer for play music
pygame.mixer.init()


def bgm_play_time(x, n):
    if bgm_stopped:
        return

    current_time = x
    current_time_f = time.strftime("%M:%S", time.gmtime(int(current_time)))

    song = "./music/" + bgm_box.get(n) + ".mp3"
    song_mut = MP3(song)

    song_length = song_mut.info.length
    song_length_f = time.strftime("%M:%S", time.gmtime(song_length))

    if int(bgm_time_slider.get()) == int(song_length):
        bgm_status_bar.config(text=f"{song_length_f} of {song_length_f}")
        bgm_stop()
    elif bgm_paused:
        pass
    else:
        bgm_time_slider.config(to=int(song_length), value=int(current_time))

        current_time_f = time.strftime("%M:%S", time.gmtime(int(current_time)))

        bgm_status_bar.config(text=f"{current_time_f} of {song_length_f}")

        current_time += 1

    bgm_status_bar.after(1000, lambda: bgm_play_time(current_time, n))


def se_play_time(x, n):
    if se_stopped:
        return

    current_time = x
    current_time_f = time.strftime("%M:%S", time.gmtime(current_time))

    song = "./music/" + se_box.get(n) + ".mp3"
    song_mut = MP3(song)

    song_length = song_mut.info.length
    song_length_f = time.strftime("%M:%S", time.gmtime(song_length))

    if int(se_time_slider.get()) == int(song_length):
        se_status_bar.config(text=f"{song_length_f} of {song_length_f}")
        se_stop()
    else:
        se_time_slider.config(to=int(song_length), value=current_time)

        current_time_f = time.strftime("%M:%S", time.gmtime(current_time))

        se_status_bar.config(text=f"{current_time_f} of {song_length_f}")

        current_time += 1

    se_status_bar.after(1000, lambda: se_play_time(current_time, n))


def bgm_play(n):
    pygame.mixer.stop()

    global bgm_stopped
    bgm_stopped = False

    if n == -1:
        n = ACTIVE
    bgm = "./music/" + bgm_box.get(n) + ".mp3"
    global play
    play = pygame.mixer.Sound(bgm)
    play.play()

    bgm_status_bar.config(text="")
    bgm_time_slider.config(value=0)

    bgm_play_time(0, n)


global bgm_paused
bgm_paused = False


def bgm_pause(is_paused):
    global bgm_paused
    bgm_paused = is_paused

    if bgm_paused:
        pygame.mixer.unpause()
        bgm_paused = False
    else:
        pygame.mixer.pause()
        bgm_paused = True


global bgm_stopped
bgm_stopped = False


def bgm_stop():
    global bgm_stopped
    bgm_stopped = True

    pygame.mixer.stop()
    bgm_box.select_clear(ACTIVE)

    bgm_status_bar.config(text="")
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


def se_play(n):
    pygame.mixer.music.stop()

    global se_stopped
    se_stopped = False

    if n == -1:
        n = ACTIVE
    se = "./music/" + se_box.get(n) + ".mp3"
    pygame.mixer.music.load(se)
    pygame.mixer.music.play(loops=0)

    se_status_bar.config(text="")
    se_time_slider.config(value=0)

    se_play_time(0, n)


global se_stopped
se_stopped = False


def se_stop():
    global se_stopped
    se_stopped = True

    pygame.mixer.music.stop()
    se_box.select_clear(ACTIVE)

    se_status_bar.config(text="")
    se_time_slider.config(value=0)


def add_bgm():
    bgms = filedialog.askopenfilenames(
        initialdir="./music/", title="Choose a BGM", filetypes=(("mp3 Files", "*.mp3"),)
    )
    for bgm in bgms:
        tem = bgm.split("/")
        bgm = tem[-1][:-4]
        bgm_box.insert(END, bgm)
        BGM.append(bgm)
    file = open("./music.dat", mode="w")
    file.write("BGM\n")
    for s in BGM:
        file.write(s + "\n")
    file.write("SE\n")
    for s in SE:
        file.write(s + "\n")
    file.close()


def remove_bgm():
    global bgm_stopped
    bgm_stopped = True

    pygame.mixer.stop()

    bgm_status_bar.config(text="")
    bgm_time_slider.config(value=0)

    if bgm_box.curselection():
        bgm_stop()
        BGM.remove(bgm_box.get(ACTIVE))
        bgm_box.delete(ANCHOR)

        file = open("./music.dat", mode="w")
        file.write("BGM\n")
        for s in BGM:
            file.write(s + "\n")
        file.write("SE\n")
        for s in SE:
            file.write(s + "\n")
        file.close()
    else:
        messagebox.showwarning("提示", "請選擇欲刪除之音樂")


def bgm_volume(x):
    play.set_volume(bgm_volume_slider.get())
    current_volume = play.get_volume()
    show_bgm_volume.config(text=f"{int(current_volume*100)}%")


def add_se():
    ses = filedialog.askopenfilenames(
        initialdir="./music/", title="Choose a SE", filetypes=(("mp3 Files", "*.mp3"),)
    )
    for se in ses:
        tem = se.split("/")
        se = tem[-1][:-4]
        se_box.insert(END, se)
        SE.append(se)
    file = open("./music.dat", mode="w")
    file.write("BGM\n")
    for s in BGM:
        file.write(s + "\n")
    file.write("SE\n")
    for s in SE:
        file.write(s + "\n")
    file.close()


def remove_se():
    global se_stopped
    se_stopped = True

    pygame.mixer.music.stop()

    se_status_bar.config(text="")
    se_time_slider.config(value=0)

    if se_box.curselection():
        SE.remove(se_box.get(ACTIVE))
        se_box.delete(ANCHOR)

        file = open("./music.dat", mode="w")
        file.write("BGM\n")
        for s in BGM:
            file.write(s + "\n")
        file.write("SE\n")
        for s in SE:
            file.write(s + "\n")
        file.close()
    else:
        messagebox.showwarning("提示", "請選擇欲刪除之音效")


def se_volume(x):
    pygame.mixer.music.set_volume(se_volume_slider.get())
    current_volume = pygame.mixer.music.get_volume()
    show_se_volume.config(text=f"{int(current_volume*100)}%")


# Create title
title = Label(root, text="抓馬盃音控軟體", font=("標楷體", 30))
title.pack()

# Create master, bgm, se frame
master_frame = Frame(root)
master_frame.pack(pady=20)

bgm_frame = LabelFrame(master_frame, text="BGM")
bgm_frame.grid(row=0, column=0, padx=10)

se_frame = LabelFrame(master_frame, text="SE")
se_frame.grid(row=0, column=1, padx=10)

# Create music box
bgm_box = Listbox(bgm_frame, width=50)
bgm_box.grid(row=1, column=0, pady=10)

se_box = Listbox(se_frame, width=50)
se_box.grid(row=1, column=0, pady=10)

# Insert music to music box
file = open("./music.dat", mode="r")

music = file.readlines()

BGM = []
SE = []

i = ""

for s in music:
    s = s.strip()
    if s == "BGM":
        i = "b"
    elif s == "SE":
        i = "s"
    else:
        if i == "b":
            bgm_box.insert(END, s)
            BGM.append(s)
        elif i == "s":
            se_box.insert(END, s)
            SE.append(s)

file.close()

# Create controllers' frame
bgm_controls_frame = Frame(bgm_frame)
bgm_controls_frame.grid(row=2, column=0, pady=10)

se_controls_frame = Frame(se_frame)
se_controls_frame.grid(row=2, column=0, pady=10)

# Create music managers' frame
bgm_managers_frame = Frame(bgm_frame)
bgm_managers_frame.grid(row=0, column=0, sticky=E, padx=10)

se_managers_frame = Frame(se_frame)
se_managers_frame.grid(row=0, column=0, sticky=E, padx=10)

# Create volume frame
bgm_volume_frame = LabelFrame(bgm_frame, text="BGM Volume")
bgm_volume_frame.grid(row=1, column=1, padx=10)

se_volume_frame = LabelFrame(se_frame, text="SE Volume")
se_volume_frame.grid(row=1, column=1, padx=10)

# Create button images
play_image = PhotoImage(file="./img/play.png").subsample(3)
pause_image = PhotoImage(file="./img/pause.png").subsample(3)
stop_image = PhotoImage(file="./img/stop.png").subsample(3)
add_image = PhotoImage(file="./img/add.png").subsample(10)
remove_image = PhotoImage(file="./img/remove.png").subsample(10)

# Create music managers
add_bgm_btn = Button(bgm_managers_frame, image=add_image, command=add_bgm)
add_bgm_btn.grid(row=0, column=0, padx=3)

remove_bgm_btn = Button(bgm_managers_frame, image=remove_image, command=remove_bgm)
remove_bgm_btn.grid(row=0, column=1, padx=3)

add_se_btn = Button(se_managers_frame, image=add_image, command=add_se)
add_se_btn.grid(row=0, column=0, padx=3)

remove_se_btn = Button(se_managers_frame, image=remove_image, command=remove_se)
remove_se_btn.grid(row=0, column=1, padx=3)

# Create controllers
bgm_play_btn = Button(
    bgm_controls_frame, image=play_image, command=lambda: bgm_play(-1)
)
bgm_play_btn.grid(row=0, column=1, padx=10)

bgm_pause_btn = Button(
    bgm_controls_frame, image=pause_image, command=lambda: bgm_pause(bgm_paused)
)
bgm_pause_btn.grid(row=0, column=0, padx=10)

bgm_stop_btn = Button(bgm_controls_frame, image=stop_image, command=bgm_stop)
bgm_stop_btn.grid(row=0, column=2, padx=10)

"""
bgm_next_btn = Button(bgm_controls_frame, text="Next", command=bgm_next_song)
bgm_next_btn.grid(row=0, column=3, padx=5)

bgm_previous_btn = Button(bgm_controls_frame, text="Previous", command=bgm_previous_song)
bgm_previous_btn.grid(row=0, column=4, padx=5)
"""

se_play_btn = Button(se_controls_frame, image=play_image, command=lambda: se_play(-1))
se_play_btn.grid(row=0, column=0, padx=10)

se_stop_btn = Button(se_controls_frame, image=stop_image, command=se_stop)
se_stop_btn.grid(row=0, column=1, padx=10)

# Create music position slider
bgm_time_slider = ttk.Scale(
    bgm_frame, from_=0, to=100, orient=HORIZONTAL, value=0, length=360
)
bgm_time_slider.grid(row=3, column=0, padx=10)

se_time_slider = ttk.Scale(
    se_frame, from_=0, to=100, orient=HORIZONTAL, value=0, length=360
)
se_time_slider.grid(row=3, column=0, padx=10)


# Create volume slider
bgm_volume_slider = ttk.Scale(
    bgm_volume_frame,
    from_=0,
    to=1,
    orient=VERTICAL,
    command=bgm_volume,
    value=1,
    length=150,
)
bgm_volume_slider.pack()

se_volume_slider = ttk.Scale(
    se_volume_frame,
    from_=0,
    to=1,
    orient=VERTICAL,
    command=se_volume,
    value=1,
    length=150,
)
se_volume_slider.pack()


# Create show volume label
show_bgm_volume = Label(bgm_volume_frame, text="100%")
show_bgm_volume.pack(pady=5)

show_se_volume = Label(se_volume_frame, text="100%")
show_se_volume.pack(pady=5)


# Create ststus bar
bgm_status_bar = Label(bgm_frame, text="", bd=1, relief=GROOVE, anchor=E)
bgm_status_bar.grid(row=4, pady=10)

se_status_bar = Label(se_frame, text="", bd=1, relief=GROOVE, anchor=E)
se_status_bar.grid(row=4, pady=10)

# Create schedule frame
schedule_frame = LabelFrame(root, text="排程")
schedule_frame.pack(ipadx=30, ipady=10)


def schedule():
    # sub-window setting
    schedule_window = Toplevel(root)
    schedule_window.geometry("320x320")
    schedule_window.title("排程")

    # Create title
    title = Label(schedule_window, text="排程", font=("標楷體", 16))
    title.pack()

    # Create controllers' frame
    controllers_frame = Frame(schedule_window)
    controllers_frame.pack(pady=10)

    # Create main frame
    main_frame = Frame(schedule_window)
    main_frame.pack(pady=10)

    # Create managers' frame
    manager_frame = Frame(main_frame)
    manager_frame.grid(row=0, column=1, sticky=E, padx=10)

    # Create confirm frame
    confirm_frame = Frame(schedule_window)
    confirm_frame.pack(pady=10)

    # Create main box
    time_box = Listbox(main_frame, width=5)
    time_box.grid(row=1, column=0, padx=10)

    music_box = Listbox(main_frame, width=30)
    music_box.grid(row=1, column=1, padx=10)

    # Create list: [time_min, time_sec, music_name]
    file = open("./schedule.dat", mode="r")

    schedules = file.readlines()

    schedule_list = []

    for s in schedules:
        schedule_list.append(s.split())
        time_min, time_sec, music_name = schedule_list[-1]
        time_box.insert(END, f"{time_min}:{time_sec}")
        music_box.insert(END, music_name)

    file.close()

    def check():
        minute_g = minute.get()
        if len(minute_g) < 2:
            minute_g = "0" + minute_g
        else:
            minute_g = minute.get()
        second_g = second.get()
        if len(second_g) < 2:
            second_g = "0" + second_g
        else:
            second_g = second.get()

        schedule_list.append([minute_g, second_g, music.get()])

        if schedule_list.count(schedule_list[-1]) > 1:
            messagebox.showerror("錯誤", "程序重複")
            schedule_list.pop(-1)
        else:
            # Sorting
            schedule_list.sort(key=lambda x: x[1])
            schedule_list.sort(key=lambda x: x[0])

            time_box.delete(0, "end")
            music_box.delete(0, "end")

            file = open("./schedule.dat", mode="w")
            for time_min, time_sec, music_name in schedule_list:
                time_box.insert(END, f"{time_min}:{time_sec}")
                music_box.insert(END, music_name)
                file.write(f"{time_min} {time_sec} {music_name}\n")
            file.close()

    # Create controllers
    minute = Spinbox(controllers_frame, from_=0, to=59, width=2, wrap=True)
    minute.grid(row=0, column=0)

    colon = Label(controllers_frame, text=":", font=("標楷體", 12))
    colon.grid(row=0, column=1)

    second = Spinbox(controllers_frame, from_=0, to=59, width=2, wrap=True)
    second.grid(row=0, column=2)

    music = ttk.Combobox(controllers_frame)
    music.grid(row=0, column=3, padx=10)

    check_btn = Button(controllers_frame, text="確定", command=check)
    check_btn.grid(row=0, column=4)

    # Reset combobox
    music["value"] = BGM + SE

    def delete():
        def delete_():
            time_box.delete(anchor)
            music_box.delete(anchor)
            schedule_list.pop(anchor[0])

            file = open("./schedule.dat", mode="w")
            for time_min, time_sec, music_name in schedule_list:
                file.write(f"{time_min} {time_sec} {music_name}\n")
            file.close()

        if music_box.curselection():
            anchor = music_box.curselection()
            delete_()
        elif time_box.curselection():
            anchor = time_box.curselection()
            delete_()
        else:
            messagebox.showwarning("提示", "請選擇欲刪除之程序")

    # Create managers
    remove_btn = Button(manager_frame, image=remove_image, command=delete)
    remove_btn.grid(row=0, column=0)

    def reset():
        time_box.delete(0, "end")
        music_box.delete(0, "end")
        schedule_list.clear()
        file = open("./schedule.dat", mode="r+")
        file.truncate(0)
        file.close()

    def confirm():
        schedule_window.destroy()

    # Create confirm btns
    confirm_btn = Button(confirm_frame, text="完成", command=confirm)
    confirm_btn.grid(row=0, column=0, padx=10)

    reset_btn = Button(confirm_frame, text="重設", command=reset)
    reset_btn.grid(row=0, column=1, padx=10)


def schedule_play_time(x):
    if len(time_list) == 0:
        messagebox.showwarning("警告", "請排程")
        return

    if stopped:
        schedule_time_slider.config(value=0)
        schedule_status_bar.config(text="")
        return

    current_time = x
    current_time_f = time.strftime("%M:%S", time.gmtime(current_time))

    for i in range(len(music_name_list) - 1, -1, -1):
        if music_name_list[i] in BGM:
            last_song = "./music/" + music_name_list[i] + ".mp3"
            break

    last_song_mut = MP3(last_song)

    last_song_length = last_song_mut.info.length

    tem = time_list[i].split(":")
    length = int(tem[0]) * 60 + int(tem[1]) + last_song_length
    length_f = time.strftime("%M:%S", time.gmtime(length))

    if int(schedule_time_slider.get()) == int(length):
        schedule_status_bar.config(text=f"{length_f} of {length_f}")
    elif paused or bgm_paused:
        pass
    else:
        schedule_time_slider.config(to=int(length), value=current_time)

        current_time_f = time.strftime("%M:%S", time.gmtime(current_time))

        schedule_status_bar.config(text=f"{current_time_f} of {length_f}")

        if current_time_f in time_list:
            if music_name_list[time_list.index(current_time_f)] in BGM:
                bgm_stop()

                bgm_status_bar.config(text="")
                bgm_time_slider.config(value=0)
                bgm_box.select_clear(0, END)

                for n in range(bgm_box.size()):
                    if (
                        bgm_box.get(n)
                        == music_name_list[time_list.index(current_time_f)]
                    ):
                        bgm_box.select_set(n)
                        bgm_play(n)
                        break
            elif music_name_list[time_list.index(current_time_f)] in SE:
                se_stop()

                se_status_bar.config(text="")
                se_time_slider.config(value=0)
                se_box.select_clear(0, END)

                for n in range(se_box.size()):
                    if (
                        se_box.get(n)
                        == music_name_list[time_list.index(current_time_f)]
                    ):
                        se_box.select_set(n)
                        se_play(n)
                        break

        current_time += 1

    schedule_status_bar.after(1000, lambda: schedule_play_time(current_time))


def start():
    global stopped
    stopped = False

    global paused
    paused = False

    # Read schedule
    file = open("./schedule.dat", mode="r")

    schedules = file.readlines()

    global time_list, music_name_list
    time_list = []
    music_name_list = []

    for s in schedules:
        tem = s.split()
        time_list.append(tem[0] + ":" + tem[1])
        music_name_list.append(tem[2])

    file.close()

    schedule_play_time(0)


global stopped
stopped = False


def stop():
    bgm_stop()
    se_stop()
    global stopped
    stopped = True


global paused
paused = False


def pause(is_paused):
    bgm_pause(is_paused)

    global paused
    paused = is_paused

    if paused:
        paused = False
    else:
        paused = True


# Create schedule controller
schedule_btn = Button(schedule_frame, text="排程", font=("標楷體", 16), command=schedule)
schedule_btn.pack(side="left", padx=10)

pause_btn = Button(
    schedule_frame, image=pause_image, font=("標楷體", 16), command=lambda: pause(paused)
)
pause_btn.pack(side="left", padx=10)

start_btn = Button(schedule_frame, image=play_image, font=("標楷體", 16), command=start)
start_btn.pack(side="left", padx=10)

stop_btn = Button(schedule_frame, image=stop_image, font=("標楷體", 16), command=stop)
stop_btn.pack(side="left", padx=10)

schedule_time_slider = ttk.Scale(
    schedule_frame, from_=0, to=100, orient=HORIZONTAL, value=0, length=500
)
schedule_time_slider.pack(side="left", padx=30)

schedule_status_bar = Label(schedule_frame, text="", bd=1, relief=GROOVE, anchor=E)
schedule_status_bar.pack(side="left", padx=10)

# Create designer label
designer = Label(root, text="設計:張詠翔", font=("標楷體", 12), anchor=E)
designer.pack(fill=X, side=BOTTOM)

root.mainloop()
