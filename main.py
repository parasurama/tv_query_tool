import pandas as pd
import numpy as np
from bokeh.plotting import *
from bokeh.models import ColumnDataSource, HoverTool, HBox, VBoxForm, Span
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.io import curdoc


# load dataset
df = pd.read_pickle('shows_df.pkl')

network_list = sorted(list(set([df['networks'][i][0]['name'] for i in df.index if len(df.networks[i]) > 0])))

# get column of list of genre names from list of dicts


def get_values(list):
    values = str([list[i]['name'] for i in range(0,len(list))]).strip("[]")
    return values

df['genre_list'] = df['genres'].map(get_values)
df['keyword_list'] = df['keywords'].map(get_values)
df['network_list'] = df['networks'].map(get_values)

df.fillna(np.nan, inplace=True)

# controls
votes = Slider(title="Minimum number of votes", value=0, start=5, end=df['vote_count'].max(), step=10)
rating = Slider(title="Minimum average rating", value=0.0, start=0.0, end=df['vote_average'].max(), step=0.5)
status = Select(title='Show Status', options=['All', 'Ended', 'Returning Series', 'Canceled', 'In Production', 'Planned'], value='All')
#show_type = Select(title='Show Type', options=['All', 'Reality', 'Documentary', 'Talk Show', 'Scripted'], value='All')
genre = Select(title='Genre', options=list(pd.read_pickle('genres.pkl')), value='All')
keyword = TextInput(title='Plot Keywords')
network = Select(title="Select Network", options=list(pd.read_pickle('networks.pkl')), value='All')


# initialize data source for bokeh
source1 = ColumnDataSource(data=dict(x=[], y=[], title=[], ym=[1, 1], x2=[10,600]))

hover = HoverTool(tooltips=[
    ("Title","@title"),
    ("Avg Rating", "@y"),
    ("Number of Votes", "@x")])

# initialize figure for bokeh
p = Figure(plot_height=600, plot_width=600,
           title="TV Show Ratings",
           x_axis_label='Vote Count',
           y_axis_label='Average Vote',
           toolbar_location=None,
           tools=[hover])

p.circle(x="x", y="y", source=source1, size=8, line_color=None, fill_alpha=0.7)
p.line(x="x2", y='ym', source=source1, color = "orange", legend='Average Rating for Selected Data', line_width=3)


def subset_shows():
    subset = df[(df.vote_count >= votes.value) & (df.vote_average >= rating.value)]

    if status.value != 'All':
        subset = subset[subset.status == status.value]

    #if show_type.value != 'All':
     #   subset = subset[subset.type == show_type.value]

    if genre.value != 'All':
        subset = subset[subset.genre_list.str.contains(genre.value)]

    if network.value != 'All':
        subset = subset[subset.network_list.str.contains(network.value)]

    if keyword.value.strip() != '':
        if any(subset.keyword_list.str.contains(keyword.value.strip())) == False:
            subset = subset[subset['name'] == 'No Valid Shows']
        else:
            subset = subset[subset.keyword_list.str.contains(keyword.value.strip())]
    return subset


def update(attrname, old, new):
    df2 = subset_shows()
    if len(df2) > 0:
        source1.data = dict(x=df2['vote_count'],
                            y=df2['vote_average'],
                            title=df2['name'],
                            ym=[df2['vote_average'].mean(), df2['vote_average'].mean()],
                            x2=[df2['vote_count'].min()-2,df2['vote_count'].max()])
    else:
        source1.data = dict(x=df2['vote_count'],
                            y=df2['vote_average'],
                            title=df2['name'],
                            ym=[0,0],
                            x2=[0, 0])

controls = [votes, rating, status, network, genre, keyword]
for control in controls:
    control.on_change('value', update)

inputs = HBox(VBoxForm(*controls), width=300)

update(None, None, None) # initial load of the data
curdoc().add_root(HBox(inputs, p, width=1100))

