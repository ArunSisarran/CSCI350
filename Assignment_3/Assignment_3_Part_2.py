import math

connections = {
    ('O', 'Z'):  71, ('O', 'S'): 151, ('A', 'Z'): 75, ('A', 'S'): 140, ('A', 'T'): 118,
    ('L', 'T'): 111, ('L', 'M'):  70, ('D', 'M'): 75, ('C', 'D'): 120, ('C', 'R'): 146,
    ('C', 'P'): 138, ('R', 'S'):  80, ('F', 'S'): 99, ('B', 'F'): 211, ('B', 'P'): 101,
    ('B', 'G'):  90, ('B', 'U'):  85, ('H', 'U'):  98, ('E', 'H'):  86, ('U', 'V'): 142,
    ('I', 'V'):  92, ('I', 'N'):  87, ('P', 'R'):  97,
    ('J', 'B'):  19, ('J', 'C'): 112, ('J', 'D'): 262, ('J', 'P'): 510, ('J', 'R'): 314}

cities = {
    'A': ( 76, 497), 'B': (400, 327), 'C': (246, 285), 'D': (160, 296), 'E': (558, 294),
    'F': (285, 460), 'G': (368, 257), 'H': (548, 355), 'I': (488, 535), 'L': (162, 379),
    'M': (160, 343), 'N': (407, 561), 'O': (117, 580), 'P': (311, 372), 'R': (227, 412),
    'S': (187, 463), 'T': ( 83, 414), 'U': (471, 363), 'V': (535, 473), 'Z': ( 92, 539),
    'J': (183, 279)}

class Problem(object):
    """The abstract class for a formal problem. A new domain subclasses this,
    overriding `actions` and `results`, and perhaps other methods.
    The default heuristic is 0 and the default action cost is 1 for all states.
    When yiou create an instance of a subclass, specify `initial`, and `goal` states 
    (or give an `is_goal` method) and perhaps other keyword args for the subclass."""

    def __init__(self, initial=None, goal=None, **kwds): 
        self.__dict__.update(initial=initial, goal=goal, **kwds) 
        
    def actions(self, state):        raise NotImplementedError
    def result(self, state, action): raise NotImplementedError
    def is_goal(self, state):        return state == self.goal
    def action_cost(self, s, a, s1): return 1
    def h(self, node):               return 0
    
    def __str__(self):
        return '{}({!r}, {!r})'.format(
            type(self).__name__, self.initial, self.goal)

class Boat(Problem):
 
    def __init__(self, initial=(3, 3, 0, 0, True), goal=(0, 0, 3, 3, False), capacity=3):
        Problem.__init__(self, initial=initial, goal=goal, capacity=capacity)
 
    def side_is_safe(self, students, villains):
        if students == 0:
            return True
        return villains <= students
 
    def state_is_safe(self, state):
        students_si, villains_si, students_man, villains_man, boat_at_si = state
        return (self.side_is_safe(students_si, villains_si) and
                self.side_is_safe(students_man, villains_man))
 
    def actions(self, state):
        students_si, villains_si, students_man, villains_man, boat_at_si = state
 
        if boat_at_si:
            students_here, villains_here = students_si, villains_si
        else:
            students_here, villains_here = students_man, villains_man
 
        legal_moves = []
        for students in range(students_here + 1):
            for villains in range(villains_here + 1):
                riders = students + villains
                if riders < 1 or riders > self.capacity:
                    continue
                new_state = self.result(state, (students, villains))
                if self.state_is_safe(new_state):
                    legal_moves.append((students, villains))
        return legal_moves
 
    def result(self, state, action):
        students_si, villains_si, students_man, villains_man, boat_at_si = state
        students, villains = action
 
        if boat_at_si:
            return (students_si - students, villains_si - villains,
                    students_man + students, villains_man + villains, False)
        else:
            return (students_si + students, villains_si + villains,
                    students_man - students, villains_man - villains, True)
 
    def is_goal(self, state):
        students_si, villains_si, students_man, villains_man, boat_at_si = state
        return (students_si == 0 and villains_si == 0 and
                students_man == 3 and villains_man == 3 and not boat_at_si)
 
    def action_cost(self, s, a, s1):
        return 1
 
    def h(self, node):
        students_si, villains_si, students_man, villains_man, boat_at_si = node.state
        people_left = students_si + villains_si
        if people_left == 0:
            return 0
        trips = math.ceil(people_left / self.capacity)
        if not boat_at_si:
            trips += 1
        return trips

