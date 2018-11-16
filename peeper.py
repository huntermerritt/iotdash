from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():

    iplist = ""
    numunique = 0
    numconnections = 0


    chartdata = """
    data = {}
        datasets: [{}],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        {}
    {}
    """


    connectionslist = []

    with open("/Users/Hunter/PycharmProjects/peeper/temp.txt", "r") as connections:
        lines = connections.readlines()

        for item in lines:
            try:
                linearr = item.split(" ")

                date = linearr[0]
                host = linearr[2]
                reciever = linearr[4]

                connectionslist.append(reciever)
                iplist += "<li class='list-group-item'>Sent from: " + host + ", Sent to: " + reciever + ", on date: " + date + "</li>"
            except:
                print(item)



    uniquerecievers = set(connectionslist)

    datastr = "label: 'Requests Per IP Address', data: ["
    labelsstr = "labels: ["

    for address in uniquerecievers:
        datastr += str(connectionslist.count(address)) + ", "
        labelsstr += "'" + address + "', "

    datastr = datastr[:-2] + "]"
    labelsstr = labelsstr[:-2] + "],"


    chartdata = chartdata.format("{", "{" + datastr + "}", labelsstr, "}")

    numunique = str(len(uniquerecievers))
    numconnections = str(len(connectionslist))

    return render_template("index.html", iplist=iplist, numunique=numunique, numconnections=numconnections, chartdata=chartdata)


if __name__ == '__main__':
    app.run()
