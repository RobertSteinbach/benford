# pip install flask
from flask import Flask, render_template, request, redirect
import csv
from glob import glob
import os

app = Flask(__name__)
stats = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0}
keys = ('1', '2', '3', '4', '5', '6', '7', '8', '9')


@app.route("/", methods=['GET','POST'])
def index():

    data = []
    eMsg = "Welcome.  Paste data into text box -or- prefill from a selected source."
    textarea = ''                 # default empty
    prefill = ''                  # default that a prefill value was NOT passed
    csvOption = ''                # assume nothing selected



    #clear the dictionary
    for i in range(9):
        stats[str(i+1)] = 0


    # Get information from the POST
    if request.method == "POST":

        # get the data from the input form
        try:
            textarea = request.form['rawdata']      # capture raw to redisplay on screen
            data = textarea.split()                 # put into a list
            csvOption = request.form['CSVOption']
        except Exception as e:
            eMsg = "Error reading form.  Error: " + str(e)

        #print('data=', data)


    # build a list of CSV files and make HTML for SELECT object.
    csvOptionsHTML = '<option selected value="">[none]</option>'
    templist = glob('static/csv/*.csv')
    templist.sort(key=os.path.basename)
    for item in templist:
        csvName = os.path.basename(item)
        #print(os.path.basename(item))
        csvOptionsHTML += "<OPTION "
        if csvOption == csvName:
            csvOptionsHTML += "SELECTED "
        csvOptionsHTML += "VALUE='" + csvName + "'>" + csvName + "</OPTION>"


    # If a prefill button was pressed, read the file and overwrite any input
    if csvOption != '':
        print('csvOption=', csvOption)
        data = []                               # wipe out any input that was passed
        with open('static/csv/' + csvOption) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                #print(row)
                data.append(row[0])
            textarea = "&#10;".join(data)


    # if length of data is zero (first time), then reset with defaults
    if len(data) < 1:
        data = []
        rowCount = 1   # prevent divide by zero error
    else:
        rowCount = len(data)

    # iterate through the list and count the first digits

    for row in data:
        # print(row, row[0])
        firstNum = str(row)[0]

        if firstNum not in keys:
            eMsg = "Input did not appear to be numeric.  Try again. "
        try:
            stats[firstNum] += 1
        except Exception as e:
            pass

        # print(stats.get(firstNum))

    # make a list of labels
    labels = []
    for i in range(9):
        labels.append(i+1)

    # make a list of values
    values = []
    for row in stats:
        values.append(stats[row])


    return render_template('index.html',data=data, textarea=textarea, stats=stats, rowCount=rowCount,
                labels=labels, values=values, eMsg=eMsg, csvOptionsHTML=csvOptionsHTML)



if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')



"""   Parking LOT



    # read the input file and build a list
    #with open('data.csv') as csv_file:
    #    csv_reader = csv.reader(csv_file)
    #    for row in csv_reader:
    #        #print(row)
    #        data.append(row[0])

    # show results
    #for row in stats:
    #    print(row, stats[row], rowCount, stats[row]/rowCount*100)


    # Sum up the numbers until we get one digit  (This doesn't produce the effect)
    sumdata = []
    for row in data:
        numTotal = 0
        for num in row:
            numTotal += int(num)
        # print(row, str(numTotal))

        # condense it down to one digit
        while len(str(numTotal)) > 1:
            newNumTotal = 0
            for num in str(numTotal):
                newNumTotal += int(num)
            numTotal = newNumTotal
        # print(row, str(numTotal))

        # save it in a list
        sumdata.append(numTotal)

    # collect stats
    sumstats = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '0': 0}
    for row in sumdata:
        firstNum = str(row)
        sumstats[firstNum] += 1
        # print(firstNum, sumstats.get(firstNum))

    # show results
    for row in sumstats:
        print(row, sumstats[row], rowCount, sumstats[row]/rowCount*100)






"""

