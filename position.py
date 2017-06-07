class Position:
    def __init__(self):
        self.board = []
        self.macroboard = []

    def parse_field(self, fstr):
        flist = fstr.replace(';', ',').split(',')
        self.board = [int(f) for f in flist]

    def parse_macroboard(self, mbstr):
        mblist = mbstr.replace(';', ',').split(',')
        self.macroboard = [int(f) for f in mblist]

    def is_legal(self, x, y):
        mbx, mby = x / 3, y / 3
        return self.macroboard[3 * mby + mbx] == -1 and self.board[9 * y + x] == 0

    def legal_moves(self):
        return [(x, y) for x in range(9) for y in range(9) if self.is_legal(x, y)]

    def make_move(self, move, pid, myid, oppid):
        (x, y) = move
        self.board[9 * y + x] = pid
        mbx, mby = x / 3, y / 3
        if self.is_occupied(mbx, mby, myid, oppid):
            self.macroboard[3 * mby + mbx] = pid
        else:
            self.macroboard[3 * mby + mbx] = 0

        next_mbx, next_mby = x % 3, y % 3
        if self.macroboard[3 * next_mby + next_mbx] == 0 or self.macroboard[3 * next_mby + next_mbx] == -1:
            self.macroboard = [(0 if i == -1 else i) for i in self.macroboard]
            self.macroboard[3 * next_mby + next_mbx] = -1
        else:
            self.macroboard = [(-1 if i==0 else i) for i in self.macroboard]

    def get_board(self):
        return ''.join(str(self.board))

    def get_macroboard(self):
        return ''.join(str(self.macroboard))

    def evaluate(self, myid, oppid):
        local_boards = [[self.board[9 * iy + ix] for iy in range(y * 3, y * 3 + 3) for ix in range(x * 3, x * 3 + 3)]
                        for x in range(3) for y in range(3)]
        #print([(b,self.board_score(b, myid, oppid))  for b in local_boards])
        macroboard_score = self.board_score(self.macroboard, myid, oppid)
        if (macroboard_score == 8):
            return 1000
        if (macroboard_score == -8):
            return -1000
        return macroboard_score * 100 + sum([self.board_score(b, myid, oppid) for b in local_boards])

    def board_score(self, b, myid, oppid):
        lines = [[(0, 0), (1, 0), (2, 0)], #r0
                 [(0, 1), (1, 1), (2, 1)], #r1
                 [(0, 2), (1, 2), (2, 2)], #r2
                 [(0, 0), (0, 1), (0, 2)], #c0
                 [(1, 0), (1, 1), (1, 2)], #c1
                 [(2, 0), (2, 1), (2, 2)], #c2
                 [(0, 0), (1, 1), (2, 2)], #d0
                 [(2, 0), (1, 1), (0, 2)]] #d1
        score = 0
        line_scores = [self.line_score([b[y*3+x] for (x,y) in line], myid, oppid) for line in lines]
        if max(line_scores) == 8:
            score = 8
        elif min(line_scores) == -8:
            score = -8
        else:
            score = sum(line_scores)
        return score

    def line_score(self, l, myid, oppid):
        my_num = 0
        opp_num = 0
        for x in l:
            if x == myid:
                my_num = my_num + 1
            elif x == oppid:
                opp_num = opp_num + 1
        if my_num == 3:
            return 8
        elif opp_num == 3:
            return -8
        elif my_num != 0 and opp_num != 0:
            return 0
        elif my_num > 0:
            return 1
        elif opp_num > 0:
            return -1
        return 0

    def is_occupied(self, mbx, mby, myid, oppid):
        lines = [[(0, 0), (1, 0), (2, 0)], #r0
                 [(0, 1), (1, 1), (2, 1)], #r1
                 [(0, 2), (1, 2), (2, 2)], #r2
                 [(0, 0), (0, 1), (0, 2)], #c0
                 [(1, 0), (1, 1), (1, 2)], #c1
                 [(2, 0), (2, 1), (2, 2)], #c2
                 [(0, 0), (1, 1), (2, 2)], #d0
                 [(2, 0), (1, 1), (0, 2)]] #d1
        b = [self.board[9 * iy + ix] for iy in range(mby * 3, mby * 3 + 3) for ix in range(mbx * 3, mbx * 3 + 3)]
        line_scores = [self.line_score([b[y*3+x] for (x,y) in line], myid, oppid) for line in lines]
        return max(line_scores) == 8 or min(line_scores) == -8
    def is_game_over(self, myid, oppid):
        lines = [[(0, 0), (1, 0), (2, 0)], #r0
                 [(0, 1), (1, 1), (2, 1)], #r1
                 [(0, 2), (1, 2), (2, 2)], #r2
                 [(0, 0), (0, 1), (0, 2)], #c0
                 [(1, 0), (1, 1), (1, 2)], #c1
                 [(2, 0), (2, 1), (2, 2)], #c2
                 [(0, 0), (1, 1), (2, 2)], #d0
                 [(2, 0), (1, 1), (0, 2)]] #d1
        line_scores = [self.line_score([self.macroboard[y * 3 + x] for (x, y) in line], myid, oppid) for line in lines]
        return max(line_scores) == 8 or min(line_scores) == -8


