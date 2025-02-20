# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Lab Assignment 12: Interactive Visualizations
# ## DS 6001: Practice and Application of Data Science
# **Dominic Scerbo (ybt7qf)**
#
# ### Instructions
# Please answer the following questions as completely as possible using text, code, and the results of code as needed. Format your answers in a Jupyter notebook. To receive full credit, make sure you address every part of the problem, and make sure your document is formatted in a clean and professional way.

# ## Problem 0
# Import the following libraries:

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# For this lab, we will be working with the 2019 General Social Survey one last time.

# %%capture
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

# Here is code that cleans the data and gets it ready to be used for data visualizations:

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

# The `gss_clean` dataframe now contains the following features:
#
# * `id` - a numeric unique ID for each person who responded to the survey
# * `weight` - survey sample weights
# * `sex` - male or female
# * `education` - years of formal education
# * `region` - region of the country where the respondent lives
# * `age` - age
# * `income` - the respondent's personal annual income
# * `job_prestige` - the respondent's occupational prestige score, as measured by the GSS using the methodology described above
# * `mother_job_prestige` - the respondent's mother's occupational prestige score, as measured by the GSS using the methodology described above
# * `father_job_prestige` -the respondent's father's occupational prestige score, as measured by the GSS using the methodology described above
# * `socioeconomic_index` - an index measuring the respondent's socioeconomic status
# * `satjob` - responses to "On the whole, how satisfied are you with the work you do?"
# * `relationship` - agree or disagree with: "A working mother can establish just as warm and secure a relationship with her children as a mother who does not work."
# * `male_breadwinner` - agree or disagree with: "It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family."
# * `men_bettersuited` - agree or disagree with: "Most men are better suited emotionally for politics than are most women."
# * `child_suffer` - agree or disagree with: "A preschool child is likely to suffer if his or her mother works."
# * `men_overwork` - agree or disagree with: "Family life often suffers because men concentrate too much on their work."

# ## Problem 1
# Our goal in this lab is to build a dashboard that presents our findings from the GSS. A dashboard is meant to be shared with an audience, whether that audience is a manager, a client, a potential employer, or the general public. So we need to provide context for our results. One way to provide context is to write text using markdown code.
#
# Find one or two websites that discuss the gender wage gap, and write a short paragraph in markdown code summarizing what these sources tell us. Include hyperlinks to these websites. Then write another short paragraph describing what the GSS is, what the data contain, how it was collected, and/or other information that you think your audience ought to know. A good starting point for information about the GSS is here: http://www.gss.norc.org/About-The-GSS
#
# Then save the text as a Python string so that you can use the markdown code in your dashboard later.
#
# It should go without saying, but no plagiarization! If you summarize a website, make sure you put the summary in your own words. Anything that is copied and pasted from the GSS webpage, Wikipedia, or another website without attribution will receive no credit.
#
# (Don't spend too much time on this, and you might want to skip it during the Zoom session and return to it later so that you can focus on working on code with your classmates.) [1 point]

markdown_text = '''
[This source](https://www.npr.org/2023/03/14/1162776985/equal-pay-day-gender-pay-gap-discrimination)

[This source](https://en.wikipedia.org/wiki/Gender_pay_gap)
'''

markdown_text

# ## Problem 2
# Generate a table that shows the mean income, occupational prestige, socioeconomic index, and years of education for men and for women. Use a function from a `plotly` module to display a web-enabled version of this table. This table is for presentation purposes, so round every column to two decimal places and use more presentable column names. [3 points]

# +
gss_table = gss_clean.groupby('sex').agg({'income':'mean',
                                          'job_prestige': 'mean',
                                          'socioeconomic_index':'mean',
                                          'education':'mean'}).reset_index()

gss_table = gss_table.round({'income': 2, 'job_prestige': 2, 'socioeconomic_index': 2, 'education': 2})

gss_table = gss_table.rename({
    'sex': 'Sex',
    'income': 'Avg. Income',
    'job_prestige': 'Avg. Occupational Prestige',
    'socioeconomic_index': 'Avg. Socioeconomic Idx',
    'education': 'Avg. Years of Education'
}, axis=1)

table = ff.create_table(gss_table)
#table
# -

# ## Problem 3
# Create an interactive barplot that shows the number of men and women who respond with each level of agreement to `male_breadwinner`. Write presentable labels for the x and y-axes, but don't bother with a title because we will be using a subtitle on the dashboard for this graphic. [3 points]

# +
gss_clean['male_breadwinner'] = gss_clean['male_breadwinner'].astype('category')
gss_clean['male_breadwinner'] = gss_clean['male_breadwinner'].cat.reorder_categories(['strongly agree', 
                                                                                      'agree', 
                                                                                      'disagree', 
                                                                                      'strongly disagree'])

gss_groupbar = gss_clean.groupby(['sex', 'male_breadwinner']).size()
gss_groupbar = gss_groupbar.reset_index()
gss_groupbar = gss_groupbar.rename({0:'count'}, axis=1)
#gss_groupbar
# -

fig_3 = px.bar(gss_groupbar, x='male_breadwinner', y='count', color='sex',
            labels={'male_breadwinner':'Male Breadwinner', 'count':'Count'},
            #hover_data = ['', '', ''],
            #text='',
            barmode = 'group')
fig_3.update_layout(showlegend=True)
#fig_3.show()

# ## Problem 4
# Create an interactive scatterplot with `job_prestige` on the x-axis and `income` on the y-axis. Color code the points by `sex` and make sure that the figure includes a legend for these colors. Also include two best-fit lines, one for men and one for women. Finally, include hover data that shows us the values of `education` and `socioeconomic_index` for any point the mouse hovers over. Write presentable labels for the x and y-axes, but don't bother with a title because we will be using a subtitle on the dashboard for this graphic. [3 points]

fig_4 = px.scatter(gss_clean, x='job_prestige', y='income', 
                 color='sex',
                 trendline='lowess',
                 height=600, width=600,
                 labels={'job_prestige':'Occupational Prestige', 
                         'income':'Income'},
                 hover_data=['education', 'socioeconomic_index'])
#fig_4.show()

# ## Problem 5
# Create two interactive box plots: one that shows the distribution of `income` for men and for women, and one that shows the distribution of `job_prestige` for men and for women. Write presentable labels for the axis that contains `income` or `job_prestige` and remove the label for `sex`. Also, turn off the legend. Don't bother with titles because we will be using subtitles on the dashboard for these graphics. [3 points]

fig_5a = px.box(gss_clean, y='income', x = 'sex', color = 'sex',
                labels={'income':'Income', 'sex':''})
fig_5a.update_layout(showlegend=False)
#fig_5a.show()

fig_5b = px.box(gss_clean, y='job_prestige', x = 'sex', color = 'sex',
             labels={'job_prestige':'Occupational Prestige', 'sex':''})
fig_5b.update_layout(showlegend=False)
#fig_5b.show()

# ## Problem 6
# Create a new dataframe that contains only `income`, `sex`, and `job_prestige`. Then create a new feature in this dataframe that breaks `job_prestige` into six categories with equally sized ranges. Finally, drop all rows with any missing values in this dataframe.
#
# Then create a facet grid with three rows and two columns in which each cell contains an interactive box plot comparing the income distributions of men and women for each of these new categories. 
#
# (If you want men to be represented by blue and women by red, you can include `color_discrete_map = {'male':'blue', 'female':'red'}` in your plotting function. Or use different colors if you want!) [3 points]

gss_reduce = gss_clean[['income', 'sex', 'job_prestige']]

min_val = min(gss_reduce['job_prestige'])
max_val = max(gss_reduce['job_prestige'])
num_bins = 6
bins = list(np.arange(min_val, max_val, (max_val-min_val)/(num_bins+1),  dtype=int))
#bins

gss_reduce['job_prestige'] = pd.cut(gss_reduce['job_prestige'], 
                                    bins=bins)

gss_reduce = gss_reduce.dropna()

# +
#gss_reduce['job_prestige']
# -

fig_6 = px.box(gss_reduce, x='sex', y='income', color='sex', 
             facet_col='job_prestige', facet_col_wrap=2,
             color_discrete_map = {'male':'blue', 'female':'red'},
             labels={'sex':'', 'income':'Income'},
             width=1000, height=600)
fig_6.update_layout(showlegend=False)
fig_6.for_each_annotation(lambda a: a.update(text=a.text.replace("job_prestige=", "")))
#fig_6.show()

# ## Problem 7
# Create a dashboard that displays the following elements:
#
# * A descriptive title
#
# * The markdown text you wrote in problem 1
#
# * The table you made in problem 2
#
# * The barplot you made in problem 3
#
# * The scatterplot you made in problem 4
#
# * The two boxplots you made in problem 5 side-by-side
#
# * The faceted boxplots you made in problem 6
#
# * Subtitles for all of the above elements
#
# Use `JupyterDash` to display this dashboard directly in your Jupyter notebook.
#
# Any working dashboard that displays all of the above elements will receive full credit. [4 points]

# +
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H1('Dash GSS Analysis'),
    dcc.Tabs(id="tabs-example-graph", value='tab-1-example-graph', children=[
        dcc.Tab(label='Welcome', value='tab-1-example-graph'),
        dcc.Tab(label='Summary', value='tab-2-example-graph'),
        dcc.Tab(label='Discovery', value='tab-3-example-graph'),
        dcc.Tab(label='Analytics', value='tab-4-example-graph')
    ]),
    html.Div(id='tabs-content-example-graph')
])

@app.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_content(tab):
    if tab == 'tab-1-example-graph':
        return html.Div([
            html.H1("Exploration of the Nationally Representative General Social Survey of Adults in the United States"),
        
            dcc.Markdown(children = markdown_text)            
        ])
    elif tab == 'tab-2-example-graph':
        return html.Div([
            html.H2("Mean Income, Occupational Prestige, Socioeconomic Idx, and Years of Education by Sex"),
        
            dcc.Graph(figure=table)
        ])
    
    elif tab == 'tab-3-example-graph':
        return html.Div([
            html.H2("Survey Responses by Sex"),
        
            html.Div([

                html.H3("Group Feature"),

                dcc.Dropdown(id='group',
                             options=[{'label': i, 'value': i} for i in ['sex', 'region', 'education']],
                             value='sex'),

                html.H3("Category Feature"),

                dcc.Dropdown(id='category',
                             options=[{'label': i, 'value': i} for i in ['satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer', 'men_overwork']],
                             value='male_breadwinner')

            ], style={'width': '25%', 'float': 'left'}),

            html.Div([

                dcc.Graph(id="graph")

            ], style={'width': '70%', 'float': 'right'})
        ])
    
    elif tab == 'tab-4-example-graph':
        return html.Div([
            html.H2("Scatter and Best Line of Fit for Occupational Prestige vs. Income"),
        
            html.Div([

                html.H2("Dist. of Income"),

                dcc.Graph(figure=fig_5a)

            ], style = {'width':'48%', 'float':'left'}),

            html.Div([

                html.H2("Dist. of Occupational Prestige"),

                dcc.Graph(figure=fig_5b)

            ], style = {'width':'48%', 'float':'right'}),

            html.H2("Distribution of Occupational Prestige Groups by Sex"),

            dcc.Graph(figure=fig_6)
        ])
    
@app.callback(Output(component_id="graph",component_property="figure"), 
              [Input(component_id='group',component_property="value"),
              Input(component_id='category',component_property="value")])

def make_figure(group, category):
    gss_groupbar = gss_clean.groupby([group, category]).size()
    gss_groupbar = gss_groupbar.reset_index()
    gss_groupbar = gss_groupbar.rename({0:'count'}, axis=1)
    
    fig = px.bar(gss_groupbar, x=category, y='count', 
                 color=group,
                 barmode = 'group')
    fig.update_layout(showlegend=True)
    return fig

# -

# ## Extra Credit (up to 10 bonus points)
# Dashboards are all about good design, functionality, and accessability. For this extra credit problem, create another version of the dashboard you built for problem 7, but take extra steps to improve the appearance of the dashboard, add user-inputs, and host it on the internet with its own URL.
#
# **Challenge 1**: Be creative and use a layout that significantly departs from the one used for the ANES data in the module 12 notebook. A good place to look for inspiration is the [Dash gallery](https://dash-gallery.plotly.host/Portal/). We will award up to 3 bonus points for creativity, novelty, and style.
#
# **Challenge 2**: Alter the barplot from problem 3 to include user inputs. Create two dropdown menus on the dashboard. The first one should allow a user to display bars for the categories of `satjob`, `relationship`, `male_breadwinner`, `men_bettersuited`, `child_suffer`, or `men_overwork`. The second one should allow a user to group the bars by `sex`, `region`, or `education`. After choosing a feature for the bars and one for the grouping, program the barplot to update automatically to display the user-inputted features. One bonus point will be awarded for a good effort, and 3 bonus points will be awarded for a working user-input barplot in the dashboard.
#
# **Challenge 3**: Follow the steps listed in the module notebook to deploy your dashboard on Heroku. 1 bonus point will be awarded for a Heroku link to an app that isn't working. 4 bonus points will be awarded for a working Heroku link.

if __name__ == '__main__':
    app.run_server(debug=True, port=8051, host='0.0.0.0')
