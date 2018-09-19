from random import randrange

class UniversalCA(object):
    """abstract class for any 1d cellular automaton"""
    FIRST_LINE = ["single cell", 'random', 'random symmetrical', 'custom']
    def __init__(self, width = 15, length = 100, rules = None, numStates = 2, first_line = 1, useSchedule = False):
        self._width = width
        self._length = length
        self._rules = rules  #need to make a rules object
        self._universe = []
        self._first_line = first_line
        print("hi, ", self._first_line)
        self._numStates = numStates
        self._useSchedule = useSchedule
        self._schedule = None
    
    def build(self):
        
        self._universe = []
        if self._first_line == 0:
            self.single_cell_first_line()
        elif self._first_line == 1:
            self.random_first_line()
        self.generate_from_first_line()
    def build_from_root(self):
        first_line = self._universe[0]
        self._universe = []
        self._universe.append(first_line)
        self.generate_from_first_line()
        
    
    def random_first_line(self):
        first_line = [randrange(0,self._numStates) for cell in range(self._width)]
        self._universe.append(first_line)
    
    def single_cell_first_line(self, state = 1):
        centre_cell = int(self._width/2)
        first_line = [0 for cell in range(self._width)]
        first_line[centre_cell] = state
        self._universe.append(first_line)
        
    def apply_rule(self, previous_line):
        """abstract for now"""
        pass
    
    def display_in_text(self):
        result =  ""
        for line in self._universe:
            for cell in line:
                result += str(cell)
            result += "\n"
        print(result)
        
    def assign_schedule(self, schedule):
        self._useSchedule = True
        self._schedule = schedule
    
                
        
    
    def generate_from_first_line(self):
        if len(self._universe) != 1:
            print("exactly one line to generate with this function")
            return
        for line in range(self._length - 1):
            if self._useSchedule:
                self._rules = self._schedule.get_scheduled_rule(line)
              #  print(self._rules)
            self._universe.append(self.make_line(self._universe[line]))
    
    def get_cell_at(self,y,x):
        """return cell state at co-ordinate NOTE y value is first"""
        return self._universe[y][x]
            
class UniversalRules(object):
    """abstract class for rules, it's arg will be an int which can be interpretted as a list of rule, or a list of tuples"""  
    def __init__(self, rule_or_rules, useSchedule = False):  
        if type(rule_or_rules) == int:
            self.assign_rules_from_int(rule_or_rules)
        else:
            self._rules = rule_or_rules
            self._ruleNum = None
        
    def assign_rules_from_int(self, rule_or_rules):
        """please override"""
        pass
    
  
    
    

class ElementaryCARules(UniversalRules):
    CONTEXT = [(1,1,1),(1,1,0),(1,0,1),(1,0,0),(0,1,1),(0,1,0),(0,0,1),(0,0,0)]
    def __init__(self, rule_or_rules): 
        
        self._rules = [] 
        self._rule_num = None
        if type(rule_or_rules) == int:
            self.make_rules_from_int(rule_or_rules)
        else:
            self.make_rules_from_list(rule_or_rules)
            
    def make_rules_from_int(self, rule_or_rules):
        temp = rule_or_rules
        power = 7
        result = []
        while power >= 0:
            if temp >= pow(2,power):
                temp -= pow(2,power)
                result.append(1)
            else:
                result.append(0)
            power -= 1
        self.make_rules_from_list(result)
        
    def apply_rule_once(self, context): 
        """takes a tuple of cell states and returns what the rule says it should"""
        #might want to re-write this all as a dictionary for speed 
        return self._rules[ElementaryCARules.CONTEXT.index(context)]
            
        
    def make_rules_from_list(self, rule_or_rules):
        if len(rule_or_rules) != 8:
            print('in UC', rule_or_rules)
            print('type is', type(rule_or_rules))
            raise TypeError("must be 8 rules for an elementary CA.  {} rules found".format(len(rule_or_rules)))
        for rule in rule_or_rules:
            if 0 < rule < 1:
                raise ValueError("rules must be 0 or 1, rule was {}".format(rule)) 
        else:
            self._rules = rule_or_rules
        self._rule_num = self.get_rule_num_from_rules()
            
    def get_rule_num_from_rules(self, rules = None):
        """RETURNS int value from conversion from binary ***DOES NOT SET VALUE***"""
        if rules == None:
            rules = self._rules
        result = 0
        power = 7
        for value in rules:
            result += (value * pow(2,power))
            power -= 1
        """above comment now6 a lie"""
        self._rule_num = result
        return result
                       
    
                   
class ElementaryCA(UniversalCA):
    def __init__(self, width = 15, length = 100,  rules = None, isCyclic = True, first_line = 0):
        
        self._width = width
        
        super(ElementaryCA, self).__init__(width, length, rules, 2, first_line)
        if type(rules) != ElementaryCARules:
            print("need to use ElementaryCARules, current ruletype is {}".format(type(rules)))
        else:
            self._rules = rules
            self._isCyclic = isCyclic
        
    def make_line(self, previous_line):
        """make a three value tuple for each cell, calculate next one, appendto result, return completed line"""
       
        if len(previous_line) != self._width:
            raise ValueError("line is {} cells, should be {} cells".format(len(previous_line),self._width))
        result = []
        #first one is special b/c it depends on vale of isCyclic
        if self._isCyclic == True:
            result.append(self._rules.apply_rule_once((previous_line[-1],previous_line[0],previous_line[1])))
        else:
            result.append(self._rules.apply_rule_once((0,previous_line[0],previous_line[1])))
        #middle should have no problems, start at 2nd index, stop at 2nd last
        for i in range(1, len(previous_line) - 1):
            result.append(self._rules.apply_rule_once((previous_line[i-1],previous_line[i],previous_line[i+1])))
        #end is also special
        if self._isCyclic == True:
            result.append(self._rules.apply_rule_once((previous_line[-2],previous_line[-1],previous_line[0])))
        else:
            result.append(self._rules.apply_rule_once((previous_line[-2],previous_line[-1],0)))
        
        if len(result) != len(previous_line):
            print("big problem. result was {}, should have been {}".format(len(result), len(previous_line)))
        
        return result
        
        
        
if __name__ == "__main__":
    r = ElementaryCARules(30)
    ca = ElementaryCA(width = 51, length = 100, rules = r)
    ca.single_cell_first_line()
    ca.generate_from_first_line()
    ca.display_in_text()
        