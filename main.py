import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# import data
pv = pd.read_csv('fcc-forum-pageviews.csv', parse_dates= ['date'], index_col = 'date')

# clean data
df = pv[(pv['value']>=pv['value'].quantile(0.025)) & (pv['value']<=pv['value'].quantile(0.975))]

def draw_line_plot():

  # draw line plot
  fig, ax = plt.subplots(figsize=(12,5))

  ax.plot(df.index,df['value'],'-r',linewidth=1)

  ax.set_xlabel('Date')
  ax.set_ylabel('Page Views')
  ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

  # save fig
  fig.savefig('line_plot.png')
  return fig


def draw_bar_plot():

  # prepare data for bar plot
  df['month']=df.index.month
  df['year']=df.index.year

  df_bar = df.groupby(['year','month'])['value'].mean()
  df_bar = df_bar.unstack()
  df_bar.fillna(value=0, inplace=True)

  lookup = {1:'January', 2:'February', 3: 'March' , 4: 'April', 5: 'May',
              6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

  df_bar.rename(lookup, axis='columns', inplace=True)

  # draw box plot
  fig = df_bar.plot.bar(legend=True, figsize=(10,7)).figure
  plt.legend(title='Months')
  plt.xlabel('Years')
  plt.ylabel('Average Page Views')

  # save fig
  fig.savefig('bar_plot.png')
  return fig

def draw_box_plot():

  # prepare data for box plots
  df_box = df.copy()
  df_box.reset_index(inplace=True)
  df_box['year'] = [d.year for d in df_box.date]
  df_box['month'] = [d.strftime('%b') for d in df_box.date]

  df_box['month_num'] = df_box['date'].dt.month  
  df_box = df_box.sort_values('month_num')

  # draw box plots using Seaborn
  fig, axes = plt.subplots(nrows = 1, ncols = 2, figsize=(12,5))

  axes[0] = sns.boxplot(x = df_box['year'], y = df_box['value'].astype('int64'), ax = axes[0])
  axes[1] = sns.boxplot(x = df_box['month'], y = df_box['value'].astype('int64'), ax = axes[1])

  axes[0].set_xlabel('Year')
  axes[0].set_ylabel('Value')
  axes[0].set_title('Year-wise Box Plot (Trend)')

  axes[1].set_xlabel('Month')
  axes[1].set_ylabel('Value')
  axes[1].set_title('Month-wise Box Plot (Seasonality)')

  # save fig
  fig.savefig('box_plot.png')
  return fig

draw_line_plot()

draw_bar_plot()

draw_box_plot()