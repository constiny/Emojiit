import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, State
import pickle
import subprocess
import ast

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# model = pickle.load(open('src/final_model.pkl', 'rb'))

# --------------------------------------------------------- #
# --------------------------------------------------------- #

# App layout
app.layout = html.Div([
    html.H1('Emoji Translator 😀🕵️📙', style={'color': "black",
                                             "background-color": "aqua",
                                             "border": "3px solid",
                                             "border-color": "light blue",
                                             "padding": "40px",
                                            "font-size": "54px",
                                            "font-family": "Lucida Console",
                                            "text-align": "center" ,
                                            }),
    html.H2('Author✍️: Vince Pan👨‍🔬', style={'color': "black",
                                            "padding": "10px",
                                            "font-size": "30px",
                                            "font-family": "Lucida Console",
                                            "text-align": "right" ,
                                            }), 
    html.Div('Type in ⌨️ or Paste 📋 below🔽', style={'color': "black",
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
    html.Div(id='emoji_output', style={'whiteSpace': 'pre-line',
                                        "padding": "10px",
                                        'color': "black",
                                        "font-size": "20px",
                                        "font-family": "Lucida Console",}),
    html.Div('Unsatisfied with the translation? Report it.',
                style={"padding": "10px"}),
    html.Button('Report', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
            children='Enter a value and press submit',
            style={"padding": "10px"}),
    dcc.RadioItems(
        id='intermediate-value'
    ),                                       

])


# --------------------------------------------------------- #
@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')])
def update_output(n_clicks):
    if n_clicks > 0:
        return "Please pick the translation you suggest to change."
    else:
        return ""
# --------------------------------------------------------- #
# --------------------------------------------------------- #


@app.callback(

    [Output('emoji_output', 'children'),
     Output('intermediate-value', 'options')],

    [Input('input_text', 'value'),
    Input('method-dropdown', 'value'),
    Input('submit-val', 'n_clicks')
    ]
)
def update_output(value, option, n_clicks):
    cmd = ['python', 'translator.py']
    cmd.append(value)
    cmd.append(option)
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    outputs = ""
    p_out = p.stdout.readlines()
    for line in p_out[:-1]:
        outputs += line.decode("utf-8") 
    s1 = ("In emoji world, you say: \n \n" + outputs)
    d = ast.literal_eval(p_out[-1].decode("utf-8"))
    opt = []
    # print(d)
    # print(type(d))
    if n_clicks > 0:
        for k, v in d.items():
            transl = f"{k} - {v}"
            d2 = {'label': transl, 'value': transl}
            opt.append(d2)


    return s1, opt


# --------------------------------------------------------- #
# --------------------------------------------------------- #
# --------------------------------------------------------- #


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8900)