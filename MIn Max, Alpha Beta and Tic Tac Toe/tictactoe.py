# encoding: utf-8

'''
Created on 2016年10月12日

'''
def mymove(board, mysymbol):
    print
    "Board as seen by the machine:",
    print
    board
    print
    "The machine is playing:",
    print
    mysymbol
    depth = 0
    alpha = float("-inf")
    beta = float("inf")
    isMax = True
    res = minmaxAlgImpro(board, mysymbol, depth, alpha, beta, isMax)
    return res


def minmaxAlgImpro(board, mysymble, depth, alpha, beta, isMax):
    final_move = True
    for i in range(9):
        if board[i] == 0:
            final_move = False
    if final_move:
        return 0
    if isMax:
        res = float("-inf")
        pos = -1
        for i in range(9):
            if board[i] == 0:
                if mysymble == "O":
                    board[i] = -1
                else:
                    board[i] = 1
                winner = check_win(board)
                if winner == "No Winner":
                    cres = minmaxAlgImpro(board, mysymble, depth + 1, alpha, beta, False)
                else:
                    cres = 10 - depth
                if res < cres:
                    res = cres
                    pos = i
                alpha = max(res, alpha)
                board[i] = 0
                if beta <= alpha:
                    break
        if depth == 0:
            return pos + 1
        else:
            return res
    else:
        res = float("inf")
        for i in range(9):
            if board[i] == 0:
                if mysymble == "O":
                    board[i] = 1
                else:
                    board[i] = -1
                winner = check_win(board)
                if winner == "No Winner":
                    cres = minmaxAlgImpro(board, mysymble, depth + 1, alpha, beta, True)
                else:
                    cres = depth - 10
                if res > cres:
                    res = cres
                beta = min(res, beta)
                board[i] = 0
                if beta <= alpha:
                    break
        return res

def check_win(board):
    threes = ((1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7))
    for each in threes:
        total = board[each[0] - 1] + board[each[1] - 1] + board[each[2] - 1]
        if total == -3:
            return "O"
        elif total == 3:
            return "X"
    return "No Winner"
