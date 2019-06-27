from tkinter import *
from netaddr import *

# Creates GUI window and frames within the window
window = Tk()
window.title("SubnetCalc")
window.geometry("255x375")
window.resizable(0, 0)

ipentry_frame = Frame(window)
submaskentry_frame = Frame(window)
results_frame = Frame(window)
error_frame = Frame(window)

ipentry_frame.pack(pady=10)
submaskentry_frame.pack()
error_frame.pack(pady=3)
results_frame.pack()

# Sets variables used in the application
ip = StringVar()
subnet = StringVar()
subid = StringVar()
firsthost = StringVar()
lasthost = StringVar()
broadcast = StringVar()
nextnet = StringVar()
hostnum = StringVar()
ipclass = StringVar()
privaddr = StringVar()
error = StringVar()


# Function called when GO button is pressed
def btn_go(event=None):
    # Retrieves ip address from ipentry field
    ipaddress = IPAddress(ipentryent.get())

    if slashnotent.get() > "32":
        error_call()
        return

    # Works out subnet mask from slash notation if subnet mask is not entered
    if submaskent.get() == "":
        if slashnotent.get() == "":
            error_call()
            return
        else:
            fulladdress = IPNetwork(ipentryent.get() + "/" + slashnotent.get())
            submask = fulladdress.netmask
            subnet.set(submask)
            ip.set(str(ipaddress) + " / " + slashnotent.get())

    # Works out slash notation from subnet mask if slash notation is not entered
    if slashnotent.get() == "":
        if submaskent.get() == "":
            error_call()
            return
        else:
            submask = IPAddress(submaskent.get())
            networkbits = submask.bits()
            slashnot = networkbits.count("1")
            ip.set(str(ipaddress) + " / " + str(slashnot))
            subnet.set(submaskent.get())

    if slashnotent.get() == "":
        fullip = IPNetwork(ip.get())
    else:
        fullip = IPNetwork(ipentryent.get() + "/" + slashnotent.get())

    # Works out class of ip address
    firstoctet = int((ipentryent.get()).split(".")[0])
    classa = range(1, 127)
    classb = range(128, 191)
    classc = range(192, 223)

    if firstoctet in classa:
        ipclass.set("Class A")
    elif firstoctet in classb:
        ipclass.set("Class B")
    elif firstoctet in classc:
        ipclass.set("Class C")
    else:
        ipclass.set("")

    # Works out if ip address is Private/Public
    iprange_a = IPRange("10.0.0.0", "10.255.255.255")
    iprange_b = IPRange("172.16.0.0", "172.31.255.255")
    iprange_c = IPRange("192.168.0.0", "192.168.255.255")

    if ipentryent.get() in iprange_a:
        privaddr.set("Private")
    elif ipentryent.get() in iprange_b:
        privaddr.set("Private")
    elif ipentryent.get() in iprange_c:
        privaddr.set("Private")
    else:
        privaddr.set("Public")

    # Works out results based on full ip address and sets StringVar's to display results
    subid.set(fullip.network)
    firsthost.set(fullip.network + 1)
    broadcast.set(fullip.broadcast)
    lasthost.set(fullip.broadcast - 1)
    hostnum.set(fullip.size - 2)
    nextnet.set(fullip.broadcast + 1)

    clearall()


# Clears entries and sets focus to ip entry
def clearall():
    ipentryent.delete(0, "end")
    slashnotent.delete(0, "end")
    submaskent.delete(0, "end")
    ipentryent.focus()
    error.set("")


# Function to display error message if invalid ip address is entered
def error_call():
    error.set("INVALID ENTRY")


# Widgets below:
ipentrylbl = Label(ipentry_frame, text="IP Address: ").pack(side=LEFT)
ipentryent = Entry(ipentry_frame, width=15)
ipentryent.pack(side=LEFT)
ipentryent.focus()
ipentryent.bind("<Return>", btn_go)
slashnotlbl = Label(ipentry_frame, text="/").pack(side=LEFT, padx=2)
slashnotent = Entry(ipentry_frame, width=5)
slashnotent.pack(side=LEFT)
slashnotent.bind("<Return>", btn_go)
submasklbl = Label(submaskentry_frame, text="Subnet Mask: ").pack(side=LEFT)
submaskent = Entry(submaskentry_frame, width=15)
submaskent.pack(side=LEFT)
submaskent.bind("<Return>", btn_go)
gobtn = Button(submaskentry_frame, text="GO", font=(None, 8, "bold"), command=btn_go, width=7)
gobtn.pack(padx=7)
gobtn.bind("<Return>", btn_go)
errorlbl = Label(error_frame, textvariable=error, fg="red")
errorlbl.pack(pady=2)

ipaddresslbl = Label(results_frame, text="IP Address: ", font=(None, 10)).grid(row=0, column=0, pady=2)
subnetmasklbl = Label(results_frame, text="Subnet Mask: ", font=(None, 10)).grid(row=1, column=0, pady=2)
subidlbl = Label(results_frame, text="Subnet ID: ", font=(None, 10)).grid(row=2, column=0, pady=2)
firsthostlbl = Label(results_frame, text="First Host: ", font=(None, 10)).grid(row=3, column=0, pady=2)
lasthostlbl = Label(results_frame, text="Last Host: ", font=(None, 10)).grid(row=4, column=0, pady=2)
broadcastlbl = Label(results_frame, text="Broadcast: ", font=(None, 10)).grid(row=5, column=0, pady=2)
nextnetlbl = Label(results_frame, text="Next Network: ", font=(None, 10)).grid(row=6, column=0, pady=2)
hostnumlbl = Label(results_frame, text="Number of Hosts: ", font=(None, 10)).grid(row=7, column=0, pady=2)
classlbl = Label(results_frame, text="IP Class: ", font=(None, 10)).grid(row=8, column=0, pady=2)
privaddrlbl = Label(results_frame, text="Private/Public", font=(None, 10)).grid(row=9, column=0, pady=2)

ipaddressres = Label(results_frame, textvariable=ip, font=(None, 10, "bold"), fg="blue").grid(row=0, column=1)
submaskres = Label(results_frame, textvariable=subnet, font=(None, 10, "bold"), fg="blue").grid(row=1, column=1)
subidres = Label(results_frame, textvariable=subid, font=(None, 10, "bold"), fg="blue").grid(row=2, column=1)
firsthostres = Label(results_frame, textvariable=firsthost, font=(None, 10, "bold"), fg="blue").grid(row=3, column=1)
lasthostres = Label(results_frame, textvariable=lasthost, font=(None, 10, "bold"), fg="blue").grid(row=4, column=1)
broadcastres = Label(results_frame, textvariable=broadcast, font=(None, 10, "bold"), fg="blue").grid(row=5, column=1)
nextnetres = Label(results_frame, textvariable=nextnet, font=(None, 10, "bold"), fg="blue").grid(row=6, column=1)
hostnumres = Label(results_frame, textvariable=hostnum, font=(None, 10, "bold"), fg="blue").grid(row=7, column=1)
classres = Label(results_frame, textvariable=ipclass, font=(None, 10, "bold"), fg="blue").grid(row=8, column=1)
privaddrres = Label(results_frame, textvariable=privaddr, font=(None, 10, "bold"), fg="blue").grid(row=9, column=1)

window.mainloop()
