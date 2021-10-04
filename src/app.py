import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from db_connection import get_words
import os

white_button_style = {'background-color': 'white',
                      'color': 'black',
                      'height': '50px',
                      'width': '100px',
                      'margin-top': '50px',
                      'margin-left': '50px'}

red_button_style = {'background-color': 'red',
                    'color': 'white',
                    'height': '50px',
                    'width': '100px',
                    'margin-top': '50px',
                    'margin-left': '50px'}

assets_path = os.getcwd() + '/assets'
app = dash.Dash(__name__, suppress_callback_exceptions=True, assets_folder = assets_path)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div(
className = 'app-header',
    children = [
    html.H1('Hello, welcome to the GRE APP'),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2')])

page_1_layout = html.Div(children = [

    html.H1('Page 1'),

    html.Button(id='button',
                children=['click'],
                n_clicks=0,
                style=white_button_style
                ),
    dcc.Dropdown(
        id='page-1-dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])

@app.callback(Output('button', 'style'), [Input('button', 'n_clicks')])
def change_button_style(n_clicks):
    if n_clicks%2==  0:
        return red_button_style
    else:
        return white_button_style

@app.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    words_list = get_words()
    return words_list + '\n\n You have selected "{}"'.format(value)


page_2_layout = html.Div([
    html.H1('Page 2'),
    dcc.RadioItems(
        id='page-2-radios',
        options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
        value='Orange'
    ),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])

@app.callback(dash.dependencies.Output('page-2-content', 'children'),
              [dash.dependencies.Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True)