###############################################################################
# Filename: GanttGrapher.py
# First written: 08-20-2016
# Author: Samuel Miller
#
# Description: This is a simple program that uses Plotly software to make a 
# Gantt chart for repeated tasks, taking the schedule data from a .csv file.
###############################################################################
import sys
import csv
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime

# Takes name of file in working directory and the desired column as 
# arguments and returns a list of the values from that column of that file
def getColumn(filename, column):
    results = csv.reader(open(filename), delimiter=",")
    return [result[column] for result in results]

# Takes the input time string as argument and returns the time in seconds
# since Jan. 1, 1970
def getTime(inputDate):
	inputTime = datetime.strptime(inputDate, "%Y-%m-%d %H:%M:%S")
	baseTime = datetime(1970, 1, 1)
	return (inputTime - baseTime).total_seconds()

# Takes the index of the tasks, the list of lengths of each bar for that task,
# and the index of the current bar as arguments and returns the color of that 
# bar segment as a string
def getColor(taskNum, barVals, barValIndex):
	if barValIndex > len(barVals) - 1:
		return 'rgba(255, 255, 255, 0)'
	elif barVals[barValIndex][1] == 'clear':
		return 'rgba(255, 255, 255, 0)'
	elif taskNum == 0:
		return 'rgba(255, 255, 0, 1)'
	elif taskNum == 1:
		return 'rgba(255, 0, 0, 1)'
	elif taskNum == 2:
		return 'rgba(255, 0, 255, 1)'
	elif taskNum == 3:
		return 'rgba(0, 0, 255, 1)'
	else:
		return 'rgba(0, 255, 255, 1)'

# Takes the list of lengths of each bar for a given task and the index of the
# current bar as arguments and returns the size of that bar (or 0 if past last 
# bar in list)
def getBarSize(barVals, barValIndex):
	if barValIndex > len(barVals) - 1:
		return 0
	else:
		return barVals[barValIndex][0]

# Takes the list of tasks, the list of events, the list of start times for each
# event, the list of stop times for each event, the overall start time and the 
# overall end time as arguments and returns the list of row indices 
# corresponding to a given task for all specified tasks
def getTaskIndices(tasks, eventTasks, starts, stops, startTime, endTime):
	taskIndices = []
	for task in tasks:
		taskIndices.append([])

	# Find relevant indices for each task
	for i, task in enumerate(tasks):
		for j, eventTask in enumerate(eventTasks):
			if eventTask == task and starts[j] != '' and stops[j] != '':
				if getTime(starts[j]) < endTime and getTime(stops[j]) > startTime:
					taskIndices[i].append(j)
	
	return taskIndices

# Takes the list of row indices corresponding to different tasks, list of start
# times, list of stop times, overall start time and overall stop time as 
# arguments and returns the list of bar lengths for each task
def getBarVals(taskIndices, starts, stops, startTime, endTime):
	eventStarts = []
	eventStops = []
	barVals = []     # Length of each bar of given task
	
	for indices in taskIndices:
		eventStarts.append([])
		eventStops.append([])
		barVals.append([])

	# Set up bar values for each task
	for i, indices in enumerate(taskIndices):
		for iteration, j in enumerate(taskIndices[i]):
			eventStarts[i].append(getTime(starts[j]))
			eventStops[i].append(getTime(stops[j]))
			if iteration == 0:
				if eventStarts[i][iteration] < startTime:
					if eventStops[i][iteration] > endTime:
						barVals[i].append([endTime - startTime, 'color'])
					else:
						barVals[i].append([eventStops[i][iteration] - startTime, 'color'])
				elif eventStarts[i][iteration] > startTime:
					barVals[i].append([eventStarts[i][iteration] - startTime, 'clear'])
					if eventStops[i][iteration] > endTime:
						barVals[i].append([endTime - eventStarts[i][iteration], 'color'])
					else:
						barVals[i].append([eventStops[i][iteration] - eventStarts[i][iteration], 'color'])
			elif iteration == len(taskIndices[i]) - 1:
				barVals[i].append([eventStarts[i][iteration] - eventStops[i][iteration - 1], 'clear'])
				if eventStops[i][iteration] > endTime:
					barVals[i].append([endTime - eventStarts[i][iteration], 'color'])
				else:
					barVals[i].append([eventStops[i][iteration] - eventStarts[i][iteration], 'color'])
			else:
				barVals[i].append([eventStarts[i][iteration] - eventStops[i][iteration - 1], 'clear'])
				barVals[i].append([eventStops[i][iteration] - eventStarts[i][iteration], 'color'])
	return barVals

# Takes the list of task and list of bar lengths for each task as arguments and
# returns the data object for the graph
def dataBuilder(tasks, barVals):
	data = []
	maxBars = 0
	for i in range(len(tasks)):
		maxBars = max(maxBars, len(barVals[i]))
	
	# Fill in the data list for the graph'
	for barValIndex in range(maxBars):
		barSizes = []
		colors = []
		for i, task in enumerate(tasks):
			barSizes.append(getBarSize(barVals[i], barValIndex))
			colors.append(getColor(i, barVals[i], barValIndex))
		data.append(go.Bar(
			y = tasks,
			x = barSizes,
			orientation = 'h',
			marker = dict(
				color = colors,
			),
			name = ''
		))
	return data

# Takes the data object for the graph, the list of tasks, and the overall start
# time of the graph as arguments and returns the figure object (AKA the graph)
def figureBuilder(data, tasks, startDate):
	# Figure out the tile for the graph
	if len(tasks) == 1:
		titleName = 'Plot of Task: ' + tasks[0]
	elif len(tasks) == 2:
		titleName = 'Plot of Tasks: ' + tasks[0] + ' and ' + tasks[1]
	else:
		titleName = 'Plot of Tasks: '
		for i, task in enumerate(tasks):
			if i == len(tasks) - 1:
				titleName = titleName + 'and ' + task
			else:
				titleName = titleName + task + ', '
		
	# Set axes and title
	layout = go.Layout(
		barmode = 'stack',
		title = titleName,
		xaxis = dict(
			title = 'Time in Seconds After ' + startDate,
			titlefont = dict(
				family = 'Courier New, monospace',
				size = 18,
				color = '#7f7f7f'
			)
		),
		yaxis = dict(
			title = 'Task Names',
			titlefont = dict(
				family = 'Courier New, monospace',
				size = 18,
				color = '#7f7f7f'
			)
		)
	)

	# Construct the graph and return it
	return go.Figure(data = data, layout = layout)
	
# Main method takes CSV file name, desired graph name, task names, as well as 
# start and end dates as command line arguments and constructs a Gantt chart
# and pushes the result to Plotly
def main(argv):
	# Make sure there are between 1 and 5 tasks (and other necessary arguments)
	if len(argv) < 6:
		print(("Command line arguments should contain CSV file name, "
			   "graph name, tasks, and start and end dates."))
		return
	if len(argv) > 10:
		print(("You really shouldn't need to print more than 5 tasks on one "
			   "Gantt Chart (it will get a little crowded)."))
		return
	
	# Set up the names and dates
	inputFile = argv[1]
	graphName = argv[2]
	startDate = argv[len(argv) - 2] # second to last argument
	endDate = argv[len(argv) - 1] # last argument
	
	# Set up the list of tasks
	taskCount = len(argv) - 5 # exclude script name, csv name, graph name, dates
	tasks = []
	for i in range(taskCount):
		tasks.append(argv[3 + i]) # skip script name, csv name, graph name
	
	# Convert date strings to seconds
	startTime = getTime(startDate)
	endTime = getTime(endDate)
	
	# Pull column data out
	eventTasks = getColumn(inputFile, 0)
	starts = getColumn(inputFile, 1)
	stops = getColumn(inputFile, 2)
	
	# Get a list of rows in csv corresponding to each task, get length of each
	# bar for each task, put this into data object, construct the figure and 
	# push it to plotly website
	taskIndices = getTaskIndices(tasks, eventTasks, starts, stops, startTime, endTime)
	barVals = getBarVals(taskIndices, starts, stops, startTime, endTime)
	data = dataBuilder(tasks, barVals)
	figure = figureBuilder(data, tasks, startDate)
	py.plot(figure, inputFile = graphName)
	
# Make sure main function is hit
if __name__ == "__main__":
	main(sys.argv)
