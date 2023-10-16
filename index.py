import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import ThemeSwitchAIO


# ========= App ============== #
FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc_css])
app.scripts.config.serve_locally = True
server = app.server

# ========== Styles ============ #

template_theme1 = "flatly"
template_theme2 = "vapor"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.VAPOR
tab_card = {'height':'100%'}

# ===== Reading n cleaning File ====== #
df_main = pd.read_csv("data_gas.csv")
df_main['DATA INICIAL'] = pd.to_datetime(df_main['DATA INICIAL'])
df_main['DATA FINAL'] = pd.to_datetime(df_main['DATA FINAL'])

df_main['DATA MEDIA'] = (df_main['DATA FINAL'] - df_main['DATA INICIAL'])/2 +df_main['DATA INICIAL']
df_main = df_main.sort_values(by='DATA MEDIA', ascending=True)
df_main.rename(columns= {'DATA MEDIA':'DATA', 'PREÇO MÉDIO REVENDA':'VALOR REVENDA'},
               inplace=True)
df_main['ANO'] =df_main['DATA'].dt.year

df_main = df_main[df_main.PRODUTO == "GASOLINA COMUM"].reset_index()
df_main = df_main[['REGIÃO','ESTADO', 'VALOR REVENDA','DATA','ANO']]

df_store = df_main.to_dict()
# =========  Layout  =========== #
app.layout = dbc.Container(children=[
    
    dcc.Store(id='dataset', data=df_store),
    dcc.Store(id='dataset_fixed', data=df_store),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("Análise do Preço dos Combustíveis")
                        ],sm=8),
                        dbc.Col([
                            html.I(className='fa fa-filter', style={'font-size':'200%'})                           
                        ],sm=4,align='center')
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id='theme', themes=[url_theme1,url_theme2]),
                            html.Legend("Fillipe Andrade")
                        ],style={'margin-top':'10px'}),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button(
                            'Acessar Linkedin', href='https://www.linkedin.com/in/fillipe-almeida-89464b53/',
                            target='_blank'
                            )
                        ])
                    ],style={'margin-top':'10px'})
                ])
            ],style=tab_card)
        ])
    ])



], fluid=True, style={'height': '100%'})


# ======== Callbacks ========== #


# Run server
if __name__ == '__main__':
    app.run_server(debug=True)
