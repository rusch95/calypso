import sys

sys.path.append('..')
from common.core import *
from common.audio import *
from common.mixer import *
from common.wavegen import *
from common.wavesrc import *
from common.gfxutil import *
from common.gfxutil import *


# creates the Audio driver
# creates a song and loads it with solo and bg audio tracks
# creates snippets for audio sound fx
class AudioController(object):
    def __init__(self, song_path):
        super(AudioController, self).__init__()
        self.audio = Audio(2)
        self.mixer = Mixer()
        self.audio.set_generator(self.mixer)

        self.song = WaveGenerator(WaveFile(song_path))
        self.mixer.add(self.song)
        self.song.play()

    # start / stop the song
    def toggle(self):
        self.song.play_toggle()

    def stop(self):
        self.song.set_gain(0)

    def restart(self):
        self.song.restart()
        self.song.set_gain(1)

    # needed to update audio
    def on_update(self):
        self.audio.on_update()
