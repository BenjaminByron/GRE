import os
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, MATCH
from db_connection import get_topics, get_words_by_topic
from dash.exceptions import PreventUpdate


assets_path = os.getcwd() + '/assets'
app = dash.Dash(__name__, suppress_callback_exceptions=True, assets_folder = assets_path)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-209615147-1"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'UA-209615147-1');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        <div></div>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <div></div>
    </body>
</html>
'''

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
        children=[html.Div([
                        html.Button(id={'role': 'button', 'index': word},
                                        n_clicks = 0,
                                        children=[str(word)],
                                        style=white_button_style,
                                        className= 'button')
                            ],),
                  html.Div(id={'role': 'card', 'index': word},
                           className='definition'),
                  ],
        className = 'card',
    )
    return card


def generate_basket(topic):
    basket = html.Div(
        children = [html.H1(topic),
                    html.Div(children = [generate_card(i) for i in get_words_by_topic(topic)],
                             className = 'basket'),],)
    return basket


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


index_page = html.Div(
    children = [
    html.Div('testing main.css', className = 'app-header'),
    html.H1('Hello, welcome to the GRE APP'),
    html.Br(),
    dcc.Link('Go to word list', href='/word-list')])


page_1_layout = html.Div(children = [
    html.Br(),
    dcc.Link('Go to word list', href='/word-list'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])


page_2_layout = html.Div([
    html.H1('Word list by Topic'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
    html.Div(children = [generate_basket(i) for i in get_topics()]),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/word-list':
        return page_2_layout
    else:
        return index_page


@app.callback(
     Output({'role': 'card', 'index': MATCH}, 'children'),
     [Input({'role': 'button', 'index': MATCH}, 'n_clicks'),
      Input({'role': 'button', 'index': MATCH}, 'children')],
    prevent_initial_call=True)
def response(n_clicks, children):
    if (n_clicks == 0) :
        raise PreventUpdate
    if (n_clicks%2 != 0) :
        return children
    if (n_clicks%2 == 0) :
        return ''

if __name__ == '__main__':
    app.run_server(debug=True)