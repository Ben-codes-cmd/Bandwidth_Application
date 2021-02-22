# Ben Jordan
# 2/21/2021

import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import os

# FUNCTION DEFINITIONS


def get_dataset():
    while True:
        file = input('What file/path would you like to view data from?: ').strip().rstrip('.csv') + '.csv'
        if os.path.exists(file):
            return file
        else:
            print(f'The file/path that you have chosen does not exist. Please try again. ({file})')


def newDataFrame(title):
    """creates a new dataframe given the CSV contents"""
    return pd.read_csv(title)


def terminate(event):
    # when button clicked
    print('Your session has successfully terminated. Thank you!')
    quit()


def displayGraph(df):
    """Display a seaborn graph that sources from the dataframe"""
    # set style attributes
    plt.style.use('dark_background')
    plt.title("Bandwidth")

    # draw line
    sb.lineplot(data=df, x="Hour", y="Throughput (Megabytes)", hue="Type", palette="crest")

    # quit button
    quit_button = Button(plt.axes([0.9, 0.015, 0.090, 0.075]), 'Quit', color='#5c5959')
    quit_button.on_clicked(terminate)

    plt.show()

# PROGRAM LOGIC


title = get_dataset()
df = newDataFrame(title)
displayGraph(df)
