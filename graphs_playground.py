import pandas as pd
import plotly as py
import plotly.graph_objs as go

df = pd.read_csv('data/eslagunanegra_pages_full.csv', delimiter=';', quotechar='|')
df['timestamp']=pd.to_datetime(df['timestamp'],format='%Y-%m-%dT%H:%M:%SZ')
df.set_index(df['timestamp'], inplace=True)
print(df.info())

monthly = df.groupby(pd.Grouper(key='timestamp',freq='M'))
edites_pages_monthly = monthly.page_id.count()


trace = go.Scatter(
    x=edites_pages_monthly.index,
    y=edites_pages_monthly.data,
    name = "Edited pages",
    line = dict(color = '#17BECF'),
    opacity = 0.8)

data = [trace]

layout = dict(
    title='Time Series with Rangeslider',
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
py.offline.plot(fig, filename = "Time Series with Rangeslider.html")
