import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, State
import pickle
import subprocess

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
                                        "font-family": "Lucida Console",})                                        

])


# --------------------------------------------------------- #
# --------------------------------------------------------- #
# --------------------------------------------------------- #


@app.callback(
    Output('emoji_output', 'children'),
    [Input('input_text', 'value'),
    Input('method-dropdown', 'value')
    ]
)
def update_output(value,option):
    cmd = ['python', 'translator.py']
    cmd.append(value)
    cmd.append(option)
    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    outputs = ""
    for line in p.stdout.readlines():
        outputs += line.decode("utf-8") 
        # outputs.append(line)
    print(outputs)


    return ("In emoji world, you say: \n \n" + outputs)


# --------------------------------------------------------- #
# --------------------------------------------------------- #
# --------------------------------------------------------- #


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8900)