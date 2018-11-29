from flask import Flask, render_template
import socket

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

    with open("/Users/haydensouthworth/Documents/TCU/Senior Year/Python/iotdash/tempcap.txt", "r") as connections:
        lines = connections.readlines()

        for item in lines:
            try:
                linearr = item.split(" ")

                date = linearr[0]
                host = linearr[2]
                reciever = linearr[4]
                # Reverse DNS Lookup
                desti = reciever.split(".")
                destin = desti[0] + "." + desti[1] + "." + desti[2] + "." + desti[3]
                dest = socket.gethostbyaddr(destin)
                dnsName = dest[0]

                fullname = dnsName.split(".")
                name = fullname[-2] + "." + fullname[-1]

                connectionslist.append(name)
                iplist += "<li class='list-group-item'>Sent from: " + host + ", Sent to: " + name + ", on date: " + date + "</li>"
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
