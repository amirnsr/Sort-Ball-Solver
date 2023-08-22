import numpy as np

class Pile():
  def __init__(self, pile):
    self.pile = np.copy(pile)
    self.num_of_empty = (pile == " ").sum()

  def get_top(self):
    return self.pile[self.num_of_empty]

  def is_full(self):
    return self.num_of_empty <= 0

  def is_empty(self):
    return self.num_of_empty >= 4

  def add_ball(self, ball):
    if self.is_full():
      return
    self.pile[self.num_of_empty - 1] = ball
    self.num_of_empty -= 1

  def remove_ball(self):
    if self.is_empty():
      return
    self.pile[self.num_of_empty] = " "
    self.num_of_empty += 1

class State():
  def __init__(self, state, action=None):
    self.state = state
    self.visited = 0
    self.order = -1
    self.action = action

  def reset(self):
    self.visited = 0
    self.order = -1

class Piles():
  def __init__(self):
    self.piles = []
    self.states_to_obj = dict()
    self.obj_to_states = dict()

  def set_original_piles(self):
    self.original_piles = np.copy(self.piles)

  def reset(self):
    self.piles = np.copy(self.original_piles)
    for state in self.obj_to_states.keys():
      state.reset()
    self.states_to_obj = dict()
    self.obj_to_states = dict()

  def size(self):
    return len(self.piles)

  def set_state(self):
    state = str({tuple(i.pile) for i in self.piles})
    if state not in self.states_to_obj.keys():
      obj_state = State(state)
      self.obj_to_states[obj_state] = state
      self.states_to_obj[state] = obj_state
    else: 
      return -1

  def get_state(self):
    state = str({tuple(i.pile) for i in self.piles})
    return self.states_to_obj[state]

  def add_pile(self, pile):
    self.piles.append(pile)

  def get_pile(self, index):
    return self.piles[index]

  def show_piles(self ,act=None):
    for i in range(self.size()):
      print('\n')
      if act!=None and i==act[0]:
          print("F: "+str(self.piles[i].pile))
      elif act!=None and i==act[1]:
          print("T: "+str(self.piles[i].pile))
      else:
          print(self.piles[i].pile)

  def available_actions(self):
    actions=[]
    for i in range(self.size()):
        if self.piles[i].is_empty():
            continue
        for j in range(self.size()):
            if j==i:
                continue
            if self.piles[j].is_full():
                continue
            if not self.piles[j].is_empty() and self.piles[i].get_top() != self.piles[j].get_top():
              continue
            actions.append((i,j))
    return actions

  def perform_action(self, action):
    if action==None:
      return
    src, trg = action
    self.piles[trg].add_ball(self.piles[src].get_top())
    self.piles[src].remove_ball()

  def undo_action(self, action):
    trg, src = action
    self.piles[trg].add_ball(self.piles[src].get_top())
    self.piles[src].remove_ball()

  def is_win_state(self):
    for i in range(self.size()):
        if len(set(self.piles[i].pile))>1:
            return False
    return True