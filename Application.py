import configparser
import pandas as pd
import tkinter as tk
import tkinter.messagebox
from tkinter.constants import NSEW, END, EXTENDED, SINGLE, ANCHOR
from PIL import ImageTk, Image
from Mode import *

# Pomocnicze constany do otrzymania modes dla piano
NUM_OF_BASS = 0
NUM_OF_FLUTE = 1
NUM_OF_LPIANO = 2
NUM_OF_PIANO = 3
NUM_OF_TRUMPET = 4
NUM_OF_VIOLIN = 5

# Plik z konfiguracjej
FILE_CONFIG = 'config.txt'


# Metoda zwracająca listę mode dla piano
def get_modes():
    modes = []
    modes.append(Mode('modes/bassacoustic', 700, 1000))
    modes.append(Mode('modes/flute', 1000, 1000))
    modes.append(Mode('modes/lightpiano', 1000, 2000))
    modes.append(Mode('modes/piano', 500, 1500))
    modes.append(Mode('modes/trumpet', 500, 1000))
    modes.append(Mode('modes/violin', 700, 1000))
    return modes


class Application(tk.Frame):
    modes = get_modes()

    # Konstruktor główny
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.parent = master
        self.parent.title('Synthesizer')

        # Configparser
        self.konfig = configparser.ConfigParser()
        self.konfig.read(FILE_CONFIG, "UTF8")
        default = self.konfig["DEFAULT"]
        self.geometry = default.get('geometry', "500x500+100+100")

        # Dataset with songs
        self.df = pd.read_csv('songs.csv', sep=',')

        # Domyślny mode na piano to Light Piano
        self.actual_mode = Application.modes[NUM_OF_LPIANO]

        self.create_start_page()

    def app_quit(self, event=None):
        # Wywołanie messagebox'a
        reply = tk.messagebox.askyesno(
            "Exit",
            "Are you sure?",
            parent=self.parent
        )
        if reply:
            # Zapisywanie geometrji okna
            geometria = self.parent.winfo_geometry()
            self.konfig["DEFAULT"]["geometry"] = geometria
            with open(FILE_CONFIG, 'w') as config_file:
                self.konfig.write(config_file)
            # Zamknięcie programu
            self.parent.destroy()

    # Metoda napeniająca okno główne
    def create_start_page(self):
        self.parent.protocol("WM_DELETE_WINDOW", self.app_quit)
        self.create_start_page_menu()
        self.create_start_page_work_space()

    # Metoda tworząca menubar w oknie głównym
    def create_start_page_menu(self):
        self.menubar = tk.Menu(self.parent)
        self.parent["menu"] = self.menubar
        program_menu = tk.Menu(self.menubar)
        for label, command, shorcut_text, shortcut in (
                ("Start Play", self.create_piano_page, "Ctrl+Q", "<Control-q>"),
                ("Exit", self.app_quit, "Ctrl+E", "<Control-e>"),
        ):
            program_menu.add_command(
                label=label,
                underline=0,
                command=command,
                accelerator=shorcut_text
            )
            self.parent.bind(shortcut, command)
        self.menubar.add_cascade(label="Program", menu=program_menu, underline=0)

        help_menu = tk.Menu(self.menubar)
        for label, command, shortcut_text, shortcut in (
                ("Info", self.create_info_page, "Ctrl+I", "<Control-i>"),
        ):
            help_menu.add_command(
                label=label,
                underline=0,
                command=command,
                accelerator=shortcut_text
            )
            self.parent.bind(shortcut, command)
        self.menubar.add_cascade(label="Help", menu=help_menu, underline=0)

    # Metoda napełniająca przestrzeń okna główengo
    def create_start_page_work_space(self):
        # Główny Frame
        self.start_frame = tk.Frame(self.parent, bg='linen', width=500, height=500)
        # Rozmieszczenie Frame'u głównego
        self.start_frame.grid(
            row=1,
            column=0,
            columnspan=1,
            rowspan=1,
            sticky=NSEW
        )
        # Tworzenia Button dla startu pracy
        button_start = tk.Button(
            self.start_frame,
            text=u'! PLAY !',
            width=20,
            height=5,
            bg='sky blue',
            command=self.create_piano_page
        )
        # Tworzenia Button dla wyświetlania okna z dodatkową informacją
        # button_info = tk.Button(
        #     self.start_frame,
        #     text=u'! INFO !',
        #     width=20,
        #     height=5,
        #     bg='sky blue',
        #     command=self.create_info_page
        # )
        # Tworzenie Button dla zamknięcia programu
        button_exit = tk.Button(
            self.start_frame,
            text=u'! EXIT !',
            width=20,
            height=5,
            bg='light coral',
            command=self.app_quit
        )
        # Tworzenie Label i wstawianie w niego obrazka applikacji
        img = ImageTk.PhotoImage(Image.open('mainlogo.jpg'))
        label_image = tk.Label(self.start_frame, image=img)
        label_image.image = img
        # Rozmieszczenie elemntów Frame'a
        label_image.place(x=100, y=10)
        button_exit.place(x=175, y=400)
        #button_info.place(x=175, y=300)
        button_start.place(x=175, y=200)

    # Metoda tworząca okno informacyjne
    def create_info_page(self, event=None):
        info_page = tk.Toplevel(self.parent)
        info_frame = tk.Frame(info_page, bg='linen', width=500, height=500)
        info_page.title('Info Page')
        info_frame.grid(
            row=1,
            column=0,
            columnspan=1,
            rowspan=1,
            sticky=NSEW
        )
        label_title_info = tk.Label(info_frame, bg='linen', text='Info o Aplikacji Synthesizer',font=('Arial', 12))
        label_info = tk.Label(info_frame, bg='linen', text='Aplikacja jest symulatorzem syntezatora', font=('Arial', 10))
        label_info_modes_and_songs = tk.Label(info_frame, bg='linen', font=('Arial',10),
                                              text='Na ten moment w aplikacji są 6 rodzajów dzwięków:\n'
                                                   '1) Bass Guitar\n'
                                                   '2) Flute\n'
                                                   '3) Light Piano\n'
                                                   '4) Piano\n'
                                                   '5) Trumpet\n'
                                                   '6) Violin\n'
                                                   'Na ten moment w aplikacji są 7 piosenek\n'
                                                   '1) In the End\n'
                                                   '2) Twinkle Twinkle Little Star\n'
                                                   '3) Sadness and Sorrow\n'
                                                   '4) Fly me to the moon\n'
                                                   '5) What a wonderful world\n'
                                                   '6) Happy Birthday\n'
                                                   '7) All Star'
                                              )
        label_n_surn = tk.Label(info_frame, bg='linen', text='Anton Saroka', font=('Arial',10))
        label_title_info.place(x=170, y= 10)
        label_info.place(x=150, y=30)
        label_info_modes_and_songs.place(x=100, y=50)
        label_n_surn.place(x=220,y=450)



    # Metoda tworząca okno z Piano
    def create_piano_page(self, event=None):
        # Tworzenie okna dodatkowego
        self.piano_window = tk.Toplevel(self.parent)
        # Nadanie tytuła oknu
        self.piano_window.title('Synthesizer Play')
        # Configparser
        self.konfig_piano = configparser.ConfigParser()
        self.konfig_piano.read(FILE_CONFIG, "UTF8")
        defult = self.konfig["DEFAULT"]
        self.geometry_piano = defult.get('geometry_piano', "500x500+50+50")
        self.piano_window.geometry(self.geometry_piano)

        self.piano_window.protocol("WM_DELETE_WINDOW", self.piano_page_quit)
        # Tworzenie i napełnienie głównej przestzreni
        self.create_piano_page_work_space()

    # Metoda wyjścia z Piano Page
    def piano_page_quit(self, event=None):
        # Wywołanie messagebox'a
        reply = tk.messagebox.askyesno(
            "Exit Piano Page",
            "Are you sure?",
            parent=self.parent
        )
        if reply:
            # Zapisywanie danych do Configparser
            geometria = self.piano_window.winfo_geometry()
            self.konfig["DEFAULT"]["geometry_piano"] = geometria
            with open(FILE_CONFIG, 'w') as config_file:
                self.konfig.write(config_file)
            # Zamknięcie okna piano
            self.piano_window.destroy()

    # Metoda tworząca główny Frame na Piano window
    def create_piano_page_work_space(self):
        # Tworzenie Frame
        self.piano_frame = tk.Frame(self.piano_window, bg='linen', width=1170, height=700)
        # Rozmieszczenie Frame
        self.piano_frame.grid(
            row=1,
            column=0,
            columnspan=1,
            rowspan=1,
            sticky=NSEW
        )
        # Tworzenie i rozmieszczenie Label dla nut piosenek
        label_for_notes = tk.Label()
        label_for_notes.place(x=400, y=10)
        # Wywołanie metod
        self.create_notes()
        self.create_frame_list()

    # Metoda tworząca i napełniająca frame z listboxami
    def create_frame_list(self):
        # Tworzenie i rozmieszczenie Frame
        self.list_frame = tk.Frame(self.piano_frame, bg='mint cream', width=150, height=615)
        self.list_frame.place(x=1010, y=10)
        # Tworzenie dodatkowych zmiennych
        self.song_notes_string = ""
        self.song_notes_list = []
        # Tworzenie listboxa z piosenkami
        self.list_songs = tk.Listbox(self.list_frame)
        for song in self.df['title']:
            self.list_songs.insert(END, song)
        # Tworzenie listboxa z modes
        self.list_modes = tk.Listbox(self.list_frame)
        self.list_modes.insert(END, 'Bass')
        self.list_modes.insert(END, 'Flute')
        self.list_modes.insert(END, 'Light Piano')
        self.list_modes.insert(END, 'Piano')
        self.list_modes.insert(END, 'Trumpet')
        self.list_modes.insert(END, 'Violin')
        # Tworzenie i rozmieszczenie Button dla wybierania piosenek
        button_songs = tk.Button(self.list_frame, text="Choose", command=self.choose_song)
        button_songs.place(x=40, y=185)
        # Tworzenie i rozmieszczenie Button dla wybierania mode
        button_modes = tk.Button(self.list_frame, text="Choose", command=self.choose_mode)
        button_modes.place(x=40, y=580)
        # Tworzenie Labla wyświetlającego aktualny mode
        self.label_mode = tk.Label(self.list_frame, text='', bg='mint cream')
        self.label_mode.config(text='Actual mode : ' + 'Light Piano')
        # Rozmieszczenie pozostałych elementów
        self.label_mode.place(x=5, y=380)
        self.list_modes.place(x=5, y=400)
        self.list_songs.place(x=5, y=10)
        # Wywołanie metody
        self.create_tutorial()

    # Metoda tworząca Frame dla nut
    def create_tutorial(self):
        # Tworzenie i rozmieszczenie Frame
        self.tutorial_frame = tk.Frame(self.piano_frame, bg='linen', width=900, height=175)
        self.tutorial_frame.place(x=50, y=10)
        # Tworzenie Lablów dla wyświetlania Tytułu piosenki i jej nut
        self.label_tutorial = tk.Label(self.tutorial_frame, bg='linen', text='', font=('Arrial', 20))
        self.label_title = tk.Label(self.tutorial_frame, bg='linen', text='', font=('Arrial', 20))
        self.label_tutorial.config(text='')
        # Rozmiesczenie elemtów
        self.label_title.place(x=400, y=5)
        self.label_tutorial.place(x=10, y=75)

    # Metoda wybierająca piosenkę
    def choose_song(self, event=None):
        # Aktualizacja labla z tytułem
        self.label_title.config(text='Song: ' + self.list_songs.get(ANCHOR))
        # Tworzenie listy z nutami piosenki
        self.song_notes_list = self.df['notes'][self.list_songs.index(ANCHOR)].split()
        # Tworzenie stringa do wyświetlania nut
        self.song_notes_string = ""
        for i in range(8):
            if len(self.song_notes_list) < 7:
                self.song_notes_string = ""
                for y in self.song_notes_list:
                    self.song_notes_string = self.song_notes_string + y + "   "
                    break
            else:
                self.song_notes_string = self.song_notes_string + self.song_notes_list[i] + "   "
        # Aktualizacja labla z nutami
        self.label_tutorial.config(text='Notes: ' + self.song_notes_string)
        # Fokus na frame z przyciskami (żeby była możliwość grać z klawiatury)
        self.notes_frame.focus_set()

    # Metoda wybierająca mode piano
    def choose_mode(self, event=None):
        # Aktualizacja lable z modem
        self.label_mode.config(text='Actual mode : ' + self.list_modes.get(ANCHOR))
        # Zmiana mode
        self.actual_mode = self.modes[self.list_modes.index(ANCHOR)]
        # Fokus na frame z przyciskami (żeby była możliwość grać z klawiatury)
        self.notes_frame.focus_set()

    # Tworzenie przycisków z nutami
    def create_notes(self):
        # Tworzenie Frame
        self.notes_frame = tk.Frame(self.piano_frame, bg='linen')
        # Tworzenie, rozmieszczenie nut oraz nadowanie nutam klawisz z klawiatury
        c0 = tk.Button(self.notes_frame, bg='white', text='C_0\n\nZ', command=self.c0_play, height=15, width=8)
        c0.grid(row=5, column=0)
        self.notes_frame.focus_set()
        self.notes_frame.bind('<z>', self.c0_play)
        self.piano_frame.bind('<Return>', lambda event: print('yeseys'))
        cd0 = tk.Button(self.notes_frame, bg='black', fg='white', text='C#_0\n\nS', command=self.cd0_play, height=12, width=8)
        cd0.grid(row=1, columnspan=2)
        self.notes_frame.bind('<s>', self.cd0_play)
        d0 = tk.Button(self.notes_frame, bg='white', text='D_0\n\nX', command=self.d0_play, height=15, width=8)
        d0.grid(row=5, column=1)
        self.notes_frame.bind('<x>', self.d0_play)
        dd0 = tk.Button(self.notes_frame, bg='black', fg='white', text='D#_0\n\nD', command=self.dd0_play, height=12, width=8)
        dd0.grid(row=1, columnspan=4)
        self.notes_frame.bind('<d>', self.dd0_play)
        e0 = tk.Button(self.notes_frame, bg='white', text='E_0\n\nC', command=self.e0_play, height=15, width=8)
        e0.grid(row=5, column=2)
        self.notes_frame.bind('<c>', self.e0_play)
        f0 = tk.Button(self.notes_frame, bg='white', text='F_0\n\nV', command=self.f0_play, height=15, width=8)
        f0.grid(row=5, column=3)
        self.notes_frame.bind('<v>', self.f0_play)
        fd0 = tk.Button(self.notes_frame, bg='black', fg='white', text='F#_0\n\nG', command=self.fd0_play, height=12, width=8)
        fd0.grid(row=1, column=3, columnspan=2)
        self.notes_frame.bind('<g>', self.fd0_play)
        g0 = tk.Button(self.notes_frame, bg='white', text='G_0\n\nB', command=self.g0_play, height=15, width=8)
        g0.grid(row=5, column=4)
        self.notes_frame.bind('<b>', self.g0_play)
        gd0 = tk.Button(self.notes_frame, bg='black', fg='white', text='G#_0\n\nH', command=self.gd0_play, height=12, width=8)
        gd0.grid(row=1, column=4, columnspan=2)
        self.notes_frame.bind('<h>', self.gd0_play)
        a0 = tk.Button(self.notes_frame, bg='white', text='A_0\n\nN', command=self.a0_play, height=15, width=8)
        a0.grid(row=5, column=5)
        self.notes_frame.bind('<n>', self.a0_play)
        b0 = tk.Button(self.notes_frame, bg='black', fg='white', text='B_0\n\nJ', command=self.b0_play, height=12, width=8)
        b0.grid(row=1, column=5, columnspan=2)
        self.notes_frame.bind('<j>', self.b0_play)
        h0 = tk.Button(self.notes_frame, bg='white', text='H_0\n\nM', command=self.h0_play, height=15, width=8)
        h0.grid(row=5, column=6)
        self.notes_frame.bind('<m>', self.h0_play)
        c1 = tk.Button(self.notes_frame, bg='white', text='C_1\n\nQ', command=self.c1_play, height=15, width=8)
        c1.grid(row=5, column=7)
        self.notes_frame.bind('<q>', self.c1_play)
        cd1 = tk.Button(self.notes_frame, bg='black', fg='white', text='C#_1\n\n2', command=self.cd1_play, height=12, width=8)
        cd1.grid(row=1, column=7, columnspan=2)
        self.notes_frame.bind("2", self.cd1_play)
        d1 = tk.Button(self.notes_frame, bg='white', text='D_1\n\nW', command=self.d1_play, height=15, width=8)
        d1.grid(row=5, column=8)
        self.notes_frame.bind('<w>', self.d1_play)
        dd1 = tk.Button(self.notes_frame, bg='black', fg='white', text='D#_1\n\n3', command=self.dd1_play, height=12, width=8)
        dd1.grid(row=1, column=8, columnspan=2)
        self.notes_frame.bind("3", self.dd1_play)
        e1 = tk.Button(self.notes_frame, bg='white', text='E_1\n\nE', command=self.e1_play, height=15, width=8)
        e1.grid(row=5, column=9)
        self.notes_frame.bind('<e>', self.e1_play)
        f1 = tk.Button(self.notes_frame, bg='white', text='F_1\n\nR', command=self.f1_play, height=15, width=8)
        f1.grid(row=5, column=10)
        self.notes_frame.bind('<r>', self.f1_play)
        fd1 = tk.Button(self.notes_frame, bg='black', fg='white', text='F#_1\n\n5', command=self.fd1_play, height=12, width=8)
        fd1.grid(row=1, column=10, columnspan=2)
        self.notes_frame.bind("5", self.fd1_play)
        g1 = tk.Button(self.notes_frame, bg='white', text='G_1\n\nT', command=self.g1_play, height=15, width=8)
        g1.grid(row=5, column=11)
        self.notes_frame.bind('<t>', self.g1_play)
        gd1 = tk.Button(self.notes_frame, bg='black', fg='white', text='G#_1\n\n6', command=self.gd1_play, height=12, width=8)
        gd1.grid(row=1, column=11, columnspan=2)
        self.notes_frame.bind("6", self.gd1_play)
        a1 = tk.Button(self.notes_frame, bg='white', text='A_1\n\nY', command=self.a1_play, height=15, width=8)
        a1.grid(row=5, column=12)
        self.notes_frame.bind('<y>', self.a1_play)
        b1 = tk.Button(self.notes_frame, bg='black', fg='white', text='B_1\n\n7', command=self.b1_play, height=12, width=8)
        b1.grid(row=1, column=12, columnspan=2)
        self.notes_frame.bind("7", self.b1_play)
        h1 = tk.Button(self.notes_frame, bg='white', text='H_0\n\nU', command=self.h1_play, height=15, width=8)
        h1.grid(row=5, column=13)
        self.notes_frame.bind('<u>', self.h1_play)
        c2 = tk.Button(self.notes_frame, bg='white', text='C_2\n\nI', command=self.c2_play, height=15, width=8)
        c2.grid(row=5, column=14)
        self.notes_frame.bind('<i>', self.c2_play)
        # Rozmieszczenie Framu głównego
        self.notes_frame.place(x=10, y=200)

    # Metoda aktualizująca listę nut
    def change_notes(self):
        self.song_notes_string = ""
        if len(self.song_notes_list) <= 7:
            for y in self.song_notes_list:
                 self.song_notes_string = self.song_notes_string + y + "   "
        else:
            for i in range(8):
                self.song_notes_string = self.song_notes_string + self.song_notes_list[i] + "   "
        self.label_tutorial.config(text='Notes: ' + self.song_notes_string)

    # Metody do dzwięków

    def c0_play(self, event=None):
        self.actual_mode.play_note('c0')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "C_0":
                self.song_notes_list.remove("C_0")
                self.change_notes()


    def cd0_play(self, event=None):
        self.actual_mode.play_note('cd0')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "C#_0":
                self.song_notes_list.remove("C#_0")
                self.change_notes()

    def d0_play(self, event=None):
        self.actual_mode.play_note('d0')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "D_0":
                self.song_notes_list.remove("D_0")
                self.change_notes()

    def dd0_play(self, event=None):
        self.actual_mode.play_note('dd0')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "D#_0":
                self.song_notes_list.remove("D#_0")
                self.change_notes()

    def e0_play(self, event=None):
        self.actual_mode.play_note('e0')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "E_0":
                self.song_notes_list.remove("E_0")
                self.change_notes()

    def f0_play(self, event=None):
        self.actual_mode.play_note('f0')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "F_0":
                self.song_notes_list.remove("F_0")
                self.change_notes()

    def fd0_play(self, event=None):
        self.actual_mode.play_note('fd0')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "F#_0":
                self.song_notes_list.remove("F#_0")
                self.change_notes()

    def g0_play(self, event=None):
        self.actual_mode.play_note('g0')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "G_0":
                self.song_notes_list.remove("G_0")
                self.change_notes()

    def gd0_play(self, event=None):
        self.actual_mode.play_note('gd0')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "G#_0":
                self.song_notes_list.remove("G#_0")
                self.change_notes()

    def a0_play(self, event=None):
        self.actual_mode.play_note('a0')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "A_0":
                self.song_notes_list.remove("A_0")
                self.change_notes()

    def b0_play(self, event=None):
        self.actual_mode.play_note('b0')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "B_0":
                self.song_notes_list.remove("B_0")
                self.change_notes()

    def h0_play(self, event=None):
        self.actual_mode.play_note('h0')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "H_0":
                self.song_notes_list.remove("H_0")
                self.change_notes()

    def c1_play(self, event=None):
        self.actual_mode.play_note('c1')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "C_1":
                self.song_notes_list.remove("C_1")
                self.change_notes()

    def cd1_play(self, event=None):
        self.actual_mode.play_note('cd1')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "C#_1":
                self.song_notes_list.remove("C#_1")
                self.change_notes()

    def d1_play(self, event=None):
        self.actual_mode.play_note('d1')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "D_1":
                self.song_notes_list.remove("D_1")
                self.change_notes()

    def dd1_play(self, event=None):
        self.actual_mode.play_note('dd1')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "D#_1":
                self.song_notes_list.remove("D#_1")
                self.change_notes()

    def e1_play(self, event=None):
        self.actual_mode.play_note('e1')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "E_1":
                self.song_notes_list.remove("E_1")
                self.change_notes()

    def f1_play(self, event=None):
        self.actual_mode.play_note('f1')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "F_1":
                self.song_notes_list.remove("F_1")
                self.change_notes()

    def fd1_play(self, event=None):
        self.actual_mode.play_note('fd1')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "F#_1":
                self.song_notes_list.remove("F#_1")
                self.change_notes()

    def g1_play(self, event=None):
        self.actual_mode.play_note('g1')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "G_1":
                self.song_notes_list.remove("G_1")
                self.change_notes()

    def gd1_play(self, event=None):
        self.actual_mode.play_note('gd1')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "G#_1":
                self.song_notes_list.remove("G#_1")
                self.change_notes()

    def a1_play(self, event=None):
        self.actual_mode.play_note('a1')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "A_1":
                self.song_notes_list.remove("A_1")
                self.change_notes()

    def b1_play(self, event=None):
        self.actual_mode.play_note('b1')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "B_1":
                self.song_notes_list.remove("B_1")
                self.change_notes()

    def h1_play(self, event=None):
        self.actual_mode.play_note('h1')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "H_1":
                self.song_notes_list.remove("H_1")
                self.change_notes()

    def c2_play(self, event=None):
        self.actual_mode.play_note('c2')
        if len(self.song_notes_string) != 0:
            if self.song_notes_list[0] == "C_2":
                self.song_notes_list.remove("C_2")
                self.change_notes()


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
