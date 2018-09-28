from socket import AF_INET, socket,SOCK_STREAM
from tkinter import *
from tkinter.ttk import *
import threading
import time

#basic setup
root = Tk()
root.title("P2P chat")
buffsixe = 1024
sStatus = 0


def listenForPeer(s):
    ps, paddr = s.accept()
    threading.Thread(target=recvMsg, args=(ps,)).start()

def recvMsg(s):
    while True:
        data = s.recv(buffsize).decode()
        printMsg(data)
    
def printMsg(msg):
    chat.config(state=NORMAL)
    chat.insert("end",msg+"\n")
    chat.config(state=DISABLED)

def setServer():
    port=int(serverPortVar.get().replace(' ',''))
    try:
        ss = socket(AF_INET,SOCK_STREAM)
        ss.bind(('',port))
        global sStatus
        sStatus = 1
        ss.listen(2)
        printMsg("Listening for connection")
        print(sStatus)
        threading.Thread(target=listenForPeer, args=(ss,)).start()
    except:
        printMsg("Error setting up server")

def setPeerAddress():
    print(sStatus)
    if sStatus == 0:
        printMsg("Please set details first")
        return
    paddr = (peerIPVar.get().replace(' ',''), int(peerPortVar.get().replace(' ','')))
    try:
        ps = socket(AF_INET,SOCK_STREAM)
        ps.connect()
        printMsg("Connected to peer")
        threading.Thread(target=recvMsg, args=(ps,)).start()
    except:
        printMsg("Error connecting to peer")

def sendMsg():
    if sStatus == 0:
        printMsg("Please set details first")
        return
    msg = chatVar.get().replace(' ','')
    printMsg(msg)
    ps.send(msg)

#screen size and positioning
ScreenSizeX = root.winfo_screenwidth()
ScreenSizeY = root.winfo_screenheight()
FramePosX   = (ScreenSizeX - 800)/2
FramePosY   = (ScreenSizeY - 600)/2
root.geometry("%sx%s+%s+%s" % (800,600,int(FramePosX),int(FramePosY)))
root.resizable(width=False, height=False)

#frames
padX = 20
padY = 20
parentFrame = Frame(root)
parentFrame.grid(padx=padX, pady=padY, sticky=E+W+N+S)
info1Frame = Frame(parentFrame)
info2Frame = Frame(parentFrame)
chatFrame = Frame(parentFrame)
sendFrame = Frame(parentFrame)
info1Frame.grid(row=0,column=1,padx=30)
info2Frame.grid(row=1,column=1,padx=30)
chatFrame.grid(row=0,rowspan=2,column=0)
sendFrame.grid(row=2,rowspan=1,column=0,pady=20)

#widgets
serverLabel = Label(info1Frame, text="Set details:", font="Helvetica 12 bold")
serverPortVar = StringVar()
serverPortVar.set("Port")
serverPortField = Entry(info1Frame, width=12, textvariable=serverPortVar)
serverSetButton = Button(info1Frame, text="Set", width=10, command=setServer)
addPeerLabel = Label(info2Frame, text="Connect to: ", font="Helvetica 12 bold")
peerIPVar = StringVar()
peerIPVar.set("IP Addres")
peerIPField = Entry(info2Frame, width=12,textvariable=peerIPVar)
peerPortVar = StringVar()
peerPortVar.set("Port")
peerPortField = Entry(info2Frame, width=12, textvariable=peerPortVar)
peerSetButton = Button(info2Frame, text="Connect", width=10, command=setPeerAddress)
serverLabel.grid(row=1, column=0, pady=3)
serverPortField.grid(row=3, column=0, pady=3)
serverSetButton.grid(row=4, column=0, pady=3,)
addPeerLabel.grid(row=1, column=0, pady=3)
peerIPField.grid(row=2, column=0, pady=3)
peerPortField.grid(row=3, column=0, pady=3)
peerSetButton.grid(row=4, column=0, pady=3)
chat = Text(chatFrame,bg="white",width=75,height=30,state=DISABLED)
chat.grid(row=0,column=0,sticky=W+N+S, padx = (0,10))
chatVar = StringVar()
chatField = Entry(sendFrame,width=75,textvariable=chatVar)
chatButton = Button(sendFrame,text="Send",width=20,command=sendMsg)
chatField.grid(row=0,column=0)
chatButton.grid(row=0,column=1,padx=5)



root.mainloop()

