# Ben Jordan
# Bandwidth Monitor Application
# 2/5/21
import psutil
import time
import csv
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import _tkinter
import os
import warnings

warnings.filterwarnings("ignore", category=plt.cbook.mplDeprecation)
# seaborn dependencies
# pandas (dataframes)
# matplotlib

# DATA RETRIEVAL


def bandwidth():
    """Retrieve the number of bytes that have been sent and received"""
    # grab system info
    info = psutil.net_io_counters()
    # mb of bandwidth received and sent (bytes> kilobytes> megabytes)
    return info.bytes_sent/(1024 ** 2), info.bytes_recv/(1024 ** 2)


def getTime():
    """Get the current hour with fractions"""
    current_time = time.localtime()
    timeval = current_time.tm_hour + (current_time.tm_min * (1/60) + current_time.tm_sec * (1/60/60))
    timeval = round(timeval, 4)
    return timeval


class newPoint:
    """Formulate a new set of data points"""
    def __init__(self):
        self.hour = getTime()
        self.upload, self.download = bandwidth()

    def newEntry(self, old_upload, old_download):
        """Format for CSV entry"""
        return [f'"Upload", {self.upload - old_upload}, {self.hour}\n',
                f'"Download", {self.download - old_download}, {self.hour}\n']


# FILE CONTROL
def unacceptable_naming(title):
    unacceptable = list('/*?”<>|')
    new_title = list(title)
    changes = False
    for i in range(len(new_title)):
        if new_title[i] in unacceptable:
            new_title[i] = '_'
            changes = True
    return ''.join(new_title), changes


def nameCSV():
    """Receive user input for naming the file"""
    while True:
        # get title and strip spaces
        title = input('What would you like to name your CSV file?: ').strip()
        # check if user filled .csv (otherwise, make sure to add it)
        title = title.rstrip('.csv') + '.csv'
        # double check with file name
        while True:
            response = input(f"Are you sure that you want to name your file '{title}'?[Y/N]")
            if response.upper() == 'Y':
                # check for unacceptable characters
                check = unacceptable_naming(title)
                if check[1]:
                    print(f'Your file name contained illegal characters and has been renamed to the following: '
                          f'{check[0]}')
                # notify before overriding
                if os.path.exists(check[0]):
                    while True:
                        cont = input(
                            'The file that you are about to create will override an existing file. Are you sure that'
                            ' you would like to continue?[Y/N]:')
                        if cont.upper() == 'Y':
                            return check[0]
                        elif cont.upper() == 'N':
                            break
                        else:
                            print(f"'{response}' is an invalid input. Please type Y or N.")
                    break
                else:
                    return check[0]
            elif response.upper() == 'N':
                break
            else:
                print(f"'{response}' is an invalid input. Please type Y or N.")
                pass


def writeCSV(title):
    """Write a CSV to log data to"""
    with open(title, 'w', newline='') as file_to_output:
        csv_writer = csv.writer(file_to_output, delimiter=',')
        csv_writer.writerow(['Type', "Throughput (Megabytes)", 'Hour'])
        file_to_output.close()


def appendCSV(title, new_point):
    """Append new data points to the established CSV"""
    upload = new_point[0]
    download = new_point[1]
    with open(title, 'a') as file_to_open:
        file_to_open.write(upload)
        file_to_open.write(download)


def init():
    filename = nameCSV()
    writeCSV(filename)
    print('.\n.\n.\n.\nYour session has started.\nPlease refrain from opening the csv document where data is being'
          ' stored until the program has terminated. \nWhen you are ready to stop gathering'
          ' data points, click the quit button on the graphing window.')
    return filename


def record_point():
    """get a new point instance and append to the csv; output new currents."""
    fresh_data = newPoint()
    appendCSV(title, fresh_data.newEntry(current_upload, current_download))
    # update currents
    return fresh_data.upload, fresh_data.download


def terminate(event):
    global session
    print('Your session will end after the next data point is collected.')
    session = False

# VISUALIZATION


def newDataFrame(title):
    """creates a new dataframe given the CSV contents"""
    return pd.read_csv(title)


def displayGraph(df, freq):
    """Display a seaborn graph that sources from the dataframe"""
    # SET STYLE ATTRIBUTES
    plt.style.use('dark_background')
    # set title
    plt.title("Bandwidth")
    # allow graph to scale to fit max x and y values
    plt.autoscale(enable=True, axis='both')
    # CREATE AND DRAW LINE
    sb.lineplot(data=df, x="Hour", y="Throughput (Megabytes)", hue="Type", palette="crest", ax=plt.axes())

    '''
    Create a dictionary with the labels as the keys and the handles as the new updated line. 
    This makes it so that each line only has one entry in the legend.
    '''
    # retrieve the handles (line objects) and labels (the label from the hue column - "Type") of the current axes
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    # format the legend so that the labels match the lines
    plt.legend(by_label.values(), by_label.keys())

    # draw once, but don't block execution
    plt.draw()

    # quit button
    quit_button = Button(plt.axes([0.9, 0.015, 0.090, 0.075]), 'Quit', color='#5c5959')
    quit_button.on_clicked(terminate)
    # set axes back to the main graph
    plt.axes()
    # Avoid from stopping program when graph window closed
    try:
        # pause (not time.sleep()) as to keep the graph window responding
        plt.pause(freq)
    except _tkinter.TclError:
        pass


# PROGRAM LOGIC

title = init()
session = True
current_upload, current_download = bandwidth()
dataFrequency = 10 * 60  # 10 minutes - number of seconds between each point (CHANGE IF NEEDED)
while session:
    current_upload, current_download = record_point()
    df = newDataFrame(title)
    displayGraph(df, dataFrequency)
print(f'Your session has ended. Refer to the csv file titled "{title}" in this directory (unless otherwise specified)'
      f' for long term data records. Thank You!')
