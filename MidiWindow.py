from Tkinter import *
from pyknon.music import Note, Rest, NoteSeq
from pyknon.genmidi import Midi
from UniversalCA import UniversalCA, ElementaryCA, ElementaryCARules
from RuleDisplay import RuleDisplay, ElementaryCARuleDisplay


TIME = 0.25/4 #quarter
NAME = "new_miditest1.mid"
SCALES = ['chromatic', 'pentatonic minor', 'pelong', 'custom']
MAPPINGS = [[0,1,2,3,4,5,6,7,8,9,10,11], [0,3,5,7,10], [0,1,3,7,8]]
class MidiWindow(object):
    """superclass for the subsection  of the Universe that gets rendered as Midifile
    multistate CA will have their mapping attribute will be an array of multi-demensional arrays"""
    def __init__(self, gui, size_arg, starting_point = None):
        self._gui = gui
        self._gui_width = gui._width
        if size_arg > self._gui_width:
            size_arg = self._gui_width
        self._size = size_arg
        @property
        def size(self):
            return self._size
        if starting_point == None:
            starting_point = (int(self._gui_width/2) - int(self._size/2))
        self._starting_point = starting_point
        self.change_starting_point(self._starting_point)
        self._allow_held_notes = False
        self._note_array = []
        self._full_mapping = []
        self._root = 0
        self._current_scale = 0
#          self._mapping = None
        self._useScale = True
        
        self.make_note_array()
    
    def get_size(self):
        return self._size
    def get_starting_point(self):
        return self._starting_point
    def change_size(self, value = None):
        """changes the size or resizes to fit universe, this should be called whenever width changes""" 
        if value == None:  #if no arg, then make the size the current size
            value = self._size
        if value > self._gui_width:
            value = self._gui_width
        self._size = value
        self._gui.change_size_callback()
        print("in change size, callback called")
        
        return value
    
    def change_starting_point(self, value = None):
        if value == None:
            value = self._starting_point
        if value + self._size > self._gui_width:
            value = self._gui_width - self._size
        self._starting_point = value
        return value
    
    def make_note_array(self):
        self._note_array = []
        start = self._starting_point
        end = self._starting_point + self._size
        for line in range(self._gui._length):
            self._note_array.append(self._gui._CA._universe[line][start:end])
           
    
    def display(self):
        for line in self._note_array:
            print(line)
            print('\n')   

class TwoStateMidiWindow(MidiWindow):
    """sublass where the input values are simple on/off, so one mapping per cell"""
    def __init__(self, gui, size_arg,  starting_point = 0, midi_mapping = None ):
        print("in Twostate constructor;" )
        super(TwoStateMidiWindow, self).__init__(gui, size_arg, starting_point)
        self._mapping = midi_mapping
        print("in Twostate constructor;", self._mapping)
        self._full_mapping = []
        self._custom_mapping = midi_mapping
        self._useScale = False
        
    
    def set_full_mapping(self, old_mapping):
        self._full_mapping = old_mapping
        
    def use_scale(self, mapping = None):
        """takes an int corresponding to scale constant, automatically switches to useScale"""
        if mapping != None:  #if we have a non default arg
            self._current_scale = mapping
            self._useScale = True
        else:  #no arg
            if self._current_scale != None:
                print("current scale is not none")
                mapping = self._current_scale
            else:
                print('current scale was none, mapping is 0')
                mapping = 0
        
              
        self._useScale = True
        self._mapping = MAPPINGS[mapping]
        print("in midi window, current scale is set to", self._current_scale)
    
       
    def full_mapping_assignment(self, root = None):
        if root == None:
            root = self._root
        if self._useScale:
            scale_size = len(self._mapping)
            
            self._full_mapping = [root + (self._mapping[i % scale_size] + 12 * (i / scale_size))  for i in range(self._size)]
            print(self._full_mapping)
    def do_custom_mapping(self, custom_scale = None, root = None):
        """if there is an arg, use it. if no arg, then use previos value (self._custom_mapping)"""
        if root == None:
            root = self._root
        self._useScale = False
        if custom_scale == None:
            custom_scale = self._custom_mapping
        else:
            self._custom_mapping = custom_scale
        scale_size = len(self._custom_mapping)
        self._full_mapping = [root + (self._custom_mapping[i % scale_size] + 12 * (i / scale_size))  for i in range(self._size)]
#         self._full_mapping = custom_scale
        
    def do_mapping(self):
        """if use scale is set, call full mapping, if not do_custom mapping with previously set custom scale"""
        if self._useScale:
            print("in do _mapping, used SCALE")
            self.full_mapping_assignment()
        else:
            print("in do_mapping, used CUSTOM")
            self.do_custom_mapping()
    
    def build_note_seqs(self):
        length = self._gui._CA._length
        vertical = zip(*self._note_array)
        print(vertical)
        print("size of vertical {}".format(len(vertical)))
        print("size of self._note_array[0] {}".format(len(self._note_array[0])))
        self._noteSeq_array = []
        for line in range(self._size):
            pitch = self._full_mapping[line]
            print(pitch)
            ns = NoteSeq()
            duration = 0     
            print(vertical[line]) 
            for i in range(length):
                if vertical[line][i] == 1:
                    duration += TIME
                else:
                    if duration > 0:
                        ns.append(Note(pitch, dur = duration)) 
                        print("added note of {} at {}".format(duration, i))
                        duration = 0
                    ns.append(Rest(dur = TIME))
                   
                if i == (length-1) and duration > 0:
                    ns.append(Note(pitch, dur = duration))
                    print("added final note of {} at {}".format(duration, i))
                    
                    
                    
            
            self._noteSeq_array.append(ns)
        midi1 = Midi(1)
        for line in self._noteSeq_array:
            midi1.seq_notes(line)
        
        midi1.write(NAME)
         
                    
            
    
        
if __name__ == "__main__":
    root = Tk()
    r = ElementaryCARules(109)
    ca = ElementaryCA(width = 51, length = 50, rules = r, first_line = 0)   
  
