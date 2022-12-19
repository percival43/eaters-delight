import pandas as pd
import plotly.graph_objs as go
import plotly.offline as pyo
from dash import html,dcc,Input,Output
import dash_bootstrap_components as dbc
import dash
from sqlalchemy import create_engine
from datetime import date

cnx = create_engine("postgresql://aguoqrsawiamxj:e836be1bac3bd822f2664d2de84591d4054d21814491fa892095c8326e317479@ec2-52-7-228-45.compute-1.amazonaws.com:5432/d2hf22v709ttic")
conn = cnx.connect()
query = f"""select uce.user_id, sum(uce.gmv) gmv, count(order_id) count from user_campaign_enrollment uce
             where uce.timeframe >= '2022-01-01'
             and uce.timeframe < '2022-12-31'
             group by user_id
             order by 3 desc"""

df = pd.read_sql(sql=query, con=conn)
conn.close()
cnx.dispose()

data = [go.Table(header=dict(values=["მომხმარებლის ID",'GMV (ევროში)','შეკვეთების რაოდენობა'],
                             fill_color='rgb(52,209,134)'),
                 cells=dict(values=[df['user_id'],df['gmv'].round(decimals=0),df['count']]))]
fig = go.Figure(data=data)



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = html.Div(children=[dbc.Row(dbc.NavbarSimple([
                                        html.A(
                                            dbc.Row(
                                                [
                                                    dbc.Col(html.Img(src = 'https://uploads-ssl.webflow.com/61956aa45070a274968848cc/61956aa45070a278e48849fa_3%20Bolt%20Food.png',height='25px')),

                                                ]
                                            )
                                        )
],
    brand="ახალი ითერის დადელაითების დროა",
    color= 'rgb(46,184,117)'

)),                             html.Br(),
                                html.H1("ამოირჩიე თარიღი:",style=dict(marginLeft="89px",fontSize="20px")),
                                dbc.Row([dbc.Col(dcc.DatePickerRange(
                                    id = "date_range_picker",
                                    month_format='MMM Do, YY',
                                    start_date_placeholder_text="საიდან",
                                    end_date_placeholder_text='სადამდე',
                                    start_date=date(2022,1,1),
                                    end_date=date(2022,12,31),
                                    clearable=True,
                                    style=dict(marginLeft="85px")
                                ))]),
                                dbc.Row(dcc.Graph(id="user_overview",figure=fig,style=dict(responsive=True)))])

@app.callback(Output('user_overview','figure'),
             [Input('date_range_picker',"start_date"),
             Input('date_range_picker','end_date')])
def update_graph(start_date,end_date):
    cnx = create_engine("postgresql://aguoqrsawiamxj:e836be1bac3bd822f2664d2de84591d4054d21814491fa892095c8326e317479@ec2-52-7-228-45.compute-1.amazonaws.com:5432/d2hf22v709ttic")
    conn = cnx.connect()
    query = f"""select uce.user_id, sum(uce.gmv) gmv, count(order_id) count from user_campaign_enrollment uce
             where uce.timeframe >= '{start_date}'
             and uce.timeframe < '{end_date}'
             group by user_id
             order by 3 desc"""

    df = pd.read_sql(sql=query, con=conn)
    conn.close()
    cnx.dispose()

    data = [go.Table(header=dict(values=["მომხმარებლის ID",'GMV (ევროში)','შეკვეთების რაოდენობა'],
                                 fill_color='rgb(52,209,134)'
                                 ),
                 cells=dict(values=[df['user_id'],df['gmv'].round(decimals=0),df['count']]))]
    fig = go.Figure(data=data)
    return fig



if __name__ == "__main__":
    app.run_server(port=8055)
