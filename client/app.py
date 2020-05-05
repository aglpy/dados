import dash
import dash_table
from dash_core_components import Interval, Markdown, Input as dccInput
import dash_html_components as html
from dash.dependencies import Input, Output
from data import streamer
import random
from funcs import get_user

dices = ['b', 'r', 'J', 'Q', 'K', 'o']
global its_turn
global dices_thrown
global dices_show
global dices_say
its_turn = False
dices_say = False
dices_thrown = ''
dices_show = ''

def run_server(table, player):
    data = streamer.get_data(table)
    app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
    updater = Interval(id='interval-component', interval=1000, n_intervals=0)

    points_table = html.Div([dash_table.DataTable(
            id='points_table',
            columns=[{"name": 'Jugador', "id": 'player'}, {"name": 'Puntos', "id": 'points'}]
            )],
        style={
                "position":"absolute",
                "height":"95px",
                "top":"20%",
                "left":"2%"
                }
        )
    main_text = html.Div([
        Markdown('Dados', id="main_text", style={"width":"100%", 
                                                "margin-left":"15px", 
                                                "margin-top":"15px", 
                                                "font-weight":"bold", 
                                                "line-height":70, 
                                                "font-size":"60px"}
                )],
                style={
                    "position":"absolute",
                    "height":"95px",
                    "top":"2%",
                    "left":"10%",
                    "width":"80%"
                })
    void_text1 = html.Div([
        Markdown('', id="void_text1")])
    void_text2 = html.Div([
        Markdown('', id="void_text2")])
    void_text3 = html.Div([
        Markdown('', id="void_text3")])
    void_text4 = html.Div([
        Markdown('', id="void_text4")])
    void_text5 = html.Div([
        Markdown('', id="void_text5")])

    say_input = html.Div([
        dccInput(id="say_input", type="text")

    ], style={
                            "position":"absolute",
                            "height":"50px",
                            "bottom":"15%",
                            "left":"65%",
                            "width":"20%"
                        }
    )

    dices_text = html.Div([
        Markdown('', id="dices_text", style={"width":"100%", 
                                                "margin-left":"15px", 
                                                "margin-top":"15px", 
                                                "font-weight":"bold", 
                                                "line-height":70, 
                                                "font-size":"60px"}
                )],
                style={
                    "position":"absolute",
                    "height":"95px",
                    "top":"40%",
                    "left":"40%",
                    "width":"20%"
                })
    show_text = html.Div([
        Markdown('', id="show_text", style={"width":"100%", 
                                                "margin-left":"15px", 
                                                "margin-top":"15px", 
                                                "font-weight":"bold", 
                                                "line-height":70, 
                                                "font-size":"60px"}
                )],
                style={
                    "position":"absolute",
                    "height":"95px",
                    "top":"40%",
                    "left":"70%",
                    "width":"20%"
                })

    button_throw = html.Div([html.Button('Tirar Dados', id='button_throw')],
                        style={
                            "position":"absolute",
                            "height":"50px",
                            "bottom":"5%",
                            "left":"20%",
                            "width":"20%"
                        })
    button_show = html.Div([html.Button('Enseñar un dado', id='button_show')],
                        style={
                            "position":"absolute",
                            "height":"50px",
                            "bottom":"5%",
                            "left":"35%",
                            "width":"20%"
                        })
    button_true = html.Div([html.Button('Me lo creo', id='button_true')],
                        style={
                            "position":"absolute",
                            "height":"50px",
                            "bottom":"5%",
                            "left":"50%",
                            "width":"20%"
                        })
    button_false = html.Div([html.Button('No me lo creo', id='button_false')],
                        style={
                            "position":"absolute",
                            "height":"50px",
                            "bottom":"5%",
                            "left":"65%",
                            "width":"20%"
                        })

    app.layout = html.Div([
            updater,
            points_table,
            main_text,
            dices_text,
            show_text,
            button_throw,
            button_show,
            button_true,
            button_false,
            void_text1,
            void_text2,
            void_text3,
            void_text4,
            void_text5,
            say_input
    ])

    app.title = "Dados"

    @app.callback(
    [
            Output(component_id='points_table', component_property='data'),
            Output(component_id='main_text', component_property='children'),
            Output(component_id='show_text', component_property='children'),
            Output(component_id='dices_text', component_property='children')
        ],
    [Input('interval-component', 'n_intervals')])
    def updater_unified(n_intervals):
        data = streamer.get_data(table)
        return [
            make_table(data),
            write_main_text(data),
            show_dice(data),
            show_dices(data)
        ]


    def make_table(data):
        table_data = []
        for row in data:
            table_data.append({'player':row.get('player'), 'points':int(row.get('points'))})
        return table_data

    def show_dice(data):
        for row in data:
            if row.get('show') in dices:
                return row.get('show')
        return ''

    def show_dices(data):
        global its_turn
        for row in data:
            if its_turn:
                pdices = row.get('dices')
            else:
                pdices = row.get('say')
            if len(pdices) == 3:
                pdices = pdices.split()
                if len(pdices) == 2:
                    a, b = pdices
                    if a in dices and b in dices:
                        return pdices
        return ''

    def write_main_text(data):
        global its_turn
        global dices_thrown
        global dices_show
        global dices_say
        for row in data:
            if row.get('dices') == '0 0':
                if row.get('player') == player:
                    its_turn = True
                    return 'Te toca tirar los dados!'
                else:
                    its_turn = False
                    dices_thrown = ''
                    dices_show = ''
                    dices_say = False
                    return f'Le toca tirar los dados a {row.get("player")}'
        return 'Dados'




    @app.callback(
        Output(component_id='void_text4', component_property='children'),
        [Input('button_show', 'n_clicks')])
    def clicks(n_clicks):
        global its_turn
        global dices_thrown
        global dices_show
        if n_clicks != None and its_turn and dices_thrown and dices_show == '':
            dices_show = random.choice(dices_thrown.split())
            user_data = get_user(data, player)
            user_data['show'] = dices_show
            streamer.send_d(table, user_data)
        return ''


    @app.callback(
        Output(component_id='void_text5', component_property='children'),
        [Input('button_throw', 'n_clicks')])
    def clickb(n_clicks):
        global its_turn
        global dices_thrown
        if n_clicks != None and its_turn and not dices_thrown:
            dices_thrown = f'{random.choice(dices)}  {random.choice(dices)}'
            user_data = get_user(data, player)
            user_data['dices'] = dices_thrown
            user_data['show'] = 'null'
            streamer.send_d(table, user_data)
        return ''

    @app.callback(
        Output(component_id='void_text1', component_property='children'),
        [Input('button_true', 'n_clicks')])
    def clickt(n_clicks):
        data = streamer.get_data(table)
        user_data = get_user(data, player)
        if user_data.get('say') == '?':
            user_data['say'] = 'T'
            streamer.send_d(table, user_data)
        return ''
        
    @app.callback(
        Output(component_id='void_text2', component_property='children'),
        [Input('button_false', 'n_clicks')])
    def clickf(n_clicks):
        data = streamer.get_data(table)
        user_data = get_user(data, player)
        if user_data.get('say') == '?':
            user_data['say'] = 'F'
            streamer.send_d(table, user_data)
        return ''

    @app.callback(
        Output(component_id='void_text3', component_property='children'),
        [Input('say_input', 'value')])
    def inputvalue(value):
        global its_turn
        global dices_thrown
        global dices_say
        if its_turn and dices_thrown and not dices_say:
            if len(value) == 3:
                if len(value.split()) == 2:
                    a, b = value.split()
                    if a in dices and b in dices:
                        data = streamer.get_data(table)
                        user_data = get_user(data, player)
                        user_data['say'] = value
                        dices_say = True
                        streamer.send_d(table, user_data)
        return ''

    app.run_server(debug=False)