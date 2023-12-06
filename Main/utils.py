import ScraperFC as sfc
import traceback
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np 


######################### Scraping & Data ##################################
def scrape(year, league):
    scraper = sfc.FBRef() # initialize the FBRef scraper
    try:
        # scrape the table
        all_stats = scraper.scrape_all_stats(year=year, league=league, normalize=True)
    except:
        traceback.print_exc()
    scraper.close()
    return all_stats

'''
Dictionary Keys for Scraper
=============================
['standard', 'goalkeeping', 
'advanced goalkeeping', 'shooting', 
'passing', 'pass types', 
'goal and shot creation', 'defensive', 
'possession', 'playing time',
 'misc']
'''
def get_data(stat, year, league,position):
    x=scrape(year, league).get(stat)[2]
    file_name = './Data/{}_{}_{}_df.csv'.format(stat,year,position)
    x.to_csv(file_name)
    read_x = pd.read_csv(file_name,header=1, index_col=0) 
    return read_x 

#'FW','MF', 'DF'
def filter_position(df,position):
    forwards = df.loc[df[ 'Pos']==position].reset_index(drop=True)
    return forwards

################################# Clustering #################################
def get_cluster(df,x, num_clusters):
    x = x.fillna(0)
    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    kmeans.fit(x)
    df['Cluster'] = kmeans.labels_
    return df

def cluster_stats(cluster_name):
     return cluster_name.cluster_centers_, cluster_name.labels_,cluster_name.inertia_, cluster_name.n_features_in, cluster_name.n_iter

def cluster_plot(df, plot_against):
     ##PLOT
    plt.plot(df['Cluster'],df[plot_against],'ro')
    plt.xlim(left=-0.2)
    plt.ylim(top=max(plot_against)+2)


#################### Stats - Feature engineering ###########################
def fullNinety_stats(df,stat):
    df[f'{stat}_90total']= np.round(df['90s']*df[stat])

def get_mins(df, col):
        df['Mins'] = 90*df[col]
        return 90*df[col]



#FUNCTION TO SET ALL DATATYPES TO NUMREIC



