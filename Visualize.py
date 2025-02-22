import PySimpleGUI as sg

def draw_board(graph):
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 != 0:
                c ='white'
            else:
                c = 'green'
            graph.DrawRectangle((i*100, j*100), (i*100+100, j*100+100), fill_color=c)


def FEN_to_visual(graph, FEN):
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
            images.append(graph.draw_image(filename=file_name, location=(col * 100 + 20, 780 - row * 100)))

    return images



# All the stuff inside your window.
layout =     [
    [
        sg.Graph(
            canvas_size=(800, 800),
            graph_bottom_left=(0, 0),
            graph_top_right=(800, 800),
            key="graph"
        )
    ],
    [sg.Text("FEN:", font=("Calibri", 24))],
    [sg.Input(default_text='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR', font=("Calibri", 16), key='input')],
    [[sg.Button('Generate', size=(15,3), key='Generate'), sg.Button('Reset', size=(15,3), key='Reset')]]
]
window = sg.Window('Graph test', layout, finalize=True)       
graph = window['graph'] 
in_box = window['input']

draw_board(graph)
piece_images = FEN_to_visual(graph, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')


# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED:
        break

    if event == 'Generate':
        for image in piece_images:
            graph.delete_figure(image)
        piece_images = FEN_to_visual(graph, values['input'])
    
    if event == 'Reset':
        for image in piece_images:
            graph.delete_figure(image)
        in_box.text='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        piece_images = FEN_to_visual(graph, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')


window.close()


