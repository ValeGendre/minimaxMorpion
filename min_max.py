



from morpion import Morpion
from copy import deepcopy
import json


def move_hash(move):
    temp = 'ABC'
    row, col = move
    return temp[row] + str(col + 1)
    


class MinMaxTree:
    def __init__(self, state, move, player_turn, father_hash='') -> None:
        self.player = player_turn
        self.move = move
        self.state = state
        self.value = 0
        self.next = []
        if move != (None, None):
            self.hash = father_hash + move_hash(move)
        else: self.hash = ''
        m = Morpion()
        m.state = state
        m.player_id = player_turn
        win, player = m.winning_condition()
        if win:
            self.value = player
            self.best_move = (None, None)
        else:
            self.update_sons()
            self.update_value()
        del m
    
    def update_sons(self):
        for row, temp in enumerate(self.state):
            for col, value in enumerate(temp):
                if value == 0:
                    new_state = deepcopy(self.state)
                    new_state[row, col] = self.player
                    self.next.append(MinMaxTree(new_state, (row, col), -self.player, self.hash))
    
    def update_value(self):
        self.best_move = (0, 0)
        func = max
        best_value = -2
        if self.player == 1:
            func = min
            best_value = 2
        for son in self.next:
            if best_value != func(best_value, son.value):
                self.best_move = son.move
                best_value = func(best_value, son.value)
        self.value = best_value
    
    def create_dict(self, base_dict={}):
        base_dict[self.hash] = self.best_move
        for son in self.next:
            base_dict = son.create_dict(base_dict)
        return base_dict


tree = MinMaxTree(Morpion().state, (None, None), Morpion().player_id)
with open("min_max.json", "w") as f:
    json.dump(tree.create_dict(), f, indent=4)