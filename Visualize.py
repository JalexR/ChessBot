import PySimpleGUI as sg
import time
import threading
import queue

def draw_board(graph):
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 != 0:
                c ='white'
            else:
                c = 'green'
            graph.DrawRectangle((i*100, j*100), (i*100+100, j*100+100), fill_color=c)


def FEN_to_visual(graph, FEN, bottom_color):
    dig = 0
    images = []
    allowed = set('/12345678bknpqrBKNPQR')

    if not (set(FEN) <= allowed):
        raise Exception('Invalid FEN provided to FEN visualizer: invalid character')

    for c in FEN:
        row = dig // 8
        col = dig - (row * 8)

        if(c == '/'):
            if(col == 0):
                continue
            else:
                raise Exception('Invalid FEN provided to FEN visualizer: improperly filled row')
        elif(c.isdigit()):
            dig += int(c)
            continue
        else:
            dig += 1
            file_name = 'Piece-Assets\\White\\' + c + '.png' if c.isupper() else 'Piece-Assets\\Black\\' + c + '.png'
            if bottom_color == 'White':
                images.append(graph.draw_image(filename=file_name, location=(col * 100 + 20, 780 - row * 100))) #White on bottom
            else:
                images.append(graph.draw_image(filename=file_name, location=(720  - col * 100, row * 100 + 80))) #Black on bottom


    return images

def generate_pieces(graph, piece_images, fen, color):
    for image in piece_images:
        graph.delete_figure(image)
    piece_images = FEN_to_visual(graph, fen, color)
    return piece_images

moves_que = queue.Queue()
def create_window(moves=None):
    # All the stuff inside your window.
    layout =     [
        [sg.Text("Color on bottom:", font=("Calibri", 12)), sg.Combo(['White', 'Black'], default_value='White', enable_events=True, key='bottom_color')],
        [
            sg.Graph(
                canvas_size=(800, 800),
                graph_bottom_left=(0, 0),
                graph_top_right=(800, 800),
                key="graph"
            )
        ],
        [sg.Text("FEN:", font=("Calibri", 24)), sg.Input(default_text='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR', font=("Calibri", 16), key='FEN_input')],
        [[sg.Button('Generate', size=(15,3), bind_return_key=True, key='Generate'), sg.Button('Reset', size=(15,3), key='Reset')]]
    ]

    window = sg.Window('Chess', layout, finalize=True)
    graph = window['graph'] 
    in_box = window['FEN_input']
    # window['FEN_input'].bind("<Return>", "Generate")

    draw_board(graph)
    piece_images = FEN_to_visual(graph, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR', 'White')

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        #If user closes window stop loop
        if event == sg.WIN_CLOSED:
            break

        if event == 'Generate':
            piece_images = generate_pieces(graph, piece_images, values['FEN_input'], values['bottom_color'])
            while not moves_que.empty():
                fen = moves_que.get()
                in_box.update(fen)
                piece_images = generate_pieces(graph, piece_images, fen, values['bottom_color'])
                window.read(timeout=10)
                time.sleep(.1)
            
        if event == 'bottom_color':
            piece_images = generate_pieces(graph, piece_images, values['FEN_input'], values['bottom_color'])

        if event == 'Reset':
            for image in piece_images:
                graph.delete_figure(image)
            in_box.update('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
            piece_images = FEN_to_visual(graph, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR', values['bottom_color'])


    window.close()

moves = [
'rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR',
'rnbqkbnr/ppp1pppp/3p4/8/2P5/8/PP1PPPPP/RNBQKBNR',
'rnbqkbnr/ppp1pppp/3p4/8/Q1P5/8/PP1PPPPP/RNB1KBNR',
'rnbqkbnr/p1p1pppp/3p4/1p6/Q1P5/8/PP1PPPPP/RNB1KBNR',
'rnbqkbnr/p1p1pppp/3p4/1Q6/2P5/8/PP1PPPPP/RNB1KBNR',
'rn1qkbnr/p1pbpppp/3p4/1Q6/2P5/8/PP1PPPPP/RNB1KBNR',
'rn1qkbnr/p1pbpppp/3p4/8/1QP5/8/PP1PPPPP/RNB1KBNR',
'rn1qkbnr/p1pbppp1/3p4/7p/1QP5/8/PP1PPPPP/RNB1KBNR',
'rn1qkbnr/p1pbppp1/3p4/7p/1QP5/3P4/PP2PPPP/RNB1KBNR',
'rn1qkbnr/p1pbpp2/3p2p1/7p/1QP5/3P4/PP2PPPP/RNB1KBNR',
'rn1qkbnr/p1pbpp2/3p2p1/7p/1QP5/3P1N2/PP2PPPP/RNB1KB1R',
'rn1qkbnr/p1pbpp2/3p4/6pp/1QP5/3P1N2/PP2PPPP/RNB1KB1R',
'rn1qkbnr/p1pbpp2/3p4/6Np/1QP5/3P4/PP2PPPP/RNB1KB1R',
'rn1qkb1r/p1pbpp2/3p3n/6Np/1QP5/3P4/PP2PPPP/RNB1KB1R',
'rn1qkb1r/p1pbpp2/3p3n/6Np/1QP5/2NP4/PP2PPPP/R1B1KB1R',
'rn1qkb1r/p1p1pp2/3p3n/5bNp/1QP5/2NP4/PP2PPPP/R1B1KB1R',
'rn1qkb1r/p1p1pp2/3p3n/3N1bNp/1QP5/3P4/PP2PPPP/R1B1KB1R',
'rn1qkb1r/p3pp2/2pp3n/3N1bNp/1QP5/3P4/PP2PPPP/R1B1KB1R',
'rn1qkb1r/p3pp2/2pp3n/5bNp/1QP2N2/3P4/PP2PPPP/R1B1KB1R',
'rn1qkb1r/p3pp2/2pp3n/5bN1/1QP2N1p/3P4/PP2PPPP/R1B1KB1R',
'rn1qkb1r/pQ2pp2/2pp3n/5bN1/2P2N1p/3P4/PP2PPPP/R1B1KB1R',
'rn2kb1r/pQ2pp2/2pp3n/q4bN1/2P2N1p/3P4/PP2PPPP/R1B1KB1R',
'rn2kb1r/pQ2pp2/2pp3n/q4bN1/2P2N1p/3P4/PP1BPPPP/R3KB1R',
'rn2kb1r/pQ2pp2/2pp3n/5bN1/2P2N1p/3P4/PP1qPPPP/R3KB1R',
'rn2kb1r/pQ2pp2/2pp3n/5bN1/2P2N1p/3P4/PP1KPPPP/R4B1R',
'rn2kb2/pQ2pp1r/2pp3n/5bN1/2P2N1p/3P4/PP1KPPPP/R4B1R',
'Qn2kb2/p3pp1r/2pp3n/5bN1/2P2N1p/3P4/PP1KPPPP/R4B1R',
'Qn2kb2/p3pp1r/2ppb2n/6N1/2P2N1p/3P4/PP1KPPPP/R4B1R',
'1Q2kb2/p3pp1r/2ppb2n/6N1/2P2N1p/3P4/PP1KPPPP/R4B1R',
'1Q3b2/p2kpp1r/2ppb2n/6N1/2P2N1p/3P4/PP1KPPPP/R4B1R',
'5Q2/p2kpp1r/2ppb2n/6N1/2P2N1p/3P4/PP1KPPPP/R4B1R',
'5Q2/p2kpp1r/2pp3n/5bN1/2P2N1p/3P4/PP1KPPPP/R4B1R',
'5Q2/p2kpp1N/2pp3n/5b2/2P2N1p/3P4/PP1KPPPP/R4B1R',
'5Q2/p2kpp1b/2pp3n/8/2P2N1p/3P4/PP1KPPPP/R4B1R',
'8/p2kpp1b/2pp3Q/8/2P2N1p/3P4/PP1KPPPP/R4B1R',
'8/p2kpp2/2pp2bQ/8/2P2N1p/3P4/PP1KPPPP/R4B1R',
'8/p2kpp2/2pp2b1/8/2P2N1Q/3P4/PP1KPPPP/R4B1R',
'4k3/p3pp2/2pp2b1/8/2P2N1Q/3P4/PP1KPPPP/R4B1R',
'4k2Q/p3pp2/2pp2b1/8/2P2N2/3P4/PP1KPPPP/R4B1R',
'7Q/p2kpp2/2pp2b1/8/2P2N2/3P4/PP1KPPPP/R4B1R',
'8/p2kppQ1/2pp2b1/8/2P2N2/3P4/PP1KPPPP/R4B1R',
'8/p2k1pQ1/2pp2b1/4p3/2P2N2/3P4/PP1KPPPP/R4B1R',
'8/p2k1pQ1/2pp2b1/4p3/1PP2N2/3P4/P2KPPPP/R4B1R',
'8/p2k1pQ1/2pp2b1/8/1PP2p2/3P4/P2KPPPP/R4B1R',
'8/p2k1pQ1/2pp2b1/8/1PP2p2/3P2P1/P2KPP1P/R4B1R',
'8/p2k1pQ1/2pp2b1/8/1PP5/3P2p1/P2KPP1P/R4B1R',
'8/p2k1pQ1/2pp2b1/8/1PP5/3P2P1/P2KPP2/R4B1R',
'8/p1k2pQ1/2pp2b1/8/1PP5/3P2P1/P2KPP2/R4B1R',
'8/p1k2pQ1/2pp2b1/8/1PP5/3P2PB/P2KPP2/R6R',
'1k6/p4pQ1/2pp2b1/8/1PP5/3P2PB/P2KPP2/R6R',
'1k3Q2/p4p2/2pp2b1/8/1PP5/3P2PB/P2KPP2/R6R',
'5Q2/p1k2p2/2pp2b1/8/1PP5/3P2PB/P2KPP2/R6R',
'2B2Q2/p1k2p2/2pp2b1/8/1PP5/3P2P1/P2KPP2/R6R',
'2B2Q2/p1k2p2/2pp4/8/1PP5/3b2P1/P2KPP2/R6R',
'2B5/p1k2Q2/2pp4/8/1PP5/3b2P1/P2KPP2/R6R',
'1kB5/p4Q2/2pp4/8/1PP5/3b2P1/P2KPP2/R6R',
'1kB5/pQ6/2pp4/8/1PP5/3b2P1/P2KPP2/R6R'
]
for move in moves:
    moves_que.put(move)

window_thread = threading.Thread(target=create_window)
window_thread.start()

# for move in moves:
#     moves_que.put(move)