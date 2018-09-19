from Tkinter import *
import os
import tkMessageBox
from MidiWindow import TwoStateMidiWindow, MidiWindow, SCALES
from Schedule import Schedule

class Dialog(Toplevel):

    def __init__(self, parent, gui, title = None):  #i added gui, so that i could access my own class rather than just its widget

        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)
        self.gui = gui  #hacked, because i should have subclassed the widget rather than included it as an attribute
        self.parent = parent 

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):

        pass # override
    
    
    
    
"""SUBCLASSES"""

"""custom dialogs!!!"""

class select_first_line_dialog(Dialog):     
    def body(self, master):
        self.var = IntVar()
        buttons = []
        buttons.append(Radiobutton (master, text = "single cell", value = 0, variable = self.var))
        buttons.append(Radiobutton (master, text = "random", value = 1, variable = self.var))
        buttons.append(Radiobutton (master, text = "random symmetrical", value = 2, variable = self.var))
        for button in range(len(buttons)):
            buttons[button].grid(row = button, sticky = W)
        buttons[self.gui._CA._first_line].select()
        return master# initial focus

    def apply(self):
        self.gui._CA._first_line = int(self.var.get())
        
class change_size(Dialog):
    def body(self, master):
        self.entLen = IntVar()
        self.entWid = IntVar()
        len_label = Label(master, text = "length")
        wid_label = Label(master, text = "width")
        len_label.grid(row = 0, column = 0, sticky = W)
        wid_label.grid(row = 1, column = 0, sticky = W)
        
        len = Entry(master, textvariable = self.entLen)
        len.grid(row = 0, column = 1)
        wid = Entry(master, textvariable = self.entWid)
        wid.grid(row = 1, column = 1)
        self.entLen.set(self.gui._CA._length)
        self.entWid.set(self.gui._CA._width)
        
        
        return master
    def apply(self):
        #error handling!!!
        try:
            self.gui._CA._width = int(self.entWid.get())
            self.gui._CA._length = int(self.entLen.get())
        except ValueError:
            tkMessageBox.showerror(text = "not valid")
            
class set_mw_details_dialog(Dialog):
    def body(self, master):
        def toggle_midi():
            self.gui._display_midi_window = not(self.gui._display_midi_window)
            self.gui.make_menu()
            self.gui.draw_CA()
        for i in range(3):
            self.grid_columnconfigure(i, weight = 1)
        self._toggle = Button (master, text = "toggle midi window ({})".format("On" if self.gui._display_midi_window else "Off"), 
                                command = toggle_midi)
        self._toggle.grid(row = 0, column = 0, columnspan = 3, sticky = E+W)
        self.entSize = IntVar()
        self.entPosition = IntVar()
        size_label = Label(master, text = "size")
        pos_label = Label(master, text = "starting position")
        size_label.grid(row = 1, column = 0, sticky = W)
        pos_label.grid(row = 2, column = 0, sticky = W)
        
        self._size = Entry(master, textvariable = self.entSize)
        self._size.grid(row = 1, column = 1)
        self._pos = Entry(master, textvariable = self.entPosition)
        self._pos.grid(row = 2, column = 1)
        def onSet():
            try:
                new_size  = self.entSize.get()
                self.entSize.set(self.gui._midi_window.change_size(new_size))  #correct value if bad
                new_start = self.entPosition.get()
                self.gui._midi_window.change_starting_point(new_start)
                self.entPosition.set(self.gui._midi_window.change_starting_point(new_start)) #correct the value if bad
                self.gui._midi_window.make_note_array()
                self.gui.draw_CA()
            except ValueError:
                tkMessageBox.showerror(title = "error", message = "not valid midi window parameters")
            
        self._size_set = Button(master, text = "set", command = onSet)
        self._size_set.grid(row = 1, column = 2)
        self._pos_set = Button(master, text = "set", command = onSet)
        self._pos_set.grid(row = 2, column = 2)
        self.entSize.set(self.gui._midi_window._size)
        self.entPosition.set(self.gui._midi_window._starting_point)
        def onPosL():
            currentPos = self.gui._midi_window._starting_point
            if currentPos > 0:
                self.gui._midi_window.change_starting_point(currentPos -1)
                self.gui._midi_window.make_note_array()
                self.entPosition.set(self.gui._midi_window.change_starting_point(currentPos -1))
                self.gui.draw_CA()
        def onPosC():
            newPos = (int(self.gui._width/2) - int(self.gui._midi_window._size/2))
            self.gui._midi_window.change_starting_point(newPos)
            self.gui._midi_window.make_note_array()
            self.entPosition.set(self.gui._midi_window.change_starting_point(newPos))
            self.gui.draw_CA()
            
        def onPosR():
            currentPos = self.gui._midi_window._starting_point
            if currentPos < self.gui._midi_window._starting_point + self.gui._midi_window._size:
                self.gui._midi_window.change_starting_point(currentPos + 1)
                self.gui._midi_window.make_note_array()
                self.entPosition.set(self.gui._midi_window.change_starting_point(currentPos +1))
                self.gui.draw_CA()
                
        self._posL = Button (master, text = "<", command = onPosL)
        self._posC = Button (master, text = "centre", command = onPosC)
        self._posR = Button (master, text = ">", command = onPosR)
        self._posL.grid(row = 3, column = 0, sticky = E+W)
        self._posC.grid(row = 3, column = 1, sticky = E+W)
        self._posR.grid(row = 3, column = 2, sticky = E+W)
        
        
        
        return master
    def apply(self):
        pass
class set_midi_mapping_dialog(Dialog):
    def body(self, master):
        
        print(self.gui._midi_map_dialog)
        self.gui._midi_map_dialog = self
        """bookkeeping: keep track of whether scale has changed"""
        self._most_recent_scale = []
        """scale"""
        self.scale_var = StringVar()
#         if self.gui._midi_window._useScale:
#             var.set(SCALES[self.gui._midi_window._current_scale])
#             print("option menu thinks that useScale == True")
#         else:
#             var.set("custom")

        def onOptionMenu(sel):
            self.scale_var.set(sel)
            self.gui._midi_window.use_scale(SCALES.index(sel))
            self.gui._midi_window.full_mapping_assignment()
            do_pitch_data()
            
        if self.gui._midi_window._useScale:
            self.scale_var.set(SCALES[self.gui._midi_window._current_scale])
            print("i.e, option menu thinks that useScale == True")
            print("scale is ",self.gui._midi_window._current_scale)
        else:
            self.scale_var.set(SCALES[3]) 
            print("i tried to set it to custom") 
            
         
#         print(var.get())
#         self._scale = apply(OptionMenu, (master, self.scale_var) + tuple(SCALES))
#         self._scale["menu"].add_command(command = onOptionMenu)
        
        self._scale = OptionMenu (master, self.scale_var, *SCALES, command = onOptionMenu)
        
#         print(var.get())
        self._scale.grid(row = 0, columnspan = 2)
        self.scale_var.set(SCALES[self.gui._midi_window._current_scale])
        """root note"""
        root_var = IntVar()
        root_label = Label (master, text = "root pitch:")
        root_Ent = Entry(master, textvariable = root_var)
        root_var.set(self.gui._midi_window._root)
        root_label.grid(row = 1, column = 0)
        root_Ent.grid(row = 1, column = 1)
        
        """pitches"""
        def do_pitch_data():
            notes = self.gui._midi_window._size #and where does midi window get it's size??
            print("size in do pitches" ,self.gui._midi_window._size)
            """hack to address fullmapping not done errr:"""
            if self.gui._midi_window._full_mapping == None:
                print('in do pitch data, ampping was None')
                self.gui._midi_window.do_mapping()
                print("in do_pitches:", self.gui._midi_window._full_mapping)
            self._note_entry = []
            self._intvar_array = []
            lab_array = []
            self._most_recent_scale = []
            for note in range(notes):
                self._intvar_array.append(IntVar())
                try:
                    self._intvar_array[note].set(self.gui._midi_window._full_mapping[note])
                except IndexError:
                    print("exceptional value was {}, size is {}".format(note, len(self.gui._midi_window._full_mapping)))
                self._most_recent_scale.append(self.gui._midi_window._full_mapping[note])
                lab_array.append(Label(master, text = "Cell: {}".format(note)))
                lab_array[note].grid(row = (note +2), column = 0, sticky = E)
                self._note_entry.append(Entry(master,textvariable = self._intvar_array[note], width = 3)) 
                self._note_entry[note].grid(row = (note +2), column = 1, sticky = W)
        do_pitch_data()
#         self._scale = apply(OptionMenu, (master, var) + tuple(SCALES))
        
        
        return master

    def apply(self):
        self._entered_scale = [self._intvar_array[note].get() for note in range(self.gui._midi_window._size)]
        print("entered:",self._entered_scale )
        print("most recent", self._most_recent_scale)
        if self._entered_scale != self._most_recent_scale:
            print('recieved a custom scale')
            self.gui._midi_window.do_custom_mapping(self._entered_scale)
    
    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.gui._midi_map_dialog = None 
        self.destroy()
        self.gui._midi_map_dialog = None 

class Schedule_dialog(Dialog):
    def body(self, master):
        #reset button
        def onReset():
            
            rule_schedule_details(Schedule())
        self._resetBtn = Button(master, text = "Reset", command = onReset)
        self._resetBtn.grid(row = 0, columnspan = 3, sticky = NSEW) 
        #interval
        self._intervalLbl = Label(master, text = "interval (steps):")
        self._intervalLbl.grid(row = 1, column = 0, sticky = W)
        self._intervalEntVar = IntVar()
#         print('in dialog, interval is{}'.format(self.gui._CA._schedule._rule_involved), 'schedule is{}'.format(self.gui._CA._schedule))
        self._intervalEntVar.set(self.gui._CA._schedule._interval)
        self._intervalEnt = Entry(master, textvariable = self._intervalEntVar, width = 3)
        self._intervalEnt.grid(row = 1, column = 1, sticky = E)
        self._rule_frame = Frame(master)
        self._rule_frame.grid(row = 2)
        """make rule schedule"""
        def rule_schedule_details(schedule_so_far = None):
            self._rule_frame.destroy()
            self._rule_frame = Frame(master)
            self._rule_frame.grid(row = 2)
            
            
            if schedule_so_far == None:
                schedule_copy = self.gui._CA._schedule
            else:
                schedule_copy = schedule_so_far
            self._number_of_rules = len(schedule_copy._rules_involved) #actuall this value +1
            self._ruleEnt_array = []
            self._ruleEntVar_array = []
            self._deleteBtn_array = []
            self._lab_array = []
            def add_rule():
                get_entry_data()
                schedule_copy._rules_involved.append(0)
                rule_schedule_details(schedule_copy)
            def delete_rule(rule):
                get_entry_data()
                print ('deleting ruleNum{} which has value {}'.format(rule, self._ruleEnt_array[rule].get()))
                del schedule_copy._rules_involved[rule]
                rule_schedule_details(schedule_copy)
            def get_entry_data():
                schedule_copy._rules_involved = [ruleNum.get() for ruleNum in self._ruleEnt_array]
                    
            for rule in range(self._number_of_rules):
                self._lab_array.append(Label(self._rule_frame, text = "Rule:"))
                self._lab_array[rule].grid(row = 2+rule, column = 0, sticky = W)
                self._ruleEntVar_array.append(IntVar())
                self._ruleEntVar_array[rule].set(schedule_copy._rules_involved[rule])
                self._ruleEnt_array.append(Entry(self._rule_frame, textvariable = self._ruleEntVar_array[rule], width = 5))
                self._ruleEnt_array[rule].grid(row = 2 + rule, column = 1, sticky = E)
                self._deleteBtn_array.append(Button(self._rule_frame, text = "delete rule",
                                                     command = lambda r = rule: delete_rule(r)))
                self._deleteBtn_array[rule].grid(row = 2+ rule, column = 2, sticky = E)
                
            """and let's put an ADD button at the end"""
            self._addBtn = Button(self._rule_frame, text = "Add new rule", command = add_rule)
            self._addBtn.grid(row = 2 + self._number_of_rules, columnspan = 3, sticky = NSEW)    
            
        rule_schedule_details()
        return master

    def apply(self):
        try:
            rules_involved = [int(ruleNum.get()) for ruleNum in self._ruleEnt_array]
       
            interval = int(self._intervalEnt.get())
        except TypeError:
            print('must enter an int')
        self.gui._CA._schedule = Schedule(interval, rules_involved)
        self.gui.rebuild()
       
        
        
            
            
            
        
        
        