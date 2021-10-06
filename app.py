import os
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, MATCH
from db_connection import get_topics, get_words_by_topic

assets_path = os.getcwd() + '/assets'
app = dash.Dash(__name__, suppress_callback_exceptions=True, assets_folder = assets_path)
server = app.server

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

def generate_card(word):
    card = html.Div(
        children=[html.Div(id={'role': 'card', 'index': word},
                           className = 'definition'),
                  html.Div([html.Button(id={'role': 'b', 'index': word},
                            children=[str(word)],
                            n_clicks=0,
                            style=white_button_style,
                            className= 'button')],)
                  ],
        className = 'card',
    )
    return card

def generate_basket(topic):
    basket = html.Div(
        children = [html.H1(topic),
                    html.Div(children =
                             [generate_card(i) for i in get_words_by_topic(topic)], ),],
        className = 'basket')
    return basket

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div(
    children = [
    html.Div('testing main.css', className = 'app-header'),
    html.H1('Hello, welcome to the GRE APP'),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2')])

page_1_layout = html.Div(children = [
    html.H1('Page 1'),
    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])


page_2_layout = html.Div([
    html.H1('Page 2'),
    html.Div(children = [generate_basket(i) for i in get_topics()]),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Go to Page 1', href='/page-1'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
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

@app.callback(
     Output({'role': 'card', 'index': MATCH}, 'children'),
     [Input({'role': 'b', 'index': MATCH}, 'n_clicks'),
      Input({'role': 'b', 'index': MATCH}, 'children')]
)
def response(n_clicks, children):
    if n_clicks == 0:
        return ''
    elif n_clicks%2==  0:
            return children
    else:
        return ''


if __name__ == '__main__':
    app.run_server(debug=True)