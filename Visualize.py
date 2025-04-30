import FreeSimpleGUI as sg
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

    window = sg.Window('Chess', layout, icon='Piece-Assets\\P.ico', finalize=True)
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
                time.sleep(1)
            
        if event == 'bottom_color':
            piece_images = generate_pieces(graph, piece_images, values['FEN_input'], values['bottom_color'])

        if event == 'Reset':
            for image in piece_images:
                graph.delete_figure(image)
            in_box.update('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
            piece_images = FEN_to_visual(graph, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR', values['bottom_color'])


    window.close()
