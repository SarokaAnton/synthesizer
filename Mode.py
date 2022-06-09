import pygame


class Mode:

    def __init__(self, path, min, max):
        self.path = path
        self.min = min
        self.max = max
        self.note_time = self.min
        pygame.init()

    def reverb_on(self):
        self.note_time = self.max

    def reverb_off(self):
        self.note_time = self.min

    def play_note(self, note):
        all_path = self.path + "/" + note + ".wav"
        note = pygame.mixer.Sound(all_path)
        note.play(maxtime=self.note_time)
        print(all_path)