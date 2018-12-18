# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 10:09:04 2018

@author: Pioneer
"""
import random
import math
import numpy
import tkinter as tk

class SuperPeerModel:
    def __init__(self):
        self.n = 100
        self.nPos = [-1]*self.n
        self.effNodes = [-1]*(math.floor(25*self.n/100))
        self.realConn = list()
        self.finalOverlay = list()
        self.spPair=list()
        
        self.win = tk.Tk()
        self.win.title("Super-Peer Network Model")
        self.win.state('zoomed')
        
        #1st column
        self.cWidth = 1000
        self.cHeight = 700
        self.h = 500
        self.k = 350
        self.canvas = tk.Canvas(self.win, width=self.cWidth, height=self.cHeight)
        self.canvas.grid(row=0, columnspan=2)
        
        #2nd column
        RCFrame = tk.Frame(self.win)
        lblRCFrame = tk.Message(RCFrame, text="Input node no to view individual connections then press enter (0 to "+str(self.n-1)+") To view the full connection press enter leaving the textbox empty.", width=300)
        self.txtRealConnection = tk.Text(RCFrame, height=1, width=5)
        self.txtRealConnection.bind("<Return>", self.ShowRealConn)
        self.lblRCWarning = tk.Label(RCFrame, fg="red")
        lblRCFrame.grid(row=0, columnspan=2)
        self.txtRealConnection.grid(row=1, column=0, sticky=tk.NW)
        self.lblRCWarning.grid(row=1, column=1, sticky=tk.NW)
        
        lblONFrame = tk.Message(RCFrame, text="Input the number of superpeers", width=300)
        self.txtNoOfSP = tk.Text(RCFrame, height=1, width=5)
        self.txtNoOfSP.bind("<Return>", self.ShowOverlayNetwork)
        self.lblONWarning = tk.Label(RCFrame, fg="red")
        lblONFrame.grid(row=2, columnspan=2, sticky=tk.NW)
        self.txtNoOfSP.grid(row=3, column=0, sticky=tk.NW)
        self.lblONWarning.grid(row=3, column=1, sticky=tk.NW)
        
        lblSDFrame = tk.Message(RCFrame, text="Input the source and destination node number to find the path between them", width=300)
        lblSource = tk.Label(RCFrame, text="Source")
        self.txtSource = tk.Text(RCFrame, height=1, width=5)
        self.txtSource.bind("<Return>", self.ShowPath)
        lblDest = tk.Label(RCFrame, text="Destination")
        self.txtDestination = tk.Text(RCFrame, height=1, width=5)
        self.txtDestination.bind("<Return>", self.ShowPath)
        self.lblSDWarning = tk.Label(RCFrame, fg="red")
        lblSDFrame.grid(row=4, columnspan=2, sticky=tk.NW)
        lblSource.grid(row=5, column=0, sticky=tk.NW)
        self.txtSource.grid(row=5, column=1, sticky=tk.NW)
        lblDest.grid(row=6, column=0, sticky=tk.NW)
        self.txtDestination.grid(row=6, column=1, sticky=tk.NW)
        self.lblSDWarning.grid(row=7, columnspan=2, sticky=tk.NW)
        
        self.msgInfo = tk.Message(RCFrame, text="Info: \n Number of Super-Peers: 2 \n", width=300)
        self.msgInfo.grid(row=8, columnspan=2, sticky=tk.NW)
        tk.Message(RCFrame, text="Notes:\n 1. The green nodes are the efficient nodes which are the candidaites for the superpeer.\n 2. The white nodes are the normal nodes which are less efficient as compared to green nodes. \n 3. The thin solid black line between two nodes represent direct connection between them in real network. \n 4. The Yellow nodes are the superpeers. The lines extending from a superpeer represents its clients in its cluster. Each cluster has different coloured line to distinguish from other clusters. \n 5. Thick solid blue line running from the source node to the destination node represents the path in the overlay network between them. \n 5. Thick dashed purple line running from the source node to the destination node represents the path in the underlying real network between them (Sometimes the purple dashed line may be hidden beneath the solid blue line. Also, the purple dashed line may be overlapping with each other. It appears very thick in comaprision to others.). \n 6. The blue node represents the source node and the red node represents the destination node.", width=300).grid(row=9, columnspan=2, sticky=tk.NW)
        RCFrame.grid(row=0, column=2, sticky=tk.NW)
        
        
        self.ArchSuperPeer()
        
    def ArchSuperPeer(self):
        nPerQuarter = math.ceil(self.n/4)
        nPerFirstQuarter = self.n - 3*nPerQuarter
        nQuarters = 1
        
        #for generating random efficient nodes
        for i in range(len(self.effNodes)):
            effn = random.randint(0, self.n-1)
            while effn in self.effNodes:
                effn = random.randint(0, self.n-1)
            self.effNodes[i] = effn

        # for generating real network connection:
        self.realConn = numpy.full((self.n, self.n), False)
        for i in range(self.n):
            rcPer = math.ceil(25*self.n/100)
            while len([conn for conn in self.realConn[i] if conn]) < rcPer:
                c = random.randint(0, self.n-1)
                while self.realConn[i][c] or c == i:
                    c = random.randint(0, self.n-1)
                if len([c1 for c1 in self.realConn[i] if c1]) < rcPer: 
                    self.realConn[i][c] = True
                if len([c2 for c2 in self.realConn[c] if c2]) < rcPer: 
                    self.realConn[c][i] = True
            
        for i in range(1, (nPerFirstQuarter+1)):
            x = random.randint(self.cWidth/2+20, self.cWidth-20)
            y = (self.cHeight)/(nPerFirstQuarter*2)*i
            self.nPos[i-1] = (x,y)
        
        nQuarters += 1
        while nQuarters <= 4:
            for i in range(1, (nPerQuarter+1)):
                x = random.randint((self.cWidth/2+20 if nQuarters == 2 else 20), (self.cWidth-20 if nQuarters == 2 else self.cWidth/2-20))
                y = (self.cHeight-15)/(nPerFirstQuarter*(1 if nQuarters < 4 else 2))*i
                self.nPos[i+nPerFirstQuarter+nPerQuarter*(nQuarters-2)-1] = (x,y)
            nQuarters += 1
            
        overlap = list()
        for i in range(0,self.n):
                for j in range(i+1,self.n):
                    if math.sqrt((self.nPos[i][0]-self.nPos[j][0])**2+(self.nPos[i][1]-self.nPos[j][1])**2) < 30:
                        overlap.append([i,j])
                        
        while len(overlap) > 0:
            for i in range(len(overlap)):
                x1 = overlap.pop(0)
                newX = (self.nPos[x1[0]][0] + 30)%(self.cWidth-10)
                self.nPos[x1[0]] = (newX+12 if newX < 12 else newX), self.nPos[x1[0]][1]
            
            for i in range(0,self.n):
                for j in range(i+1,self.n):
                    if math.sqrt((self.nPos[i][0]-self.nPos[j][0])**2+(self.nPos[i][1]-self.nPos[j][1])**2) < 30:
                        overlap.append([i,j])
              
        
        self.DrawRealConnection()
        self.DrawNodes()
        
        self.win.mainloop()
    
    
    def DrawNodes(self, sp=None):
        for i, xy in enumerate(self.nPos):
            x = xy[0]
            y = xy[1]
            self.canvas.create_oval(x-10, y-10, x+10, y+10, fill=("yellow" if sp is not None and i in sp else "green" if i in self.effNodes else "white"), width=(3 if sp is not None and i in sp else 1))
            self.canvas.create_text(x, y, text=i)
    
    
    def ShowRealConn(self, event):
        c = self.txtRealConnection.get("1.0", tk.END)
        self.txtRealConnection.delete('1.0', tk.END)
        self.canvas.delete("all")
        warning = "Please input positive integer value which is less than "+str(self.n)
        if c.strip() == "":
            self.DrawRealConnection()
        else:
            try:
                c = int(c)
                if c >= 0:
                    self.DrawRealConnection(selectedNode=c)
                else:
                    self.lblRCWarning.config(text=warning)
            except:
                self.lblRCWarning.config(text=warning)
        self.DrawNodes()
    
    
    def DrawRealConnection(self, selectedNode=None, overlayNetwork=None, sp=None):
        self.ResetWarning()
        if selectedNode is not None:
            conn = [j for j, c in enumerate(self.realConn[selectedNode]) if c]
            for c in conn:
                self.canvas.create_line(self.nPos[selectedNode][0], self.nPos[selectedNode][1], self.nPos[c][0], self.nPos[c][1])
        elif overlayNetwork is not None:
            clr = dict()
            for pp in overlayNetwork:
                if pp is not None:
                    r = random.randint(50,255)
                    g = random.randint(10+pp,255)
                    b = random.randint(15+pp,255)
                    clr[pp] = self.RGB(r, g, b) 
            
            for node, superPeer in enumerate(overlayNetwork):
                if superPeer is not None:
                    self.canvas.create_line(self.nPos[node][0], self.nPos[node][1], self.nPos[superPeer][0], self.nPos[superPeer][1], fill=clr[superPeer])

            pair = list()
            if len(sp) > 1:
                for i in range(len(sp)):
                    p, minD = None, None
                    for j in range(len(sp)):
                        if j != i:
                            d = self.EucledianDistance(self.nPos[sp[i]], self.nPos[sp[j]])
                            if p is None or d < minD and len(pair) == 0 or ((i,p) not in pair and (p,i) not in pair):
                                p = j
                                minD = d
                    pair.append((sp[i], sp[p]))
                    self.canvas.create_line(self.nPos[sp[i]][0], self.nPos[sp[i]][1], self.nPos[sp[p]][0], self.nPos[sp[p]][1], width=2)
            self.spPair = pair
        else:
            for i, rc in enumerate(self.realConn):
                conn = [j for j, c in enumerate(rc) if c]
                for c in conn:
                    self.canvas.create_line(self.nPos[i][0], self.nPos[i][1], self.nPos[c][0], self.nPos[c][1])
            
      
          
    def OverlayNetwork(self, spCount = 2):
        dictDist = dict()
        self.msgInfo.configure(text="Info \n Number of Super-Peers: " + str(spCount))
        for node in self.effNodes:
            dictDist[node] = self.EucledianDistance(self.nPos[node])
        sortedDist = sorted(dictDist.items(), key=lambda kv: kv[1])
        choosenSP = sortedDist[0:spCount*3-1:3]
        choosenSPNodes = [tup[0] for tup in choosenSP]
        finalOverlay = [-1]*self.n
        
        for node in range(self.n):
            dictDist[node] = self.EucledianDistance(self.nPos[node])
        allSortedDist = sorted(dictDist.items(), key=lambda kv: kv[1], reverse=True)
        
        for nodeDist in allSortedDist:
            minD, c = None, None
            for sp in choosenSP:
                if nodeDist[0] not in choosenSPNodes:
                    d = self.EucledianDistance(self.nPos[nodeDist[0]], self.nPos[sp[0]])
                    if (c is None or d < minD) and len([fo for fo in finalOverlay if fo == sp[0]]) <= (self.n/spCount+2):
                        minD = d
                        c = sp[0]
            finalOverlay[nodeDist[0]] = c
        
        self.finalOverlay = finalOverlay
        self.canvas.delete("all")
        self.DrawRealConnection(overlayNetwork=finalOverlay, sp=choosenSPNodes)
        self.DrawNodes(sp=choosenSPNodes)
     
        
        
    def ShowOverlayNetwork(self, event):
        self.ResetWarning()
        self.spPair = list()
        self.finalOverlay = list()
        
        noSP = self.txtNoOfSP.get("1.0", tk.END)
        self.txtNoOfSP.delete('1.0', tk.END)
        try:
            noSP = int(noSP)
            if noSP <= 0:
                self.lblONWarning.config(text="There must be at least 1 superpeer!")
            elif noSP > math.ceil(25*self.n/300):
                self.lblONWarning.config(text="The overlay network is saturated. No more superpeers!")
            else:
                self.OverlayNetwork(spCount=noSP)
        except Exception as ex:
            self.lblONWarning.config(text="Please Input Positive Integer value only")
    

    def ShowPath(self, event):
        self.ResetWarning()
        source = self.txtSource.get("1.0", tk.END)
        dest = self.txtDestination.get("1.0", tk.END)
        self.txtSource.delete('1.0', tk.END)
        self.txtDestination.delete('1.0', tk.END)
        try:
            source = int(source)
            dest = int(dest)
            if source < 0 or dest < 0:
                self.lblSDWarning.config(text="Both Source and Destination Node should have positive integer value only.")
            else:
                self.OverlayNetwork(len(self.spPair) if len(self.spPair) > 0 else 2)
                self.msgInfo.configure(text="Info \n Number of Super-Peers: " + str(len(self.spPair)) + "\n Source Node: " + str(source) + "\n Destination Node: " + str(dest))
                self.canvas.create_oval(self.nPos[source][0]-10, self.nPos[source][1]-10, self.nPos[source][0]+10, self.nPos[source][1]+10, fill="#3775A9", width=2, dash=(3,5))
                self.canvas.create_text(self.nPos[source][0], self.nPos[source][1], text=source)
                self.canvas.create_oval(self.nPos[dest][0]-10, self.nPos[dest][1]-10, self.nPos[dest][0]+10, self.nPos[dest][1]+10, fill="#D93F27", width=2, dash=(3,5))
                self.canvas.create_text(self.nPos[dest][0], self.nPos[dest][1], text=dest)
                lstOP = list()
                lstOP.append(source)
                if self.finalOverlay[source] is None or self.finalOverlay[dest] == None:
                    self.lblSDWarning.config(text="Source or Destination cannot be superpeer node.")
                else:
                    if self.finalOverlay[source] == self.finalOverlay[dest]:
                        lstOP.append(self.finalOverlay[source])
                        lstOP.append(dest)
                        self.canvas.create_line(self.nPos[source][0], self.nPos[source][1], self.nPos[self.finalOverlay[source]][0], self.nPos[self.finalOverlay[source]][1], fill="Blue", width=2, arrow=tk.LAST)
                        self.canvas.create_line(self.nPos[dest][0], self.nPos[dest][1], self.nPos[self.finalOverlay[dest]][0], self.nPos[self.finalOverlay[dest]][1], fill="Blue", width = 2, arrow=tk.FIRST)
                    else:
                        s = self.finalOverlay[source]
                        lstOP.append(s)
                        self.canvas.create_line(self.nPos[source][0], self.nPos[source][1], self.nPos[s][0], self.nPos[s][1], fill="Blue", width=2, arrow=tk.LAST)
                        traversed = set()
                        flagStop = False
                        while True:
                            traversed.add(s)
                            flagGT1 = False
                            pairs = [pair for pair in self.spPair if (pair[0] == s and pair[1] not in traversed) or (pair[1] == s and pair[0] not in traversed)]
                            
                            if len(pairs) == 2:
                                if min(pairs[0][0], pairs[0][1]) == min(pairs[1][0], pairs[1][1]) and max(pairs[0][0], pairs[0][1]) == max(pairs[1][0], pairs[1][1]):
                                    flagGT1 = True
                            if len(pairs) > 1 and not flagGT1:
                                for pair in pairs:
                                    d = pair[0] if pair[0] not in traversed else pair[1]
                                    if d == self.finalOverlay[dest]:
                                        lstOP.append(d)
                                        lstOP.append(dest)
                                        self.canvas.create_line(self.nPos[s][0], self.nPos[s][1], self.nPos[d][0], self.nPos[d][1], fill="Blue", width=2, arrow=tk.LAST)
                                        self.canvas.create_line(self.nPos[d][0], self.nPos[d][1], self.nPos[dest][0], self.nPos[dest][1], fill="Blue", width=2, arrow=tk.LAST)
                                        flagStop = True
                                        break
                                    traversed.add(d)
                            else:
                                d = pairs[0][0] if pairs[0][0] not in traversed else pairs[0][1]
                                lstOP.append(d)
                                self.canvas.create_line(self.nPos[s][0], self.nPos[s][1], self.nPos[d][0], self.nPos[d][1], fill="Blue", width=3, arrow=tk.LAST)
                                if d == self.finalOverlay[dest]:
                                    lstOP.append(dest)
                                    self.canvas.create_line(self.nPos[d][0], self.nPos[d][1], self.nPos[dest][0], self.nPos[dest][1], fill="Blue", width=3, arrow=tk.LAST)
                                    flagStop = True
                                    break
                                s = d
                            if flagStop:
                                break
                self.ShowRealPath(lstOP)
        except Exception as ex:
            self.lblSDWarning.config(text="Both Source and Destination Node should have integer value only.")
    
    def ShowRealPath(self, lst):
        for i in range(len(lst)-1):
            source = lst[i]
            dest = lst[i+1]
            c = self.realConn[source]
            if c[dest] == True:
                self.canvas.create_line(self.nPos[source][0]-5, self.nPos[source][1]-5, self.nPos[dest][0]-5, self.nPos[dest][1]-5, fill="Purple", width=4, arrow=tk.LAST, dash=(3,5))
            else:
                conns = [index for index, conn in enumerate(c) if conn == True]
                for conn in conns:
                    c2 = self.realConn[conn]
                    if c2[dest] == True:
                        self.canvas.create_line(self.nPos[source][0]-5, self.nPos[source][1]-5, self.nPos[conn][0]-5, self.nPos[conn][1]-5, fill="Purple", width=4, arrow=tk.LAST, dash=(3,5))
                        self.canvas.create_line(self.nPos[conn][0]-5, self.nPos[conn][1]-5, self.nPos[dest][0]-5, self.nPos[dest][1]-5, fill="Purple", width=4, arrow=tk.LAST, dash=(3,5))
                        break
                    
    
    def EucledianDistance(self, p, q=None):
        if q is None:
            return math.sqrt((p[0]-self.h)**2+(p[1]-self.k)**2)
        else:
            return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)
        
    def RGB(self, r, g, b):
        return '#{:02X}{:02X}{:02X}'.format(r, g, b)
    
    def ResetWarning(self):
        self.lblRCWarning.config(text="")
        self.lblONWarning.config(text="")
        self.lblSDWarning.config(text="")
        
SuperPeerModel()
        