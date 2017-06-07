from random import randint
import time
import copy

class RandomBot:
    def __init__(self):
        self.myid = 1
        self.oppid = 2
    def get_move(self, pos, tleft):
        tstart = int(round(time.time() * 1000))
        alpha = float('-inf')
        beta = float('inf')
        best_score, best_move = self.negamax(pos, 4, 0, self.myid, alpha, beta)
        print('cost time:', int(round(time.time() * 1000)) - tstart)
        #print('output:', best_score, best_move)
        return best_move

    def negamax(self, pos, max_depth, current_depth, pid, alpha, beta):
        if current_depth == max_depth or pos.is_game_over(self.myid, self.oppid):
            return ((-1) ** (current_depth)) * pos.evaluate(self.myid, self.oppid), None
        best_move = None
        best_score = float('-inf')
        for move in pos.legal_moves():
            new_pos = copy.deepcopy(pos)
            new_pos.make_move(move, pid, self.myid, self.oppid)
            recursed_score, current_move = self.negamax(new_pos, max_depth, current_depth + 1, self.change_pid(pid), -beta, -max(alpha, best_score))
            current_score = -recursed_score
            #if (current_depth < 3):
                #print('depth:', current_depth, current_score, move)
            if (current_score > best_score):
                best_score = current_score
                best_move = move
                if best_score >= beta:
                    return best_score, best_move
        return best_score, best_move

    def change_pid(self, pid):
        return self.myid if pid == self.oppid else self.oppid

