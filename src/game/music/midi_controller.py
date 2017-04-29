#pset7.py


import sys
sys.path.append('..')
from common.core import *
from common.clock import *
from common.audio import *
from common.mixer import *
from common.wavegen import *
from common.wavesrc import *
from common.gfxutil import *
from common.synth import *

from kivy.core.image import Image
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.clock import Clock as kivyClock
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
import random
import numpy as np
import bisect
from common.kivyparticle.engine import ParticleSystem

import numpy as np

# generates audio data by asking an audio-source (ie, WaveFile) for that data.
class WaveGenerator2(object):
    def __init__(self, wave_source, loop=False):
        super(WaveGenerator2, self).__init__()
        self.source = wave_source
        self.loop = loop
        self.frame = 0
        self.paused = False
        self._release = False
        self.gain = 1.0
        self.forwards = True

    def reset(self):
        self.paused = True
        self.frame = 0

    def play_toggle(self):
        self.paused = not self.paused

    def play(self):
        self.paused = False

    def pause(self):
        self.paused = True

    def release(self):
        self._release = True
    
    def reverse(self, forwards=None):
        if forwards is not None:
            self.forwards = forwards
        else:
            self.forwards ^= 1

    def set_gain(self, g):
        self.gain = g

    def get_gain(self):
        return self.gain

    def generate(self, num_frames, num_channels) :
        if self.paused:
            output = np.zeros(num_frames * num_channels)
            return (output, True)

        else:
            # get data based on our position and requested # of frames
            if self.forwards:
                output = self.source.get_frames(self.frame, self.frame + num_frames)
            else:
                output = self.source.get_frames(max(0,self.frame - num_frames), self.frame)
                print 
            output *= self.gain

            # check for end-of-buffer condition:
            actual_num_frames = len(output) / num_channels
            continue_flag = actual_num_frames == num_frames

            # advance current-frame
            if self.forwards:
                self.frame += actual_num_frames
            else:
                self.frame -= actual_num_frames


            # looping. If we got to the end of the buffer, don't actually end.
            # Instead, read some more from the beginning
            if self.loop and not continue_flag:
                continue_flag = True
                remainder = num_frames - actual_num_frames
                if self.forwards:
                    output = np.append(output, self.source.get_frames(0, remainder))
                    self.frame = remainder
                else:
                    raise NotImplementedError

            if self._release:
                continue_flag = False

            # zero-pad if output is too short (may happen if not looping / end of buffer)
            shortfall = num_frames * num_channels - len(output)
            if shortfall > 0:
                output = np.append(output, np.zeros(shortfall))

            # return
            return (output, continue_flag)


BEAT_LEN = 1800

class MainWidget(BaseWidget) :
    def __init__(self):
        super(MainWidget, self).__init__()

        self.midi_controller = MidiController("grieg_mountain_king.mid")
        
        # and text to display our status
        self.label = topleft_label()
        self.add_widget(self.label)
        

    def on_key_down(self, keycode, modifiers):
        # play / pause toggle
        if keycode[1] == 'p':
            self.midi_controller.toggle()
        elif keycode[1] == 'r':
            self.midi_controller.reverse()
        elif keycode[1] == 's':
            self.midi_controller.start()
        elif keycode[1] == '1':
            print self.midi_controller.sched.now_str()

    def on_key_up(self, keycode):
        # button up
        pass
        
    def on_update(self) :
        self.midi_controller.on_update()
        # self.label.text = self.audio_controller.sched.now_str() + '\n'
        self.label.text = self.midi_controller.sched.now_str() + '\n'



# creates the Audio driver
# creates a song and loads it with solo and bg audio tracks
# creates snippets for audio sound fx
class AudioController(object):
    def __init__(self, song_path):
        super(AudioController, self).__init__()
        self.audio = Audio(2)
        self.mixer = Mixer()
        self.audio.set_generator(self.mixer)

        self.solo_gen = WaveGenerator2(WaveFile(song_path))
        
        self.mixer.add(self.solo_gen)
        self.mixer.set_gain(1)
        
        # self.synth = Synth('data/The_Nes_Soundfont.sf2')
        #
        # # create TempoMap, AudioScheduler
        # self.tempo_map  = SimpleTempoMap(120)
        # self.sched = AudioScheduler(self.tempo_map)
        #
        # # connect scheduler into audio system
        # self.mixer.add(self.sched)
        # self.sched.set_generator(self.synth)
        #
        #
        # self.synth.program(2, 0, 0)
        
        
        

    # start / stop the song
    def toggle(self):
        self.solo_gen.play_toggle()

    # mute / unmute the solo track
    def set_mute(self, mute):
        self.solo_gen.set_gain(0 if mute else 1)

    # reverse music
    def reverse(self):
        self.solo_gen.reverse()


    def current_time(self):
        return self.solo_gen.frame * (1./SIGNAL_RATE)

    # needed to update audio
    def on_update(self):
        self.audio.on_update()

def copy_midi_msg(old_msg, time=None, reverse_type=True, velocity=None):
    if not reverse_type:
        raise NotImplementedError
    
    new_type = old_msg.type
    # TODO: deal properly with control changes
    new_dict = dict(old_msg.dict())
    
    if time is not None:
        new_dict['time'] = time
        
    if velocity is not None:
        new_dict['velocity'] = velocity
        
    if old_msg.type=='note_on':
        new_type = 'note_off'
        new_dict['velocity'] = 0
    elif old_msg.type =='note_off':
        new_type = 'note_on'    
    new_dict['type'] = new_type
    
    
    try:
        return mido.Message(**new_dict)
    except LookupError:
        return None

def reverse_messages(msg_list):
    """Takes a list of MIDI messages and returns a list of messages that, when taken in reverse order, correspond to playing the song backwards."""
    reversed_list = list(msg_list)
    current_velocities = dict()
    for i,a in enumerate(msg_list):
        b = msg_list[i-1]
        vel = current_velocities.get(b.dict().get('note',None),None)
        reversed_list[i-1] = copy_midi_msg(b,time=a.time,reverse_type=True,velocity=vel)
        if b.type == 'note_on':
            current_velocities[b.note] = b.velocity
        
    return reversed_list


import mido

class MidiController(object):
    def __init__(self, song_path, level_update):
        super(MidiController, self).__init__()
        self.audio = Audio(2)
        self.mixer = Mixer()

        self.synth = Synth('music/The_Nes_Soundfont.sf2')
        
        self.mid = mido.MidiFile(song_path)
        self.mid_messages = list(self.mid)
        self.reversed_messages = reverse_messages(self.mid_messages)

        # create TempoMap, AudioScheduler
        self.tempo_map  = SimpleTempoMap(160)
        self.sched = AudioScheduler(self.tempo_map)

        # connect scheduler into audio system
        self.mixer.add(self.sched)
        self.sched.set_generator(self.synth)
        self.audio.set_generator(self.mixer)

        self.mixer.set_gain(1)

        # save the level
        self.level_update = level_update
        
        # current index in self.mid_messages
        self.current_idx = 0
        
        self.paused = False
        
        # amount of time that has passed in-song before next scheduled note
        self.cumulative_time = 0.
        
        # whether we're going to reverse at the end of the current measure
        self.reverse_pending = False
        
        # whether we're currently moving backwards
        self.reversed = False
        
        # thing to call when reversing
        self.reverse_callback = None
        
        self.num_reverses = 0

    def toggle(self):
        """pauses or plays the music."""
        self.paused ^= True
        if self.paused:
            pass
            # TODO: cancel all currently playing notes but save when they were
            # TODO: cancel all scheduled notes but store when they were
        else:
            pass
            # TODO: resume playing the paused notes
            # TODO: reschedule all scheduled notes
    
    def start(self):
        next_beat = quantize_tick_up(self.sched.get_tick(), BEAT_LEN)
        
        self.schedule_cmd = self.sched.post_at_tick(next_beat, self._midi_schedule_next_note,0)
        self.mark_beat_cmd = self.sched.post_at_tick(next_beat, self._mark_beat, 0)

    # reverse music
    def reverse(self, callback=None):
        """Reverses the music at the next barline. callback will be called when that happens."""
        self.reverse_pending ^= True
        if not self.reverse_pending:
            # cancel the pending reverse
            self.sched.remove(self.reverse_cmd)
            
            # we just cancelled a pending reverse
            return
        
        next_beat = quantize_tick_up(self.sched.get_tick(), BEAT_LEN)
        self.reverse_cmd = self.sched.post_at_tick(next_beat, self._reverse)
        
        
    
    def _mark_beat(self, tick, arg):
        print "---------------------------------------"
        next_beat = quantize_tick_up(self.sched.get_tick()+1, BEAT_LEN)
        self.mark_beat_cmd = self.sched.post_at_tick(next_beat, self._mark_beat, 0)
        
    def _reverse(self, tick, arg):
        self.reverse_pending = False
        if self.reverse_callback is not None:
            self.reverse_callback()
        
        self.reversed ^= True

        # cancel all calls to _midi_schedule_next_note
        if self.schedule_cmd:
            self.sched.remove(self.schedule_cmd)
        
        if self.schedule_action:
            self.sched.remove(self.schedule_action)
        
        # start with the same index as we last executed.
        if self.reversed:
            self.current_idx -= 1
        else:
            self.current_idx += 1

        # call the first action in the opposite direction
        print "REVERSE"
        self.num_reverses += 1
        self._midi_schedule_next_note(tick, self.num_reverses)
        
    def _midi_schedule_next_note(self, tick, num_reverses):
        # to prevent multiple streams of notes from going at once
        if num_reverses != self.num_reverses:
            return
            
        if self.reversed:
            to_schedule = self.reversed_messages[self.current_idx]
            self.current_idx -= 1
            
        else:
            to_schedule = self.mid_messages[self.current_idx]
            self.current_idx += 1
        
        if to_schedule is None:
            print "end of song"
            return
        next_tick = self.sched.get_tick() + to_schedule.time*800
        self.schedule_action = self.sched.post_at_tick(next_tick, self._midi_action, to_schedule)
        
        # schedule another call to this function at the same time.
        self.schedule_cmd = self.sched.post_at_tick(next_tick, self._midi_schedule_next_note, num_reverses)
    
    def _midi_action(self,tick=0.0, message=None):
        self.schedule_action = None
        
        if message.is_meta:
            return
        
        if message.type == 'note_on':
            self.synth.noteon(message.channel, message.note, message.velocity)
            print '%snote on: %d' % ((message.note-20)*' ',message.note)
        elif message.type == 'control_change':
            self.synth.cc(message.channel, message.control, message.value)
        elif message.type == 'note_off':
            self.synth.noteoff(message.channel, message.note)
            print "%snote off: %d" % ((message.note-20)*' ',message.note)
        elif message.type == 'program_change':
            print message
            # TODO: figure out what to do with program changes
        
        
        
    # needed to update audio
    def on_update(self):
        self.audio.on_update()
        self.level_update(.5)



if __name__ == '__main__':
    run(MainWidget)


