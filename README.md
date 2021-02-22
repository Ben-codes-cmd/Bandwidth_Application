# Bandwidth_Application
Track your machine's network throughput with a real time graph displaying bytes sent and received.
## Program Features and Specifics
This project utilizes python modules such as:
- psutil - a handy system utility module to retrieve system bandwidth information
- seaborn (built and customized with matplotlib) for graphing
- tkinter provides a clean, interactive graphical user interface
- the Python csv library allows for long term data storage
- pandas converts csv files into convenient dataframes for graphing lines

This program covers exception handling and formatting for elements requiring user input.  
Within the graphing window, I have incorporated a responsive button to terminate the program.  
  
As my largest python script yet, I worked to make the function definitions as modular and readable as possible to make for easy debugging.  

## HOW TO USE
- Upon downloading the zipped file linked in the repository, extract and view the contents of the folder. 
- If you only wish to view the functioning program but not modify the code, an executable file is included that has all necessary dependencies embedded. Simply click, and experience the program. 
- If you wish to make changes to the code, you will want to make sure that all of the following dependencies are installed on your machine.
  - psutil
  - pandas
  - seaborn
  - matplotlib
  - tkinter  
All of these modules are installable at the command line using pip install.  
  
By default, data points are periodically collected every 10 minutes. To customize this, change the data_frequency variable in the  
'PROGRAM LOGIC' section. This variable takes in a number of seconds between each point.  
  
- To start a new session, choose the 'Bandwidth Application' file and run it at the command line in the python environment  
 
- To open an existing dataset, choose the 'Graph_Opener' file and run it at the command line in the python environment 
