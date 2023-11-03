from board.move import move
from pieces.nullpiece import nullpiece
from pieces.queen import queen
import random

class AI:

    global tp
    tp=[]


    def __init__(self):
        pass


    def evaluate(self,gametiles):
        min=100000
        count=0
        count2=0
        chuk=[]
        movex=move()
        tp.clear()
        xp=self.minimax(gametiles,3,-1000000000,1000000000,False)

        for zoom in tp:
            if zoom[4]<min:
                chuk.clear()
                chuk.append(zoom)
                min=zoom[4]
            if zoom[4]==min:
                chuk.append(zoom)
        fx=random.randrange(len(chuk))
        print(tp)
        return chuk[fx][0],chuk[fx][1],chuk[fx][2],chuk[fx][3]


    def reset(self,gametiles):
        for x in range(8):
            for y in range(8):
                if gametiles[x][y].pieceonTile.tostring()=='k' or gametiles[x][y].pieceonTile.tostring()=='r':
                    gametiles[x][y].pieceonTile.moved=False


    def updateposition(self,x,y):
        a=x*8
        b=a+y
        return b

    def checkmate(self,gametiles):
        movex=move()
        if movex.checkw(gametiles)[0]=='checked':
            array=movex.movesifcheckedw(gametiles)
            if len(array)==0:
                return True

        if movex.checkb(gametiles)[0]=='checked' :
            array=movex.movesifcheckedb(gametiles)
            if len(array)==0:
                return True

    def stalemate(self,gametiles,player):
        movex=move()
        if player==False:
            if movex.checkb(gametiles)[0]=='notchecked':
                check=False
                for x in range(8):
                    for y in range(8):
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                            lx1=movex.pinnedb(gametiles,moves1,y,x)
                            if len(lx1)==0:
                                continue
                            else:
                                check=True
                            if check==True:
                                break
                    if check==True:
                        break

                if check==False:
                    return True

        if player==True:
                if movex.checkw(gametiles)[0]=='notchecked':
                    check=False
                    for x in range(8):
                        for y in range(8):
                            if gametiles[y][x].pieceonTile.alliance=='White':
                                moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                                lx1=movex.pinnedw(gametiles,moves1,y,x)
                                if len(lx1)==0:
                                    continue
                                else:
                                    check=True
                                if check==True:
                                    break
                        if check==True:
                            break

                    if check==False:
                        return True






    def minimax(self,gametiles, depth,alpha , beta ,player):
        if depth==0 or self.checkmate(gametiles)==True or self.stalemate(gametiles,player)==True:
            return self.calculateb(gametiles)
        if not player:
            minEval=100000000
            kp,ks=self.eva(gametiles,player)
            for lk in kp:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.move(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,True)
                    if evalk<minEval and depth==3:
                        tp.clear()
                        tp.append(move)
                    if evalk==minEval and depth==3:
                        tp.append(move)
                    minEval=min(minEval,evalk)
                    beta=min(beta,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break

                if beta<=alpha:
                    break
            return minEval

        else:
            maxEval=-100000000
            kp,ks=self.eva(gametiles,player)
            for lk in ks:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.movew(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,False)
                    maxEval=max(maxEval,evalk)
                    alpha=max(alpha,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break
                if beta<=alpha:
                    break

            return maxEval



    def printboard(self,gametilles):
        count = 0
        for rows in range(8):
            for column in range(8):
                print('|', end=gametilles[rows][column].pieceonTile.tostring())
            print("|",end='\n')


    def checkeva(self,gametiles,moves):
        arr=[]
        for move in moves:
            lk=[[move[2],move[3]]]
            arr.append(self.calci(gametiles,move[0],move[1],lk))

        return arr



    def eva(self,gametiles,player):
        lx=[]
        moves=[]
        kp=[]
        ks=[]
        movex=move()
        for x in range(8):
            for y in range(8):
                    if gametiles[y][x].pieceonTile.alliance=='Black' and player==False:
                        if movex.checkb(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedb(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            kp=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='K'):
                                ax=movex.castlingb(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([0,6])
                                        if l=='qs':
                                            moves.append([0,2])
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            lx=movex.pinnedb(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        kp.append(self.calci(gametiles,y,x,moves))


                    if gametiles[y][x].pieceonTile.alliance=='White' and player==True:
                        if movex.checkw(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedw(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            ks=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if moves==None:
                            print(y)
                            print(x)
                            print(gametiles[y][x].pieceonTile.position)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='k'):
                                ax=movex.castlingw(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([7,6])
                                        if l=='qs':
                                            moves.append([7,2])
                        if gametiles[y][x].pieceonTile.alliance=='White':
                            lx=movex.pinnedw(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        ks.append(self.calci(gametiles,y,x,moves))

        return kp,ks



    def calci(self,gametiles,y,x,moves):
        arr=[]
        jk=object
        for move in moves:
            jk=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            mk=self.calculateb(gametiles)
            gametiles[y][x].pieceonTile=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=jk
            arr.append([y,x,move[0],move[1],mk])
        return arr


    def calculateb(self, gametiles):
        value = 0
        piece_values = {
            'P': -100, 'N': -350, 'B': -350, 'R': -525, 'Q': -1000, 'K': -10000,
            'p': 100, 'n': 350, 'b': 350, 'r': 525, 'q': 1000, 'k': 10000
        }

        # Additional value for the Queen's Gambit opening move
        if gametiles[1][3].pieceonTile.tostring() == "-" and gametiles[1][4].pieceonTile.tostring() == '-':
            value += 30

        active_piece_bonus = {
            'Q': 50, 'R': 30, 'B': 20
        }

        for x in range(8):
            for y in range(8):
                piece = gametiles[y][x].pieceonTile.tostring()
                if piece in piece_values:
                    value += piece_values[piece]

                if piece == 'P' and (x, y) in [(4, 1), (3, 2), (4, 2)]:
                    value += 20 # Bonus for advancing the pawn

                # Develop the knight towards the center
                if piece == 'N' and (x, y) in [(1, 0), (6, 0)]:
                    value += 40 # Bonus for developing the knight

                # Attack a pawn
                if piece == 'N':
                    for dx, dy in [(1, 2), (1, -2), (-1, 2), (-1, -2)]:
                        new_x, new_y = x + dx, y + dy
                        if 0 <= new_x < 8 and 0 <= new_y < 8 and gametiles[new_y][new_x].pieceonTile.tostring() == 'p':
                            value += 30 # Bonus for attacking a pawn

                # Optimal pawn defense
                if piece == 'P':
                    moves = self.get_legal_moves_for_piece(gametiles, x, y)
                    for move in moves:
                        new_x, new_y = move[2], move[3]
                        if gametiles[new_y][new_x].pieceonTile.tostring() != ' ':
                            value += 10 # Bonus for moves that defend pawns optimally
                        else:
                            # Consider not ignoring a better way to add a defender
                            for dx, dy in [(1, 1), (1, -1)]:
                                target_x, target_y = x + dx, y + dy
                                if 0 <= target_x < 8 and 0 <= target_y < 8:
                                    target_piece = gametiles[target_y][target_x].pieceonTile.tostring()
                                    if target_piece == 'N':
                                        value += 20 # Bonus for using a knight to defend a pawn

                
                # Develop the dark-squared bishop to an active diagonal
                if piece == 'B' and (x, y) == (2, 0):
                    value += 30 # Bonus for developing the bishop

                # Prevent the opponent from capturing our own pawn while defending pieces
                if piece == 'N':
                    for dx, dy in [(1, 2), (1, -2), (-1, 2), (-1, -2)]:
                        new_x, new_y = x + dx, y + dy
                        if 0 <= new_x < 8 and 0 <= new_y < 8 and gametiles[new_y][new_x].pieceonTile.tostring() == 'p':
                            value += 30 # Bonus for attacking a pawn

                # Avoid giving up the Bishop
                if piece == 'B':
                    for dx, dy in [(1, 2), (1, -2), (-1, 2), (-1, -2)]:
                        new_x, new_y = x + dx, y + dy
                        if 0 <= new_x < 8 and 0 <= new_y < 8 and gametiles[new_y][new_x].pieceonTile.tostring() == 'P':
                            value -= 50 # Penalty for losing the Bishop

                # Ensure Opponents checkmate opportunities are considered
                if piece == 'Q':
                    if self.has_checkmate_opportunity(gametiles):
                        value += 1000 # Encourage checkmate opportunities

                # Check that the knight on b1 is defended
                if piece == 'N' and x == 1 and y == 0:
                    if gametiles[2][2].pieceonTile.tostring() == 'P':
                        value += 50 # Bonus for defending the knight

                # Prepare for Bishop development on the long diagonal
                if piece == 'P' and (x, y) == (1, 2):
                    value += 30 # Bonus for preparing Bishop development

                # Prioritize King's Pawn Opening
                if piece == 'P' and (x, y) in [(4, 1), (3, 2), (4, 2)]:
                    value += 20 # Bonus for advancing the pawn

                # Develop the knight towards the center
                if piece == 'N' and (x, y) in [(1, 0), (6, 0)]:
                    value += 40 # Bonus for developing the knight

                # Attack a pawn
                if piece == 'N':
                    for dx, dy in [(1, 2), (1, -2), (-1, 2), (-1, -2)]:
                        new_x, new_y = x + dx, y + dy
                        if 0 <= new_x < 8 and 0 <= new_y < 8 and gametiles[new_y][new_x].pieceonTile.tostring() == 'p':
                            value += 30 # Bonus for attacking a pawn

                # Prepare to castle
                if piece == 'K' and (x, y) in [(4, 7), (3, 7), (5, 7)]:
                    value += 20 # Bonus for king's potential castle positions

                # Bonus for controlling the center
                if (x, y) in [(3, 3), (3, 4), (4, 3), (4, 4)]:
                    value += piece_values.get(piece, 0) / 2

                # Consider the Queen's Gambit opening (offering a wing pawn)
                if (x, y) == (1, 1) and piece == 'P':
                    value += 20 # Wing pawn offered for center control

                # Check for opportunities to capture free pawns
                if piece == 'n':
                    moves = self.get_legal_moves_for_piece(gametiles, x, y)
                    for move in moves:
                        if move[2] >= 0 and move[2] < 8 and move[3] >= 0 and move[3] < 8:
                            target_piece = gametiles[move[3]][move[2]].pieceonTile.tostring()
                            if target_piece == 'P':
                                value += 50 # Reward for capturing a free pawn

                # Check for opportunities to win material through a fork
                if piece == 'n':
                    moves = self.get_legal_moves_for_piece(gametiles, x, y)
                    for move in moves:
                        if move[2] >= 0 and move[2] < 8 and move[3] >= 0 and move[3] < 8:
                            target_piece = gametiles[move[3]][move[2]].pieceonTile.tostring()
                            if target_piece in ('P', 'B'):
                                value += 100 # Reward for a potential fork

                # Consider the opponent's knight development
                if piece == 'n':
                    if (x, y) in [(3, 3), (3, 4), (4, 3), (4, 4)]:
                        value -= 50 # Opponent's knight attacks the center
                    if (x, y) == (1, 0) or (x, y) == (6, 0):
                        value -= 30 # You missed an opportunity to better defend a pawn

                # Consider defending pawns and pieces under attack
                if piece in ('P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k'):
                    moves = gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                    if moves is not None:
                        for move in moves:
                            if len(move) >= 4:
                                new_x, new_y = move[2], move[3]
                                if gametiles[new_y][new_x].pieceonTile.tostring() != ' ':
                                    value += 10 # Bonus for moves that defend pawns or pieces under attack

                # Check if a pawn is under threat
                if piece == 'P' and self.is_pawn_under_threat(gametiles, x, y, 'p'):
                    value -= 30 # Penalize for having a pawn under threat

                # Revealing an attack on a pawn
                if piece == 'N':
                    for dx, dy in [(1, 2), (1, -2), (-1, 2), (-1, -2)]:
                        new_x, new_y = x + dx, y + dy
                        if 0 <= new_x < 8 and 0 <= new_y < 8:
                            target_piece = gametiles[new_y][new_x].pieceonTile.tostring()
                            if target_piece == 'p':
                                value += 20 # Bonus for revealing an attack on a pawn

                # Opponents moves causing trouble
                opponent_moves = self.get_legal_moves_for_piece(gametiles, x, y)
                if opponent_moves:
                    value -= 20 # Penalize for opponent moves causing potential trouble


                # Working on values of pawns
                if piece in ('P', 'p'):
                    # Make pawns more important in the center
                    if (x, y) in [(3, 3), (3, 4), (4, 3), (4, 4)]:
                        value += piece_values[piece] * 1.5
                    # Consider pawns strength and weakness
                    if x >= 4:  # Considering advancing pawns only when they are needed to protect squares behind
                        value -= 10

                # Working on values for Bishops
                if piece in ('B', 'b'):
                    # Considering Bishops strengths and weaknesses
                    if x < 4:
                        value += 20
                    # Reward active Bishops
                    active_bonus = active_piece_bonus.get(piece, 0)
                    value += active_bonus

                # Working on values for Rooks
                if piece in ('R', 'r'):
                    # Considering Rooks strengths and weaknesses
                    if x < 4:
                        value += 40
                    # Reward active Rooks
                    active_bonus = active_piece_bonus.get(piece, 0)
                    value += active_bonus

                # Working on values for Queens
                if piece in ('Q', 'q'):
                    # Considering queens strengths and weaknesses
                    if x < 4:
                        value += 60
                    # Reward active Queens
                    active_bonus = active_piece_bonus.get(piece, 0)
                    value += active_bonus

                # Working on values for Kings
                if piece in ('K', 'k'):
                    # Considering Kings strengths and weaknesses
                    if x < 4:
                        value += 80
                    # Assess pawns in front of kings
                    if piece == 'k':
                        for i in range(y + 1, 8):
                            if gametiles[i][x].pieceonTile.tostring() == 'P':
                                value -= 30  # Penalize for a hostile pawn in front of the black king
                    elif piece == 'K':
                        for i in range(0, y):
                            if gametiles[i][x].pieceonTile.tostring() == 'p':
                                value -= 30  # Penalize for a hostile pawn in front of the white king
                    # Assess pawns as bodyguards
                    if (piece == 'k' and y < 2) or (piece == 'K' and y > 5):
                        value += 30  # Give a bonus when pawns are protecting the King
                    # Assess King exposure
                    if (piece == 'k' and (x > 4 or x < 3)) or (piece == 'K' and (x > 4 or x < 3)):
                        value -= 40  # Penalize an exposed King

                    # Additional considerations for specific pieces
                    # Avoiding knight vulnerability
                    if piece == 'n':
                        if self.is_knight_under_threat(gametiles, x, y, 'k'):
                            value -= 20

                    # Capturing free pawns
                    if piece == 'n':
                        for dx, dy in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
                            new_x, new_y = x + dx, y + dy
                            if 0 <= new_x < 8 and 0 <= new_y < 8:
                                target_piece = gametiles[new_y][new_x].pieceonTile.tostring()
                                if target_piece == 'P':
                                    value += 30  # Reward for capturing a free pawn

                    # Checkmate opportunities
                    if piece == 'Q':
                        if self.has_checkmate_opportunity(gametiles, x, y, 'k'):
                            value += 1000  # Encourage checkmate opportunities

                    # Defending Rooks
                    if piece == 'r':
                        if self.is_rook_under_threat(gametiles, x, y, 'R'):
                            value += 20  # Reward for defending a rook

                    # Avoid giving up the Queen
                    if piece == 'Q':
                        if self.is_queen_under_threat(gametiles, x, y, 'p'):
                            value -= 100  # Penalize for being under threat by a pawn

        return value
    
    def get_legal_moves_for_piece(self, gametiles, x, y):
        piece = gametiles[y][x].pieceonTile.tostring()
        moves = []

        if piece == 'P':
            # Pawn moves for white
            if y - 1 >= 0 and gametiles[y - 1][x].pieceonTile.tostring() == '-':
                moves.append((x, y, x, y - 1))
            if y == 6 and gametiles[y - 1][x].pieceonTile.tostring() == '-' and gametiles[y - 2][x].pieceonTile.tostring() == '-':
                moves.append((x, y, x, y - 2))
            if x - 1 >= 0 and y - 1 >= 0 and gametiles[y - 1][x - 1].pieceonTile.alliance == 'Black':
                moves.append((x, y, x - 1, y - 1))
            if x + 1 < 8 and y - 1 >= 0 and gametiles[y - 1][x + 1].pieceonTile.alliance == 'Black':
                moves.append((x, y, x + 1, y - 1))

        if piece == 'N':
            # Knight moves
            knight_moves = [(-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, -2), (2, -1), (2, 1), (1, 2)]
            for dx, dy in knight_moves:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    target_piece = gametiles[new_y][new_x].pieceonTile.tostring()
                    if target_piece != piece:  # Ensure the target square is not occupied by your own piece
                        moves.append((x, y, new_x, new_y))

        if piece == 'B':
            # Bishop moves (diagonals)
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dx, dy in directions:
                new_x, new_y = x, y
                while True:
                    new_x, new_y = new_x + dx, new_y + dy
                    if 0 <= new_x < 8 and 0 <= new_y < 8:
                        target_piece = gametiles[new_y][new_x].pieceonTile.tostring()
                        if target_piece == '-':
                            moves.append((x, y, new_x, new_y))
                        else:
                            if target_piece.islower():
                                moves.append((x, y, new_x, new_y))
                            break
                    else:
                        break
            # Check for bishop development towards the long diagonal
            if x == 2 and y == 0:
                moves.append((x, y, 3, 1))
            # Check for knight safety
            for dx, dy in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    target_piece = gametiles[new_y][new_x].pieceonTile.tostring()
                    if target_piece == 'N':
                        moves.append((x, y, new_x, new_y))  # Include moves that protect the knight

        if piece == 'R':
            # Rook moves (horizontally and vertically)
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dx, dy in directions:
                new_x, new_y = x, y
                while True:
                    new_x, new_y = new_x + dx, new_y + dy
                    if 0 <= new_x < 8 and 0 <= new_y < 8:
                        target_piece = gametiles[new_y][new_x].pieceonTile.tostring()
                        if target_piece == '-':
                            moves.append((x, y, new_x, new_y))
                        else:
                            if target_piece.islower():
                                moves.append((x, y, new_x, new_y))
                            break
                    else:
                        break
            # Check for knight safety
            for dx, dy in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    target_piece = gametiles[new_y][new_x].pieceonTile.tostring()
                    if target_piece == 'N':
                        moves.append((x, y, new_x, new_y))  # Include moves that protect the knight

        if piece == 'Q':
            # Queen moves (combines Rook and Bishop moves)
            rook_moves = []
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dx, dy in directions:
                new_x, new_y = x, y
                while True:
                    new_x, new_y = new_x + dx, new_y + dy
                    if 0 <= new_x < 8 and 0 <= new_y < 8:
                        target_piece = gametiles[new_y][new_x].pieceonTile.tostring()
                        if target_piece == '-':
                            rook_moves.append((x, y, new_x, new_y))
                        else:
                            if target_piece.islower():
                                rook_moves.append((x, y, new_x, new_y))
                            break
                    else:
                        break

            bishop_moves = []
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dx, dy in directions:
                new_x, new_y = x, y
                while True:
                    new_x, new_y = new_x + dx, new_y + dy
                    if 0 <= new_x < 8 and 0 <= new_y < 8:
                        target_piece = gametiles[new_y][new_x].pieceonTile.tostring()
                        if target_piece == '-':
                            bishop_moves.append((x, y, new_x, new_y))
                        else:
                            if target_piece.islower():
                                bishop_moves.append((x, y, new_x, new_y))
                            break
                    else:
                        break

            moves.extend(rook_moves)
            moves.extend(bishop_moves)
        # Check for queen safety
        if x == 3 and y == 0:
            moves.append((x, y, 3, 1))  # Move the queen up one square (example move)

        # Check for knight safety
        for dx, dy in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                target_piece = gametiles[new_y][new_x].pieceonTile.tostring()
                if target_piece == 'N':
                    moves.append((x, y, new_x, new_y))  # Include moves that protect the knight
        
        if piece == 'K':
            # King moves
            king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dx, dy in king_moves:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    target_piece = gametiles[new_y][new_x].pieceonTile.tostring()
                    if target_piece == '-' or target_piece.islower():
                        moves.append((x, y, new_x, new_y))
            # Check for knight safety
            for dx, dy in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    target_piece = gametiles[new_y][new_x].pieceonTile.tostring()
                    if target_piece == 'N':
                        moves.append((x, y, new_x, new_y))  # Include moves that protect the knight

        return moves

    def is_knight_under_threat(self, gametiles, knight_x, knight_y, alliance):
        opponent_alliance = "White" if alliance == "Black" else "Black"

        for dx, dy in [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]:
            new_x, new_y = knight_x + dx, knight_y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                piece = gametiles[new_y][new_x].pieceonTile
                if piece is not None and piece.alliance == opponent_alliance:
                    return True
        return False

    def has_checkmate_opportunity(self, gametiles):
        for x in range(8):
            for y in range(8):
                piece = gametiles[y][x].pieceonTile
                if piece is not None and piece.tostring() != '-':
                    piece_moves = piece.legalmoveb(gametiles)
                    if piece_moves is not None:
                        for move in piece_moves:
                            if len(move) >= 4: # Ensure there are at least 4 elements in the move
                                new_x, new_y = move[2], move[3]
                                new_gametiles = gametiles.copy() # Create a copy of the board for testing
                                new_gametiles[new_y][new_x].setpiece(piece) # Make the move on the copy of the board

                                if not self.is_king_safe(new_gametiles, piece.alliance):
                                    return True # Checkmate opportunity found for a piece
                        
        return False # No checkmate opportunity for any piece
    
    def is_king_safe(self, gametiles, alliance):
        king_x, king_y = None, None

        # Find the king's coordinates
        for x in range(8):
            for y in range(8):
                piece = gametiles[y][x].pieceonTile
                if piece is not None and piece.alliance == alliance and piece.tostring() == 'k':
                    king_x, king_y = x, y

        if king_x is None or king_y is None:
            return False # King not found, return as unsafe
        
        # Check if the king is under threat by an opposing piece
        opponent_alliance = "White" if alliance == "Black" else "Black"
        for x in range(8):
            for y in range(8):
                piece = gametiles[y][x].pieceonTile
                if piece is not None and piece.alliance == opponent_alliance:
                    moves = piece.legalmoveb(gametiles)
                    for move in moves:
                        if move[2] == king_x and move[3] == king_y:
                            return False # King is under threat
        return True # King is safe

    def is_rook_under_threat(self, gametiles, rook_x, rook_y, rook_piece):
        opponent_alliance = "White" if rook_piece.alliance == "Black" else "Black"

        # Check if any of the opponent's pieces can capture the rook
        for x in range(8):
            for y in range(8):
                if gametiles[y][x].pieceonTile.alliance == opponent_alliance:
                    moves = gametiles[y][x].pieceonTile.legalmoveb(gametiles)  # Get legal moves for the opponent's piece
                    for move in moves:
                        if move[2] == rook_x and move[3] == rook_y:
                            return True  # Rook is under threat

        return False  # Rook is not under threat

    def is_queen_under_threat(self, gametiles, queen_x, queen_y):
        queen_piece = gametiles[queen_y][queen_x].pieceonTile
        opponent_alliance = "White" if queen_piece.alliance == "Black" else "Black"

        # Check if any of the opponent's pieces can capture the queen
        for x in range(8):
            for y in range(8):
                if gametiles[y][x].pieceonTile.alliance == opponent_alliance:
                    opponent_piece = gametiles[y][x].pieceonTile.tostring()
                    moves = gametiles[y][x].pieceonTile.legalmoveb(gametiles) # Get legal moves for the opponents pieces
                    for move in moves:
                        if move[2] == queen_x and move[3] == queen_y:
                            return True # Queen is under threat by an opponent's piece
        return False  # Queen is not under threat
    
    def is_pawn_under_threat(self, gametiles, piece_x, piece_y, opponent_piece):
        # Check if the pawn is under threat by an opponent's piece
        for dx in range(8):
            for dy in range(8):
                if piece_x == dx and piece_y == dy:
                    continue # Skip checking the piece against itself
                target_piece = gametiles[dy][dx].pieceonTile.tostring()
                if target_piece == opponent_piece:
                    moves = gametiles[dy][dx].pieceonTile.legalmoveb(gametiles) # Get legal moves for the opponents piece
                    if moves is not None:
                        for move in moves:
                            if len(move) == 4 and move[2] == piece_x and move[3] == piece_y:
                                return True # Piece is under threat
            return False
     

    def move(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='K' or gametiles[y][x].pieceonTile.tostring()=='R':
            gametiles[y][x].pieceonTile.moved=True

        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='P' and y+1==n and y==6:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='P':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('Black',self.updateposition(n,m))
                promotion=False

        return gametiles



    def revmove(self,gametiles,x,y,n,m,mts):
        if gametiles[x][y].pieceonTile.tostring()=='K':
            if m==y-2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[n][7].pieceonTile.moved=False

                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            elif m==y+2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(m,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[n][0].pieceonTile.moved=False
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts

            return gametiles

        if gametiles[x][y].pieceonTile.tostring()=='k':
            if m==y-2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            elif m==y+2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(n,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts


            return gametiles

        gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
        s=self.updateposition(n,m)
        gametiles[n][m].pieceonTile.position=s
        gametiles[x][y].pieceonTile=mts

        return gametiles



    def movew(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='k' or gametiles[y][x].pieceonTile.tostring()=='r':
            pass

        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='p' and y-1==n and y==1:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='p':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('White',self.updateposition(n,m))
                promotion=False

        return gametiles
























                        
