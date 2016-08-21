# GanttMaker
Uses Plotly software to make basic Gantt Chart from csv file but allowing for repeated tasks.

After my boss asked me to make a Gantt Chart of some data, I figured it would be easy to find
software to build the graph from a CSV file. While there are a lot of resources for making
Gantt charts online, none of the ones I could find seemed to allow for repeated tasks. Using
Plotly I was able to make a work-around that involves making horizontal stacked bar charts 
instead of the normal Gantt chart option, which does not allow repeated tasks.

How to run:
First you will need to set up an account with Plotly. I've only used it for a little bit now
but from what I've seen it is very useful and simple to get started. Instructions for getting
Plotly up and running for you can be found here: https://plot.ly/python/getting-started/. After
that, all you need is a Python interpreter and you should be good to go. 

Now you must set up the csv file with the input schedule. The first column of the file should
contain the names of each of the tasks (some of them repeated, of course). The second and third
columns should have the start and end times of the event, respectively. The format for these
dates should be as follows: 'YYYY-MM-DD hh-mm-ss' (example: '2016-08-21 18:04:09'). Note the use 
of the 24 hour clock. Also be aware that this will not work for any times before Jan. 1, 1970.

When you run the script you must provide the following command-line arguments: 
name-of-the-csv-file what-to-name-graph task1 task2 task3 ... start-time end-time

You can provide between 1 and 5 tasks. If you wish to plot more than 5 tasks, a couple quick changes
to the code can allow for that. Similarly, you can change the default colors for the tasks by making
some simple changes to the RGB values in the getColor function. Once you have all this set up, or if 
you are fine with how it already is, you can run it and you should automatically be taken to the 
output graph on the Plotly website through your default browser. You can then export the graph as a
.jpg or .png file.

Example output:
I have some other files in this repository to show an example of some input and what the resulting
output should look like. The graph 'exampleOutput.png' resulted from the data from 'exampleInput.csv'
with the following command:
$ python GanttGrapher.py exampleInput.csv exampleOutput sleeping eating exercising cooking coding 
"2016-08-21 00:00:01" "2016-08-21 23:59:59"

Future adjustments:
I plan to clean up the code a bit, allow users to pick colors for tasks, and perhaps allow them to pick
different colors for the same task but during different repititions of it. I'd also like to display
the x-axis in a more natural form rather than as 'Seconds after STARTDATE'. There is a large variety
of graphing options through Plotly, so I encourage others to look through the other graphs and see
what other interesting things they can do.
