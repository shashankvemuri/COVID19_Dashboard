import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk
import numpy as np

#Load and Cache the data
@st.cache(persist=True)
def getmedata():
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    df = pd.read_csv(url, delimiter=',', header='infer')
    df.rename(index=lambda x: df.at[x, 'Country/Region'], inplace=True)
    dft = df.loc[df['Province/State'].isnull()]
    dft = dft.transpose()
    dft = dft.drop(['Province/State', 'Country/Region', 'Lat', 'Long'])
    dft.index = pd.to_datetime(dft.index)
    return(dft, df)
df1 = getmedata()[0]
st.title('COVID-19 Dashboard!')
st.subheader('With up-to-date COVID-19 Data')

#####In Scope Countries
countrylist = df1.columns.tolist()
countrylist1 = ['United Kingdom', 'US', 'Italy']
x = st.multiselect('Choose in scope countries', countrylist, countrylist1)
df1_inscope = df1[x]
dailytotal = st.selectbox('Toggle between Daily and Total number of deaths', ('Daily', 'Total'))

if dailytotal == 'Daily':
    plotdata = df1_inscope.diff() #day on day changes
else:
    plotdata = df1_inscope

#Build Pie Chart
df1 = plotdata.tail(1).transpose()
fig = px.pie(df1, values = str(df1.columns[0]), names = df1.index)
fig.update_traces(textposition='inside', textinfo = 'percent+label')
ddate = str(df1.columns[0])[:10] #chop timestamp

if dailytotal == 'Daily':
    st.header('Number of deaths on ' + ddate)
else:
    st.header('Total number of deaths up until ' + ddate)

fig.update_layout(
    #title = f'Deaths on {ddate} due to COVID-19',
    xaxis_title = 'Dates'
    ,yaxis_title = 'Number of Deaths'
    ,font = dict(size = 25)
    ,template = 'seaborn' #"plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"
)

st.plotly_chart(fig)
piechart = st.sidebar.checkbox('Show Pie Chart data')

if piechart == True:
    st.dataframe(df1)
    st.write()
else:
    st.write()

#Move to Line graph
if dailytotal == 'Daily':
    st.header('Timeseries of daily number of deaths')
else:
    st.header('Timeseries total Number of deaths')
fig = px.line()

for i,n in enumerate(plotdata.columns):
    fig.add_scatter(x=plotdata.index, y= plotdata[plotdata.columns[i]], name= plotdata.columns[i])
fig.update_layout(
     xaxis_title = 'Dates'
    ,yaxis_title = 'Number of Deaths'
    ,template = 'seaborn' #"plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"
    ,legend=dict(orientation="h", yanchor = 'top', y = 1.2)
)
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=7, label="1w", step="day", stepmode="backward"),
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=2, label="2m", step="month", stepmode="backward"),
            dict(step="all")
        ]),
        font = dict( color='#008000', size = 11),
    )
)
st.plotly_chart(fig, use_container_width=True)

##Show underlying data?
showdata = st.sidebar.checkbox('Show Line graph timeseries data')
if showdata == True:
    st.dataframe(plotdata)
else:
    st.write()

###Plot a streamlit map
st.header('Explore the infection spreading with a map')
df2 = getmedata()[1]
df2.rename(columns={'Lat': 'lat', 'Long': 'lon', 'Province/State': 'Province', 'Country/Region': 'Country'}, inplace=True)
maxslide = len(df2.columns) - 5
slide = st.slider('Slide across to explore infection spread', 0, maxslide, 10)
datecolumn = df2.columns[slide + 4]
datecolumnlist = [datecolumn]
st.subheader('Infections Recorded on ' + datecolumn)
dfmap = df2[['Country','Province', 'lat', 'lon', datecolumn]]
dfmap = dfmap.replace(0,np.nan).dropna(subset = [datecolumn, 'lat', 'lon'])
st.map(dfmap[['lat','lon']])
mapgraph = st.sidebar.checkbox('Show map data')

if mapgraph == True:
    st.dataframe(dfmap)
    st.write()
else:
    st.write()