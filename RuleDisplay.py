from tkinter import *
from UniversalCA import UniversalCA, ElementaryCA, ElementaryCARules
COLOURS = ['black', 'blue']
HEIGHT = 600
OFFSET = 2

class RuleDisplay(object):
    """top level gui object for selecting rules"""
    def __init__(self, main_gui):
#         self._rules = main_gui._CA._rules
        self._main_gui = main_gui
        self._numStates = main_gui._CA._numStates
        self._ruleNum = main_gui._CA._rules._rule_num
        self._top = Toplevel()
        self._top.title("choose rule")
        self._top.attributes("-topmost", 1)
        self._frame = Frame(self._top)
        self._frame.pack()
        self._label = Label(self._frame, text = "Rule:")
        self._label.grid(row= 0, column = 0)
        self._ruleVar = StringVar()
        self._ruleEnt = Entry(self._frame, textvariable = self._ruleVar, width = 3)
        def set_by_rule():
            try:
                self._main_gui._CA._rules.make_rules_from_int(int(self._ruleVar.get()))
            except TypeError("must be an integer"):
                pass
            self.draw_rules()
            self._main_gui.rebuild()
        self._btn = Button(self._frame, text = "okay", command = set_by_rule)
        self._btn.grid(row = 0, column = 2)
        
        self._ruleVar.set(self._ruleNum)
        self._ruleEnt.grid(row = 0, column = 1)
#
        self._frame.pack()
        
        self.draw_rules_display()
    
    def draw_rules(self):
        print('in the superclass')
        

class ElementaryCARuleDisplay(RuleDisplay):
    UNIT = (HEIGHT/27)
    def __init__(self, main_gui):
        self._numberOfRules = 8
        super(ElementaryCARuleDisplay, self).__init__(main_gui)
    
    def draw_rules(self):
        for i in range(self._numberOfRules):
            self.draw_single_rule(OFFSET, i, ElementaryCARules.CONTEXT[i], self._main_gui._CA._rules._rules[i])
            
    def draw_rules_display(self):
        UNIT = ElementaryCARuleDisplay.UNIT
        global OFFSET
        self._canvas = Canvas(self._top, width = (UNIT*7), height = HEIGHT)
        self._canvas.pack()
        self.draw_rules()
        def toggle_rule(event):
            for rule_num in range(self._numberOfRules):
                if UNIT*3  < event.x < UNIT*4 and ((OFFSET +1 + rule_num*3) * UNIT) < event.y < ((OFFSET + 2 + rule_num*3)*UNIT):
                    print(self._main_gui._CA._rules._rules[rule_num], rule_num)
                    self._main_gui._CA._rules._rules[rule_num] = (self._main_gui._CA._rules._rules[rule_num] + 1)%2
                    self._ruleVar.set(self._main_gui._CA._rules.get_rule_num_from_rules())
                    #redraw rules
                    self.draw_rules()
                    """???"""
                    
                    self._main_gui.rebuild()
                    return
        self._canvas.bind("<Button-1>", toggle_rule)
        
    def draw_single_rule(self, offset, rule_num, rule_seq, value):
        """offset is how many units down the first rule is place, rule_num is from 0, rule is tuple"""
        UNIT = ElementaryCARuleDisplay.UNIT
        a,b,c = rule_seq
        self._canvas.create_rectangle((UNIT*2, (offset + rule_num*3) * UNIT, UNIT*3, (offset + 1 + rule_num*3)*UNIT), fill = COLOURS[a])
        self._canvas.create_rectangle((UNIT*3, (offset + rule_num*3) * UNIT, UNIT*4, (offset + 1 + rule_num*3)*UNIT), fill = COLOURS[b])
        self._canvas.create_rectangle((UNIT*4, (offset + rule_num*3) * UNIT, UNIT*5, (offset + 1 + rule_num*3)*UNIT), fill = COLOURS[c])
        
        self._canvas.create_rectangle((UNIT*3, (offset +1 + rule_num*3) * UNIT, UNIT*4, (offset + 2 + rule_num*3)*UNIT), fill = COLOURS[value])

if __name__ == "__main__":
    root = Tk()
    r = ElementaryCARules(109)
    ca = ElementaryCA(width = 51, length = 20, rules = r, first_line = 0)
    print(ca._first_line)
    
   # ca.single_cell_first_line()
    
   
    
    
 