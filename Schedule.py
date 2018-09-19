from UniversalCA import UniversalCA, ElementaryCA, ElementaryCARules

class Schedule(object):
    def __init__(self, interval = 1, rules_involved = [0]):
        self._instructions = []  #a list of tuples (row, rule)
        self._rules_involved = rules_involved  #a list of the rules in rotation"""
        self.set_interval(interval)
        self._current_rule = -1 #at line 1, will increment to 0
    
    
    def get_scheduled_rule(self, line):
        """note that when it recieves 0, it is actually building line 1"""
        if (line) % self._interval == 0:
            return ElementaryCARules(self.get_next_rule())
        else:
            return ElementaryCARules(self._rules_involved[self._current_rule])
    
    def get_next_rule(self):
        self._current_rule = (self._current_rule + 1)% len(self._rules_involved)
        return self._rules_involved[self._current_rule]
    
    def set_interval(self, value):
        if value <= 0:
            raise ValueError("schedule interval can't be below 1")
        print("in schedule constructor, interval got set: {}".format(value))
        self._interval = value
    
    def display_details(self):
        print("rules {}".format(self._rules_involved))
        print("interval {}".format(self._interval))

if __name__ == "__main__":
    s = Schedule( 5, (200,201,202))
   
    
        

        