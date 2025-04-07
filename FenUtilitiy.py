def fen_to_internal(fen):
    from ChessEngine import Piece
    array_output = [0 for i in range(64)]
    type_from_symbol = {'k':Piece.KING, 'p':Piece.PAWN, 'n':Piece.KNIGHT, 'b':Piece.BISHOP, 'r':Piece.ROOK, 'q':Piece.QUEEN,
                        'K':Piece.KING, 'P':Piece.PAWN, 'N':Piece.KNIGHT, 'B':Piece.BISHOP, 'R':Piece.ROOK, 'Q':Piece.QUEEN}
    col = 0
    row = 7

    for c in fen:
        if c == '/':
            col = 0
            row -= 1
        else:
            if c.isdigit():
                col += int(c)
            else:
                piece_color = Piece.WHITE if c.isupper() else Piece.BLACK
                piece_type = type_from_symbol[c]
                array_output[row*8 + col] = piece_type + piece_color
                col += 1
    return array_output

def internal_to_fen(A):
    fen = ''
    type_from_int = {
        9: 'K', 10: 'P', 11: 'N', 12: 'B', 13: 'R', 14: 'Q',
        17: 'k', 18: 'p', 19: 'n', 20: 'b', 21: 'r', 22: 'q'
    }

    i = 56  # Start of row 8
    while i >= 0:
        blank_squares = 0
        for j in range(8):
            val = A[i + j]
            if val == 0:
                blank_squares += 1
            else:
                if blank_squares > 0:
                    fen += str(blank_squares)
                    blank_squares = 0
                fen += type_from_int[val]
        if blank_squares > 0:
            fen += str(blank_squares)
        if i != 0:
            fen += '/'
        i -= 8
    return fen

if __name__ == '__main__':
    start = '5Q2/p2kpp1r/2ppb2n/6N1/2P2N1p/3P4/PP1KPPPP/R4B1R'
    print(start)
    internal = fen_to_internal(start)
    print(internal)
    fen = internal_to_fen(internal)
    print(fen)
    print(fen == start)