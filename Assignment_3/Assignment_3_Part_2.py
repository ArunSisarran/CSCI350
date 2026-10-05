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
 
    def safe(self, s, v):
        return s == 0 or v <= s
 
    def is_safe(self, state):
        ss, vs, sm, vm, L = state
        return self.safe(ss, vs) and self.safe(sm, vm)
 
    def actions(self, state):
        ss, vs, sm, vm, L = state
        here_s, here_v = (ss, vs) if L else (sm, vm)
        return [(s, v) for s in range(here_s + 1) for v in range(here_v + 1)
                if 1 <= s + v <= self.capacity and self.is_safe(self.result(state, (s, v)))]
 
    def result(self, state, action):
        ss, vs, sm, vm, L = state
        s, v = action
        if L:
            return (ss - s, vs - v, sm + s, vm + v, False)
        return (ss + s, vs + v, sm - s, vm - v, True)
 
    def is_goal(self, state):
        return state[0] == 0 and state[1] == 0
 
    def action_cost(self, s, a, s1):
        return 1
 
    def h(self, node):
        ss, vs, sm, vm, L = node.state
        n = ss + vs
        return 0 if n == 0 else -(-n // 3) + (0 if L else 1)
