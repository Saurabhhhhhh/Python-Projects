# ------------------------------------All modules-----------------------------------------------
from tkinter import *
import pygame
from win32api import GetSystemMetrics 
from mutagen.mp3 import MP3
import audio_metadata
from PIL import Image, ImageTk
from io import BytesIO
import eyed3
from tkinter import filedialog
import os
import time
import tkinter.ttk as ttk
from ttkthemes import themed_tk as tk

# ------------------------------------All initialisation-----------------------------------------------
pygame.init()
pygame.mixer.init()

# ------------------------------------All functions-----------------------------------------------
def Music_list():
    global music_box, nextOne
    musiclist = Toplevel(root)
    musiclist.geometry('500x500')  
    musiclist.title('Song List')
    music_box = Listbox(musiclist, width=100,height=100, bg= 'white', fg= 'black', selectbackground= 'cyan', selectforeground= 'black')
    music_box.pack()

    mmenu = Menu(musiclist)
    m1= Menu(mmenu,tearoff=0)
    m1.add_command(label = "Choose From Folder", command = song_list)
    mmenu.add_cascade(label = "Add Songs", menu = m1)
    musiclist.config(menu=mmenu)

    m2 = Menu(mmenu,tearoff=0)
    m2.add_command(label = "Play All", command = None)
    m2.add_command(label = "Delete Current Song", command = delete_song)
    m2.add_command(label = "Delete All Songs", command = delete_songs)
    mmenu.add_cascade(label = "Options", menu = m2)
    musiclist.config(menu=mmenu)

def song_list():
    global file, length
    files = filedialog.askopenfilenames(title = "Choose songs")
    file = list(files)
    length = len(file)
    n = 0
    for i in range(length):

        name = os.path.basename(file[n])
        music_box.insert(END, name)
        n +=1

def current_canvas(image_path):
    global final_img, nextOne
    canvas.delete('all')
    try:
        metadata = audio_metadata.load(image_path) #file[indexs[0]]
        artwork = metadata.pictures[0].data
        stream = BytesIO(artwork)

        img = Image.open(stream)
        img = img.resize((150, 150))
        final_img = ImageTk.PhotoImage(img)
        canvas.create_image(300, 174, anchor = NW, image= final_img)
    except Exception as e:
        canvas.create_image(300, 174, anchor = NW, image= final_init)
    
    audiofile = eyed3.load(image_path)
    Artist = audiofile.tag.artist
    Title = audiofile.tag.title        

    canvas.create_text(642, 200, text = Title, fill = 'black', font = ('bahnschrift 15 bold'))
    canvas.create_text(648, 230, text = f'- {Artist}', fill = '#BCC6CC', font = ('corbal 13 '))

def default_canvas():
    global final_init
    init = Image.open('assest\Defaut_cover.jpg')
    init = init.resize((150, 150))
    final_init = ImageTk.PhotoImage(init)

    canvas.create_image(300, 174, anchor = NW, image= final_init)
    canvas.create_text(642, 200, text = "Hello Welcome To The", fill = 'black', font = ('bahnschrift 15 bold'))
    canvas.create_text(648, 230, text = 'World Of Music', fill = '#BCC6CC', font = ('corbal 13 '))

def play():
    global Play_key, indexs, nextOne, stopped, length
    
    if Play_key == 0:
        pause_btn.config(image= play_btn_img)
        stopped = False
        indexs = list(music_box.curselection())
        nextOne = indexs[0]

        pygame.mixer.music.load(file[indexs[0]])
        pygame.mixer.music.set_volume(volume_slider.get())
        pygame.mixer.music.play(loops=0)
        Play_key = 1

        current_canvas(file[indexs[0]])
        play_time()

            

    elif Play_key == 1:
        pause_btn.config(image=pause_btn_img)
        pygame.mixer.music.set_volume(volume_slider.get())
        pygame.mixer.music.pause()
        Play_key = 2
    else:
        pygame.mixer.music.set_volume(volume_slider.get())
        pygame.mixer.music.unpause()
        pause_btn.config(image=play_btn_img)
        Play_key = 1

def stop():
    global Play_key, song_position, stopped
    canvas.delete("all")
    song_position.config(text="00:00")
    song_slider.config(value= 0)
    pygame.mixer.music.stop()
    music_box.select_clear(ACTIVE)
    pause_btn.config(image=pause_btn_img)
    indexs.clear()
    Play_key = 0
    default_canvas()
    stopped = True

def forward():
    global nextOne, music_box
    if nextOne + 1 == len(file):
        pygame.mixer.music.load(file[nextOne])
        current_canvas(file[nextOne])
        pygame.mixer.music.set_volume(volume_slider.get())
        pygame.mixer.music.play(loops=0) 

        music_box.selection_clear(0, END)
        music_box.activate(nextOne)
        music_box.selection_set(nextOne, last = None)
    else:       
        nextOne += 1
        song_position.config(text="00:00")
        song_slider.config(value= 0)
        pygame.mixer.music.load(file[nextOne])
        current_canvas(file[nextOne])
        pygame.mixer.music.set_volume(volume_slider.get())
        pygame.mixer.music.play(loops=0)

        music_box.selection_clear(0, END)
        music_box.activate(nextOne)
        music_box.selection_set(nextOne, last = None)
       
def back():
    global nextOne
    if nextOne == 0:
        pygame.mixer.music.load(file[nextOne])
        current_canvas(file[nextOne])
        pygame.mixer.music.set_volume(volume_slider.get())
        pygame.mixer.music.play(loops=0)

        music_box.selection_clear(0, END)
        music_box.activate(nextOne)
        music_box.selection_set(nextOne, last = None)
    else:
        nextOne -= 1
        song_position.config(text="00:00")
        song_slider.config(value= 0)
        pygame.mixer.music.load(file[nextOne])
        current_canvas(file[nextOne])
        pygame.mixer.music.set_volume(volume_slider.get())
        pygame.mixer.music.play(loops=0)

        music_box.selection_clear(0, END)
        music_box.activate(nextOne)
        music_box.selection_set(nextOne, last = None)

def delete_song():
    global music_box

    music_box.delete(ANCHOR)
    stop()

def delete_songs():
    global music_box
    music_box.delete(0, END)
    stop()

def play_time():
    global song_length, Play_key, stopped
    if stopped:
        return

    current_time = pygame.mixer.music.get_pos() /1000

    # slider_label.config(text=f'Slider: {int(song_slider.get())} and Song Pos: {int(current_time)}')

    final_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    song_mut = MP3(file[nextOne])
    song_length = song_mut.info.length
    final_song_length = time.strftime('%M:%S',time.gmtime(song_length))
    current_time += 1

    if int(song_slider.get()) == int(song_length):
        song_position.config(text= int(song_length))
        
    elif Play_key == 2:
        pass

    elif int(song_slider.get()) == int(current_time):
        #Slider hasn't move
        song_slider.config(to=int(song_length), value= int(current_time))
    else:
        #Slider has moved
        song_slider.config(to=int(song_length), value= int(song_slider.get()))
        final_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))
        # slider_label.config(text= f"{int(song_slider.get())} of {int(song_length)}")

        next_time = int(song_slider.get()) + 1
        song_slider.config(value= next_time)

    song_position.config(text = final_current_time)
    # song_slider.config(value=int(current_time))

    
    

    song_position.after(1000, play_time)

def slide(X):
    global file, indexs
    #slider_label.config(text= f"{int(song_slider.get())} of {int(song_length)}")
    pygame.mixer.music.load(file[indexs[0]])
    pygame.mixer.music.set_volume(volume_slider.get())
    pygame.mixer.music.play(loops=0, start= int(song_slider.get()) )

def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    current_volume.config(text= f'{int(volume_slider.get()*100)}%')

# ------------------------------------All variables-----------------------------------------------
WIDTH = GetSystemMetrics(0)
HEIGHT = GetSystemMetrics(1)
width = int(WIDTH*0.8)
height = int(HEIGHT*0.7) +1
resolution = str(width) + 'x' + str(height)
Play_key = 0
Initial = 0
global stopped
stopped = False

# ------------------------------------Main window-------------------------------------------------
root = tk.ThemedTk()
root.get_themes()
root.set_theme('breeze')

#Geometry of the window
root.title("Music Player")
root.geometry(resolution)
root.minsize(width,height)
root.maxsize(width,height)
icon = PhotoImage(file = 'assest\icon.png')
root.iconphoto(False, icon)

#Background of the window
root.configure(bg='#FAF0DD')



#Song detail
canvas = Canvas(root, width= 1092, height= 450,bg='#FAF0DD')
canvas.pack(padx= 0, pady= 0)
default_canvas()
    
#Frame For Button
btn_frame = Frame(root)
btn_frame.pack(anchor= NW, padx=(30,0))

#Music Buttons Image
play_btn_img = PhotoImage(file = 'assest\play.png')
pause_btn_img = PhotoImage(file = 'assest\pause.png')
forward_btn_img = PhotoImage(file = 'assest/forward.png')
back_btn_img = PhotoImage(file = 'assest/back.png')
stop_btn_img = PhotoImage(file = 'assest\stop1.png')
option_btn_img = PhotoImage(file = 'assest\option.png')

#Music Buttons config
pause_btn = Button(btn_frame, image= pause_btn_img, borderwidth=0, command=play, bg='#FAF0DD', activebackground='#FAF0DD')
forward_btn = Button(btn_frame, image= forward_btn_img, borderwidth= 0, command=forward, bg='#FAF0DD', activebackground='#FAF0DD')
back_btn = Button(btn_frame, image= back_btn_img, borderwidth= 0, command=back, bg='#FAF0DD', activebackground='#FAF0DD')
stop_btn = Button(btn_frame, image= stop_btn_img, borderwidth= 0, command= stop, bg='#FAF0DD', activebackground='#FAF0DD')
option_btn = Button(btn_frame, image= option_btn_img, borderwidth= 0, command= Music_list, bg='#FAF0DD', activebackground='#FAF0DD')

pause_btn.grid(row= 0, column= 1)
forward_btn.grid(row= 0, column= 2)
back_btn.grid(row= 0, column= 0)
stop_btn.grid(row= 0, column= 3)
option_btn.grid(row= 0, column= 4)

#Frame for status thing
status_frame = Frame(root,bg='#FAF0DD')
status_frame.pack(anchor=NW, padx= 5)

#Song Position
song_position = Label(status_frame, text="00:00",anchor=W, font = ('bahnschrift 11'), pady=7,padx= 20, bg='#FAF0DD')
song_position.grid(row= 0, column= 0)

#Song Slider
song_slider = ttk.Scale(status_frame, from_= 0, to= 100, orient= HORIZONTAL, command= slide, length=300, value = 0 )
song_slider.grid(row = 0, column= 1)

#temporary label
# slider_label = Label(status_frame, text='0')
# slider_label.grid(row= 1, column= 0)

#Speaker Label
speaker_label = Label(root,bg='#FAF0DD')
speaker_label.place(x= 870, y= 489)
speaker_image = PhotoImage(file = 'assest\sound.png')
speaker = Label(speaker_label, image= speaker_image, padx= 300,bg='#FAF0DD')
speaker.pack()

slider_label = Label(root,bg='#FAF0DD')
slider_label.place(x= 900, y= 489)

volume_slider = ttk.Scale(slider_label, from_=0, to=1, orient= HORIZONTAL, value= 1, command= volume, length= 120)
volume_slider.pack()

current_volume = Label(root, text="100%",bg='#FAF0DD')
current_volume.place(x= 1030, y = 489)



root.mainloop()