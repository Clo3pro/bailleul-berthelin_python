from importlib import import_module

import dash
from dash import dcc
from dash import html,Input, Output, State
from dash import dash_table
import plotly.express as px
import folium
from folium import GeoJsonTooltip
import pandas as pd
import branca
import dash_bootstrap_components as dbc
import geopandas as gdp

from main import CHEMIN_ABSOLU, pourcentage_de_communes_défa_par_dép_selon_range_0_25_50_75_100 as dictRangePourcent

app = dash.Dash(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# command to launch: cloeberthelin$ /usr/local/bin/python3 /Users/cloeberthelin/labo_school/bailleul-berthelin_python/bailleul-berthelin_python/app.py
# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
colors = {
    'background': '#3D0085',
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
"""
df = pd.DataFrame({
	"Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
	"Amount": [4, 1, 2, 2, 4, 5],
	"City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})
fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
"""


dep_list = []
pourcentage_list = []
nb_total_ville = []
nb_communes_defa = []

with open(CHEMIN_ABSOLU + 'pourcent_defavorise.csv', mode='r', encoding='utf8') as f:
    for elem in f:
        dep_list.append([elem.split(',')[0]])
        pourcentage_list.append([elem.split(",")[1].split('\n')[0]])
        nb_total_ville.append([elem.split(",")[2].split('\n')[0]])
        nb_communes_defa.append([elem.split(",")[3].split('\n')[0]])

depTitle = str(dep_list[0])
depTitle = depTitle.split("['")[1].split("']")[0]

pourcenTitle = str(pourcentage_list[0])
pourcenTitle = pourcenTitle.split("['")[1].split("']")[0]

nbtotalTitle = str(nb_total_ville[0])
nbtotalTitle = nbtotalTitle.split("['")[1].split("']")[0]

nbcommTitle = str(nb_communes_defa[0])
nbcommTitle = nbcommTitle.split("['")[1].split("']")[0]


pourcentage_list.pop(0)
dep_list.pop(0)
nb_total_ville.pop(0)
nb_communes_defa.pop(0)
map2Data = pd.read_csv(CHEMIN_ABSOLU+ "pourcent_defavorise.csv")
####################################################################
## Création du dictionnaire de données pour l'affichage du tableau##
####################################################################
data = {depTitle: dep_list, pourcenTitle: pourcentage_list, nbtotalTitle: nb_total_ville, nbcommTitle: nb_communes_defa}
#df = pd.DataFrame(data=data)
tableDf = pd.read_csv("pourcent_defavorise.csv")
vtest = dictRangePourcent()
depContours = "departements.geojson"
####################################################################
#######################Création des cartes #########################
####################################################################

defaData = "location_ville.geojson"
map = folium.Map(location=[45.156891, 0.730795],zoom_start="9")
folium.GeoJson(defaData, name="Communes défavorisées du département le plus touché").add_to(map)
folium.LayerControl().add_to(map)
map.save('cartographie.html')

##bins = data["Pourcentage communes defavorisees"].quantile([0, 0.25, 0.5, 0.75, 1])

map2 = folium.Map(location=[47.998, 1.747],zoom_start="6",scrollWheelZoom=True)
g =folium.Choropleth(
	geo_data=depContours,
    name="Pourcentage de communes défavorisées par département",
    data=map2Data,
    columns=["Departement","Pourcentage communes defavorisees"],
    fill_color="YlOrRd",
	key_on='properties.code',
    fill_opacity=0.7,
    line_opacity=0.2,
	highlight=True,
    legend_name="Communes défavorisées par Département (%)").add_to(map2)
folium.LayerControl().add_to(map2)

map2.save('carto2.html')
####################################################################
############# Création du tableau et affichage en web ##############
####################################################################

"""def generate_table(dataframe, max_rows=50):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ]
    )
    ], className="table tableColor",style={"overflowY": 'auto'}
	)"""
def generate_table(dataframe, max_rows=100):
    
    return dash_table.DataTable(columns=[{'id': c, 'name': c} for c in dataframe.columns],
        data= dataframe.to_dict('records')
        ,
		style_cell={'textAlign': 'center',
		'border': '1px solid grey' },
		style_header={
        'backgroundColor': 'rgb(30, 30, 30)',
        'color': '#7FDBFF',
		'font-size':'18px'
        },
        style_data={
        'backgroundColor': '#666666',
        'color': '#7FDBFF'
        },
        style_table={
            'height': 500,
            'overflowY': 'scroll',
            'width': 'auto'
        }) 


####################################################################
####### Formattage des données et création de l'histogramme ########
####################################################################
df = pd.DataFrame({
    "Pourcentage de communes défavorisées": ['0', '0-25', '25-50', '50-75', '75-100'],
    # "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Nombre de départements": [vtest['0'], vtest['0-25'], vtest['25-50'], vtest['50-75'], vtest['75-100']]
})
fig = px.bar(df, x="Pourcentage de communes défavorisées", y="Nombre de départements", barmode="group")


fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)
####################################################################
###################### Affichage du Dashboard ######################
####################################################################
app.layout = html.Div(style={'backgroundColor': colors['background'],'height':'100% !important'}, className=" m-0 px-3",children=[
    html.H1(
        children='Tableau de bord',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Villes en zone agricole défavorisées', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure=fig
    ),
	html.Div(id="buttonContainer", className="row px-3 text-center space-around flex-sm-row py-3", children=[
    dbc.Button("Tableau pourcentage communes défas par dép",outline=True, color="info",id='btn-pullUp',class_name=' col-3  me-3', n_clicks=0),
	dbc.Button("Carte département le plus touché",outline=True,color="info", id='btn-pullUpMap',class_name='col-3 me-3', n_clicks=0),
	dbc.Button("Carte pourcentage par département",outline=True,color="info", id='btn-pullUpMap2',class_name='col-3 me-3', n_clicks=0)
	]),
    dbc.Collapse(id='DaContainer',is_open=False,className='bigBox row px-3 text-center', children=[ 
        html.H3(id='DaTitle',children='TABLEAU COMMUNES DEFAVORISÉES',className='titleclass col-12'),
        html.Div(id='DaTable',className=' col-10 offset-1 px-3',children=[ generate_table(tableDf)])
	]),
	dbc.Collapse(id="mapContainer",is_open=False,className="mx-2 my-2",children=[
		html.H3(children="CARTOGRAPHIE DU DÉPARTEMENT LE PLUS TOUCHÉ",className='titleclass col-12'),
		html.Iframe(id='map',srcDoc=open("cartographie.html",'r').read(),className="px-1",width='100%',height='500')
	]),
	dbc.Collapse(id="map2Container",is_open=False,className="mx-2 my-2",children=[
		html.H3(children="CARTOGRAPHIE DU POURCENTAGE DE COMMUNES DÉFAVORISÉES PAR DÉPARTEMENT",className='titleclass col-12'),
		html.Iframe(id='map2',srcDoc=open("carto2.html",'r').read(),className="px-1",width='100%',height='600')
	])
	
])


####################################################################
######## Fonctions pour afficher les différents composants #########
####################################################################
@app.callback(
    
	Output("DaContainer", "is_open"),
    [Input("btn-pullUp", "n_clicks")],
    [State("DaContainer", "is_open")],
)


def displayTable(n, is_open):
    if n:
        return not is_open
    return is_open
    

@app.callback(
    
	Output("mapContainer", "is_open"),
    [Input("btn-pullUpMap", "n_clicks")],
    [State("mapContainer", "is_open")],
)


def displayMap(n, is_open):
    if n:
        return not is_open
    return is_open
    
@app.callback(
    
	Output("map2Container", "is_open"),
    [Input("btn-pullUpMap2", "n_clicks")],
    [State("map2Container", "is_open")],
)


def displayMap(n, is_open):
    if n:
        return not is_open
    return is_open
   


if __name__ == '__main__':
    app.run_server(debug=True)
