from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import pickle
from UniversalCA import UniversalCA, ElementaryCA, ElementaryCARules
from Dialog import Dialog, select_first_line_dialog, change_size, set_mw_details_dialog, set_midi_mapping_dialog, Schedule_dialog
from RuleDisplay import RuleDisplay, ElementaryCARuleDisplay
from MidiWindow import TwoStateMidiWindow, MidiWindow, SCALES
from Schedule import Schedule
SIZE = 12
COLORS = ["black", "blue"]
MIDI_COLORS = ['gray', 'cyan']
COLORSETS = [COLORS, MIDI_COLORS]
class GUI(object):
    """gui for graphically representing a range of CA"""
    CA_TYPES = {"<class 'UniversalCA.ElementaryCARules'>":"Elementary CA"}
    def __init__(self, master, CA):
        self._frame = Frame(master)
        self._master = master
        self._master.title("Cellular Automata")
        self._CA = CA
        
        self._display_midi_window = True
        self.first_time_build()
        self._midi_map_dialog = None
    
    def first_time_build(self):    
        self._CA.build()
        self._frame.destroy()
        self.make_screen()
        self.make_menu()
        """make_midi_window + use_sacle"""
        if str(type(self._CA._rules)) == "<class 'UniversalCA.ElementaryCARules'>":
               self._midi_window = TwoStateMidiWindow(self, 19, 1)
        self._midi_window.make_note_array()
        self._midi_window.use_scale(0)
        self._midi_window.do_mapping()
#        self._midi_window.use_scale(0)
#         self._midi_window.full_mapping_assignment(0)
        self.draw_CA()
        
    def rebuild(self):
        """keep the first line, but rebuild the rest, obviously impossible if width changes"""
        self._CA.build_from_root()
        self._frame.destroy()
        self.make_screen()
        self.make_menu()
        self.make_midi_window()
        self.draw_CA()
    def full_build(self):
        """build again from scratch"""
        self._CA.build()
        self._frame.destroy()
        self.make_screen()
        self.make_menu()
        self.make_midi_window()
        self.draw_CA()
        
    def make_menu(self):
        menubar = Menu(self._master)
        def toriaezu():
            pass
        """file"""
        fileToDo = [self._CA._schedule, self._CA._rules]
        
        
        
        def onLoadFile():
            self.open_file_opt = o_options = {}
            o_options['defaultextension'] = '.ca'
            o_options['filetypes'] = [('all files', '.*'), ('Cellular Automata Files', '.ca')]
    #        options['filetypes'] = [('Cellular Automata Files', '.ca')]
    #         options['initialdir'] = 'C:\\'
    #        options['initialfile'] = 'customCA.ca'
            o_options['parent'] = root
            o_options['title'] = 'Open File'
            openfile = tkFileDialog.askopenfile(mode='rb', **self.open_file_opt)
            """for now, just test schedule"""
            for item in fileToDo:
                self._CA._schedule = pickle.load(openfile)
                self._CA._rules = pickle.load(openfile)
            self.rebuild()
        
            
        def onSaveFile():
            self.save_file_opt = s_options = {}
            s_options['defaultextension'] = '.ca'
            s_options['filetypes'] = [('all files', '.*'), ('Cellular Automata Files', '.ca')]

#         options['initialdir'] = 'C:\\'
            s_options['initialfile'] = 'customCA.ca'
            s_options['parent'] = root
            s_options['title'] = 'Save File'
            savefile = tkFileDialog.asksaveasfile(mode='wb', **self.save_file_opt)
            
        
            for item in fileToDo:
                pickle.dump(item, savefile)
            savefile.close()
        def temp_make_file():
            
#             self._midi_window.full_mapping_assignment(0)
            self._midi_window.build_note_seqs()
        """details"""
        def change_rule():
            ElementaryCARuleDisplay(self)
        def initial_condition():
            select_first_line_dialog(self._master, self, title = "set initial condition" )
            self.full_build()
        def size():
            change_size(self._master, self, title = "change size")
            self.full_build()
        """midi"""
        def toggle_midi():
            self._display_midi_window = not(self._display_midi_window)
            self.make_menu()
            self.draw_CA()
        def set_mw_size():
            set_mw_details_dialog(self._master, self, title = "set midi window")
            """redraw, and menu, remake mw"""
        def open_midi_mapping_dialog():
#             self._midi_window.use_scale()
#             self._midi_window.full_mapping_assignment(0)
#             print("about to p", self._midi_map_dialog)
            self._midi_map_dialog = set_midi_mapping_dialog(self._master, self, title = "define midi mappings")
#             print("hey2", self._midi_map_dialog)
            """schedule"""
        def toggle_schedule():
            if self._CA._useSchedule:
                self._CA._useSchedule = False
            else:
                """ temp: change this part soon"""
                self._CA.assign_schedule(Schedule(10,(109,210)))
            self.rebuild()
        def make_schedule_dialog():
            if self._CA._schedule == None:
                self._CA._schedule = Schedule()
            self._schedule_dialog = Schedule_dialog(self._master, self, title = "set rule schedule")
            
        
            
            
        
            
        filemenu = Menu(menubar)
        filemenu.add_command(label = "Save State", command = onSaveFile)
        filemenu.add_command(label = "Load State", command = onLoadFile)
        filemenu.add_command(label = "Export Midi File", command = temp_make_file)
        menubar.add_cascade(label = "File", menu = filemenu)
        
        
        details = Menu(menubar)
        details.add_command(label = "CA Type: {}".format(GUI.CA_TYPES[str(type(self._CA._rules))]), command = toriaezu)
        details.add_command(label = "Rule: {}".format(self._CA._rules._rule_num), command = change_rule)
        var = IntVar()
        details.add_checkbutton(label = "Cyclic Universe", variable = var)
        details.add_command(label = "Initial Condition: {}".format(UniversalCA.FIRST_LINE[self._CA._first_line]), 
                            command = initial_condition)
        details.add_command(label = "Width: {}".format(self._width), command = size)
        details.add_command(label = "Length: {}".format(self._length), command = size)
        menubar.add_cascade(label = "Details", menu = details)
        midi = Menu(menubar)
        disp_midi_val = "On" if self._display_midi_window else "Off"
        midi.add_command(label = "Toggle Midi Window: {}".format(disp_midi_val), command = toggle_midi)
        midi.add_command(label = "Midi Window Size", command = set_mw_size)
        midi.add_command(label = "Midi Window Position", command = set_mw_size)
        midi.add_command(label = "Midi Mappings", command = open_midi_mapping_dialog)
        menubar.add_cascade(label = "Midi", menu = midi)
        
        schedule = Menu(menubar)
        schedule_status = "On" if self._CA._useSchedule else "Off"
        schedule.add_command(label = "Use Rule Schedule: {}".format(schedule_status), command = toggle_schedule)
        schedule.add_command(label = "Make Schedule", command = make_schedule_dialog)
        menubar.add_cascade(label = "Schedule Rules", menu = schedule)
        
        
        self._master.config(menu = menubar)
         
    def make_screen(self):
    
        self._width = self._CA._width
        self._length = self._CA._length
        width = self._width * SIZE
        image_height = self._length * SIZE
        
        
        screenwidth = self._master.winfo_screenwidth()
        screenheight = self._master.winfo_screenheight()
        if screenwidth < width:
            width = screenwidth
        if screenheight < image_height:
            canvas_height = screenheight
        else:
            canvas_height = image_height
            
        self._frame = Frame(self._master, bd=2, relief=SUNKEN)

        self._frame.grid_rowconfigure(0, weight=1)
        self._frame.grid_columnconfigure(0, weight=1)
        
        self._xscrollbar = Scrollbar(self._frame, orient=HORIZONTAL)
        self._xscrollbar.grid(row=1, column=0, sticky=E+W)
        
        self._yscrollbar = Scrollbar(self._frame)
        self._yscrollbar.grid(row=0, column=1, sticky=N+S)
        
        self._canvas = Canvas(self._frame, bd=0, scrollregion=(0, 0, width, image_height),
                        xscrollcommand=self._xscrollbar.set,
                        yscrollcommand=self._yscrollbar.set)
        self._canvas.config(height = canvas_height, width = width)
        
        self._canvas.grid(row=0, column=0, sticky=N+S+E+W)
        
        self._xscrollbar.config(command=self._canvas.xview)
        self._yscrollbar.config(command=self._canvas.yview)
        
        self._frame.pack()
            
    def change_size_callback(self):   
        """ this is called by the change_size method in midiwindow, whenever the midiwindow changes size
        it's purpose is to make sure that if the midi window dialog is open when changes occur, they are updated"""
        print('callback called')
        print(self._midi_map_dialog)
        if self._midi_map_dialog != None:
            self._midi_map_dialog.destroy()
            self._midi_map_dialog = set_midi_mapping_dialog(self._master, self, title = "define midi mappings")
            print('callback called done')
    def draw_CA(self):
        
        
        start = self._midi_window._starting_point
        end = (self._midi_window._starting_point + self._midi_window._size - 1)
            
       
        for line in range(self._length):
            for column in range(self._width):
                if self._display_midi_window:
                    if start <= column <= end:
                        colorset = 1
                    else:
                        colorset = 0
                else:
                    colorset = 0
                self._canvas.create_rectangle(column * SIZE, line *SIZE, (column+1)*SIZE, (line+1)*SIZE, 
                                              fill = COLORSETS[colorset][self._CA.get_cell_at(line, column)])
        self._canvas.update()
        
        
        
    def make_midi_window(self):
        if str(type(self._CA._rules)) == "<class 'UniversalCA.ElementaryCARules'>":
            if self._midi_window != None:
                size = self._midi_window.get_size()
                start = self._midi_window.get_starting_point()
                if self._midi_window._useScale:
                    scale_num = self._midi_window._current_scale
                    self._midi_window = TwoStateMidiWindow(self, size, start)
                    self._midi_window.use_scale(scale_num)
                    print("found NUM scale during rebuild:", scale_num)
                else:
                    scale_notes = self._midi_window._custom_mapping
                    print("found CUSTOM scale during rebuild:", scale_notes)
                    self._midi_window = TwoStateMidiWindow(self, size, start, midi_mapping = scale_notes)
            else:
                self._midi_window = TwoStateMidiWindow(self, size, start)
        self._midi_window.make_note_array()
#         self._midi_window.use_scale(0)
        self._midi_window.do_mapping()









if __name__ == "__main__":
    root = Tk()
    r = ElementaryCARules(30)
    ca = ElementaryCA(width = 19, length = 800, rules = r, first_line = 1)
   
   # ca.single_cell_first_line()
    
   
    gui = GUI(root, ca)  
   

    root.mainloop()
    