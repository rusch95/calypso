# pset7.py


# sys.path.append('..')

import midi
from common.audio import *
from common.clock import *
from common.core import *
from common.gfxutil import *
from common.mixer import *
from common.synth import *
from common.wavegen import *
from common.wavesrc import *

BEAT_LEN = 160 * 6


class MidiController(object):
    def __init__(self, song_path, level_update):
        super(MidiController, self).__init__()
        self.audio = Audio(2)
        self.mixer = Mixer()

        self.synth = Synth('music/The_Nes_Soundfont.sf2')

        self.mid = midi.read_midifile(song_path)
        messages = list(self.mid.iterevents())

        self.mid_messages = [m for m in messages if m.channel == 0]
        self.platform_messages = [m for m in messages if m.channel == 1]

        # create TempoMap, AudioScheduler
        self.tempo_map = SimpleTempoMap(160)
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

        # this keeps track of the number of reverses we've done so that when we flip we don't keep playing notes from the old path.
        self.num_reverses = 0

        # this keeps track of all the notes currently playing so we can stop them if we get reset.
        self.playing_notes = set([])

        # print "SR= ",Audio.sample_rate
        # self.beat = WaveFile("music/12911_sweet_trip_mm_hat_cl.wav")


        self.current_offset = 0

        # current notes on and their velocities. Helps with reversing
        self.current_values = dict()

        self.started = False
        self.lose_tick = None

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

    def start(self, start_callback=None):
        next_beat = quantize_tick_up(self.sched.get_tick(), BEAT_LEN)
        self.current_offset = next_beat

        self.schedule_cmd = self.sched.post_at_tick(next_beat, self._midi_schedule_next_note, self.num_reverses)

        def callback(*args):
            if start_callback is not None:
                start_callback()

    def reset(self, lost=False):
        if self.schedule_cmd:
            self.sched.remove(self.schedule_cmd)

        if self.schedule_action:
            self.sched.remove(self.schedule_action)

        for channel, note in self.playing_notes:
            self.synth.noteoff(channel, note)
        self.playing_notes.clear()

        self.reversed = False
        self.current_idx = 0

        # so we don't keep playing scheduled notes
        self.num_reverses += 10

        if not lost:
            self.started = False
            self.lose_tick = None
        else:
            self.lose_tick = self.convert_tick(self.sched.get_tick())

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

        self.reverse_callback = callback

    def _reverse(self, tick, arg):
        self.reverse_pending = False

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
        # print "REVERSE", tick, self.current_offset
        self.num_reverses += 1

        # old_offset = self.current_offset
        # current_tick = tick
        # current_offsettick =
        # old_func = old_offset + time_on_note
        # new func = new_offset - time_on_note
        # old_func = new_func when current_tick = time_on_note
        # new_offset = old_offset + 2 * current_tick

        self.current_offset += 2 * (tick - self.current_offset)

        self._midi_schedule_next_note(tick, self.num_reverses)

        if self.reverse_callback is not None:
            self.reverse_callback()


    def convert_tick(self, song_tick):
        if self.reversed:
            return self.current_offset - song_tick
        else:
            return self.current_offset + song_tick

    def convert_tick_for_level(self, song_tick):
        if not self.started:
            return 0
        elif self.lose_tick is not None:
            return self.lose_tick
        elif self.reversed:
            return self.current_offset - song_tick
        else:
            return -(self.current_offset - song_tick)

    def _midi_schedule_next_note(self, tick, num_reverses):
        # to prevent multiple streams of notes from going at once
        if num_reverses != self.num_reverses:
            return

        self.started = True

        if self.reversed:
            to_schedule = self.mid_messages[self.current_idx]
            self.current_idx -= 1

        else:
            to_schedule = self.mid_messages[self.current_idx]
            self.current_idx += 1

        if to_schedule is None:
            print "end of song"
            return

        next_tick = self.convert_tick(to_schedule.tick)
        # print "NOTE",next_tick, to_schedule, self.current_idx, self.current_offset

        self.schedule_action = self.sched.post_at_tick(next_tick, self._midi_action, to_schedule)

        # schedule another call to this function at the same time.
        self.schedule_cmd = self.sched.post_at_tick(next_tick, self._midi_schedule_next_note, num_reverses)

    def _midi_action(self, tick=0.0, message=None):
        self.schedule_action = None

        if (message.type == 'NoteOnEvent' and not self.reversed) or (self.reversed and message.type == 'NoteOffEvent'):
            self.synth.noteon(message.channel, message.pitch, message.velocity)
            if not self.reversed:
                self.current_values[(message.channel, message.pitch)] = message.velocity
            # self.playing_notes.add((message.channel, message.pitch))
            print '%snote on: %d' % ((message.pitch - 20) * ' ', message.pitch)
        elif message.type == 'ControlChangeEvent':
            self.synth.cc(message.channel, message.control, message.value)
        elif (message.type == 'NoteOffEvent' and not self.reversed) or (
            self.reversed and message.type == 'NoteOnEvent'):
            self.synth.noteoff(message.channel, message.pitch)
            if not self.reversed:
                message.velocity = self.current_values[(message.channel, message.pitch)]
            try:
                self.playing_notes.remove((message.channel, message.pitch))
            except KeyError:
                pass
            print "%snote off: %d" % ((message.pitch - 20) * ' ', message.pitch)
        else:
            print message
            # TODO: figure out what to do with program changes

    # needed to update audio
    def on_update(self):
        self.audio.on_update()
        # print self.sched.get_tick(), self.current_offset, self.convert_tick_for_level(self.sched.get_tick())
        self.level_update(loc=-self.convert_tick_for_level(self.sched.get_tick()))


if __name__ == '__main__':
    run(MainWidget)
