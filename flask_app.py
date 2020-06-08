import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, State
import pickle
import subprocess
import ast
import psycopg2
from psycopg2 import sql
from datetime import datetime
from src.pw import pw

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# --------------------------------------------------------- #
status = 0
# --------------------------------------------------------- #

# App layout
app.layout = html.Div([

    html.H1('Emoji Translator 😀🕵️📙', style={'background': "linear-gradient(45deg, blueviolet, crimson)",
                                                "height": "100px",
                                                "color": "#fff",
                                                "padding": "8px",
                                                "padding-bottom": "20px",
                                                "display": "flex",
                                                "flex-direction": "column",
                                                "justify-content": "center",
                                                "text-align": "center",
                                                "position": "relative",
                                                "overflow": "hidden"
                                            }),
    html.H2('Author✍️: Vince Pan👨‍🔬', style={'color': "black",
                                            "padding": "10px",
                                            "font-size": "30px",
                                            "font-family": "Lucida Console",
                                            "text-align": "right" ,
                                            }), 
    html.Div('Type in ⌨️ or Paste 📋 below🔽:', style={'color': "black",
                                                    "padding": "10px",
                                                    "font-size": "20px",
                                                    "font-family": "Lucida Console",
                                                    "text-align": "left" ,
                                                    'width': '60%', 
                                                    'display': 'inline-block'}), #notice style variable which wants a dict of CSS
    html.Div(dcc.Dropdown(
                        id='method-dropdown',
                        options=[
                            {'label': 'Method for unpredictable word: (Default) Keep', 'value': 'K'},
                            {'label': 'Remove', 'value': 'R'},
                            {'label': 'Keep placeholder', 'value': 'H'},
                        ],
                        placeholder="Method for unpredictable word: Keep",
                        value='K'
                        ) ,
             style={'width': '30%',
                    "padding": "10px",
                    'display': 'inline-block',
                    "text-align": "center"}), 

    dcc.Textarea(
                    id='input_text',
                    value='Head, shoulders, knees and toes',
                    style={'width': '100%', 'height': 200},
                ),
    
    html.Div( "In emoji world🌎, you say 🗣️ :", style={'whiteSpace': 'pre-line',
                                        "padding": "10px",
                                        'color': "black",
                                        "font-size": "20px",
                                        "font-family": "Lucida Console",}),
    dcc.Textarea(
                    id='emoji_output',
                    style={'width': '100%',
                         'height': 200,
                         'disabled' : False,}
                ),

    html.Div('Unsatisfied with the translation? Report it.',
                style={"padding": "10px"}),
    html.Button('Report', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
            children='Enter a value and press submit',
            style={"padding": "10px"}),
    dcc.Checklist(id='intermediate-value'), 
    html.Button('Confirm submission', id='confirm-val', n_clicks=0, style={"padding": "10px"}),
    html.Div(id='output-aftersubmission', style={"padding": "10px"}),
    html.Div('Wanna see more works from Vince Pan. Go to https://constiny.github.io/', style = {"padding": "50px",})
])


# --------------------------------------------------------- #



@app.callback(

    [Output('emoji_output', 'value'),
     Output('intermediate-value', 'options')],

    [Input('input_text', 'value'),
    Input('method-dropdown', 'value'),
    Input('submit-val', 'n_clicks')
    ]
)
def update_output(value, option, n_clicks):
    # load the translator.py with subprocess and return text translation and translated pairs
    cmd = ['python', 'translator.py']
    cmd.append(value)
    cmd.append(option)
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    outputs = ""
    p_out = p.stdout.readlines()
    for line in p_out[:-1]:
        outputs += line.decode("utf-8") 
    s1 = ("\n" + outputs)
    d = ast.literal_eval(p_out[-1].decode("utf-8"))
    opt = []

    if n_clicks > 0:
        for k, v in d.items():
            transl = f"{k} - {v}"
            d2 = {'label': transl, 'value': transl}
            opt.append(d2)
    print(n_clicks)

    return s1, opt


# --------------------------------------------------------- #
@app.callback(
    [Output('container-button-basic', 'children'),
    Output('confirm-val', 'style'),
    Output('output-aftersubmission', 'style')],
    [Input('submit-val', 'n_clicks')])
def show_content_for_report(n_clicks):
    # show the content suggest pick an option and confirm button
    
    if n_clicks > 0:
        status = 1
        return "Please pick the translation you suggest to change.", {'display': 'block'}, {'display': 'block'}
    else:
        return "", {'display': 'none'}, {'display': 'none'}
# --------------------------------------------------------- #

@app.callback(
    Output('output-aftersubmission', 'children'),
    [Input('confirm-val', 'n_clicks'),
    Input('intermediate-value', 'value')]
)
def thanks_for_feedback(n_clicks, value):
    if n_clicks == 1:
        print(value[0].split(" - "))
        print(type(value))
        conn = psycopg2.connect(dbname='emoji_translator', user='postgres', host='localhost', password=pw)
        for pair in value:
            c = conn.cursor()
            now = datetime.now()
            c.execute(
                sql.SQL("insert into user_fb values (%s, %s, %s)"),
                [pair.split(" - ")[1], pair.split(" - ")[0], now])
            conn.commit()
        conn.close()
        return "Thank you for your advices."
    elif n_clicks > 1:
        return "Your advise is recorded. Please don't over submit."
    else:
        return ""

# --------------------------------------------------------- #
# --------------------------------------------------------- #


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8901)