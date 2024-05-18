import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output,callback  # pip install dash (version 2.0.0 or higher)
import dash_bootstrap_components as dbc

df = pd.read_csv("C:\\Users\\Azri\\Python Wasteland\\BAHRAIN GP 2023\\240416FINALSLTBAHRAIN23.csv")
minisecdf = pd.read_csv(r'F:\Python Wasteland\BAHRAIN GP 2023\minisecBahrain23.csv')
speedf = pd.read_csv(r'F:\Python Wasteland\BAHRAIN GP 2023\minisecspeedBahrain23.csv')
app = Dash(external_stylesheets=[dbc.themes.DARKLY])
chartstyle = {'display': 'inline-block',
              'background-color':'rgba(38,50,56,1)',
              'border' :'1px',
              'border-radius':'10px',
              'padding':'0px',
              'margin':'10px'}
app.title = "F1 Bahrain 2023"
app.layout = html.Div(
        className="app-div",
        children=[html.H1(app.title),
                  html.Hr(),
                  html.Div(className = 'Controls',style={
                       'display': 
                      'flex',
                      'justify-content': 'center',
                      'align-items': 'center',
                      'width': '100%'},
                      children = [
                      dcc.Dropdown(
                          id='dropdown',
                          style={'display': 'inline-block'},
                          options=[
                              {'label':i,'value':i} for i in df['Driver'].unique()
                              ],
                              value=df.Driver.unique(),
                              multi=True , 
                              placeholder='Choose Drivers')]),
                    html.Div(id = 'control2',
                        children = [
                            dcc.RangeSlider(
                              id = 'LapSlider',
                              min = df['Laps(?)'].min(),
                              max = df['Laps(?)'].max(),
                              value = [df['Laps(?)'].min(),df['Laps(?)'].max()],
                              step = 1)]),
                    html.Div(className = 'ChartA',style={
                      'display': 
                      'flex',
                      'justify-content': 'center',
                      'align-items': 'center',
                      'width': '100%'},
                      children=[
                      dcc.Graph(id= 'laptime',style=chartstyle),
                      dcc.Graph(id= 'boxplot',style=chartstyle)]),
                     html.Div(className = 'Chart B',style = {
                         'display':
                         'flex',
                         'justify-content': 'center',
                         'align-items': 'center',
                         'width': '100%'},
                        children=[
                         dcc.Graph(id='tyrestrat',style=chartstyle),
                         dcc.Graph(id='minisec',style=chartstyle)])])
app.title = "F1TEST"
@callback(
    Output('laptime', 'figure'),
    Output('boxplot','figure'),
    Output('tyrestrat', 'figure'),
    Output('minisec', 'figure'),
    Input('dropdown', 'value'),
    Input('LapSlider', 'value'))

def update_figure(dropdown,LapSlider):
    tyre_col = {'SOFT':'red',
                'MEDIUM':'yellow',
                'HARD':'white'}
    font_dict = {'color':'white',
                 'family':"Droid Sans",
                 'weight':'bold'}
    bg_dict = {'paper_bgcolor':'rgba(0,0,0,0)',
               'plot_bgcolor':'rgba(0,0,0,0)',
               'title_font':font_dict,
               'font':font_dict}
    newdf = df[(df.Driver.isin(dropdown)) & (df['Laps(?)'] >= LapSlider[0]) & (df['Laps(?)'] <= LapSlider[1])  ]
    boxdf = newdf[(df['Laps(?)'] >= LapSlider[0]) & (df['Laps(?)'] <= LapSlider[1]) & (newdf['PitIn'].isnull() & newdf['PitOut'].isnull()) & (newdf['TrackStat'] == 1)]
    newspf = speedf[speedf['Driver'].isin(dropdown)]
    newspf['Rank'] = newspf.groupby(['Minisector'])['Speed'].rank(ascending=False)
    best_speed = newspf[newspf['Rank']<2]
    plotsec = pd.merge(minisecdf,best_speed,on='Minisector')
    lapfig=px.line(newdf, 
                   x='Laps(?)',
                   y='Smoothed',
                   color='Driver',
                   title = 'Smoothed Lap Times')
    boxfig = px.box(boxdf, x="Driver", y="LapTime",title='Lap Time Distribution',color='red')
    secfig  = px.scatter(plotsec, y="y", x="x", color="Driver",title='Minisector Average Speed')
    secfig.update_xaxes(visible=False)
    secfig.update_yaxes(visible=False)
    tyrestrat = px.scatter(newdf, y='Driver',x='Laps(?)',color = 'Tyres',symbol='Stint',color_discrete_map=tyre_col,title='Tyre Strategy')
    tyrestrat.update_layout(title_font=font_dict,showlegend=False)
    tyrestrat.update_layout(bg_dict)
    boxfig.update_layout(bg_dict)
    secfig.update_layout(bg_dict)
    lapfig.update_layout(bg_dict)

    
    return lapfig,boxfig,tyrestrat,secfig

if __name__ == "__main__":
   app.run(debug=True)