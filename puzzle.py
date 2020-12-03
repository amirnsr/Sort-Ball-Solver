import numpy as np
from bs4 import BeautifulSoup
import requests
import os
import time
from selenium import webdriver

URL='https://sumx.ir'
headers={'User-Agent': 'Chrome/39.0.2171.95'}

st=False
seqq=[]
nodes=set()

def getTop(p,act):
    i=act[0]
    j=act[1]
    a=0
    while(a<4 and p[a][i]==" "):
        a+=1
    if a==4:
        a-=1
    b=0
    while(b<4 and p[b][j]==" "):
        b+=1
    return a,b

def sameColor(x,y):
    c=set()
    for i in x:
        if i!=" ":
            c.add(i)
    for i in y:
        if i!=" ":
            c.add(i)
    return len(c)==1

def availableActions(p):
    #print(p[:,0])
    actions=[]
    lates=[]
    for i in range(14):
        if p[:,i].all==" ":
            continue
        src=i
        for j in range(14):
            if j==i:
                continue
            if " " not in p[:,j]:
                continue
            trg=j
            a,b=getTop(p,[src,trg])
            if sameColor(p[:,src],p[:,trg]):
                if a<b:
                    src=j
                    trg=i
            #print(a,b)
            if a==4:
                continue
            if b==4:
                #actions.append([src,trg])
                flag=True
                if a==3:
                    lates.append([src,trg])
                    continue
                while(a<3):
                    if p[a][src]!=p[a+1][src]:
                        flag=False
                    a+=1
                if flag:
                    lates.append([src,trg])
                    continue
                actions.append([src,trg])
            elif b!=0 and p[b][j]==p[a][i]:
                actions.insert(0,[src,trg])
    for l in lates:
        actions.append(l)
    return actions

def showPiles(p,act=None):
    for i in range(14):
        print('\n')
        if act!=None and i==act[0]:
            print("F: "+str(p[:,i]))
        elif act!=None and i==act[1]:
            print("T: "+str(p[:,i]))
        else:
            print(p[:,i])

def win(p):
    for i in range(14):
        if p[0][i]!=p[1][i]:
            return False
        if p[0][i]!=p[2][i]:
            return False
        if p[0][i]!=p[3][i]:
            return False
        if p[1][i]!=p[2][i]:
            return False
        if p[1][i]!=p[3][i]:
            return False
        if p[2][i]!=p[3][i]:
            return False
    return True

def doAction(p,act):
    a,b=getTop(p,act)
    i=act[0]
    j=act[1]
    if b==4:
        p[3][j]=p[a][i]
        p[a][i]=" "
    else:
        p[b-1][j]=p[a][i]
        p[a][i]=" "
    return p

stack=[]

def bfs(p,h=0):
    global st
    while(len(stack)):
        if st:
            return
        nxtp=stack.pop(0)
        actions=availableActions(nxtp)
        if win(nxtp):
            st=True
            print("Win!")
            return
        if len(actions)==0:
            print("No Action")
            continue
        if str(nxtp) in nodes:
            print("Oops")
            continue
        nodes.add(str(nxtp))
        print("\033[H\033[J")
        for act in actions:
            stack.append(doAction(np.copy(nxtp),act))
        showPiles(nxtp)
        time.sleep(0.1)
        
def dfs(p,h=0):
    global st
    if st:
        return
    if win(p):
        st=True
        print("Win!")
        return
    actions=availableActions(p)
    if len(actions)==0:
        #print("No Action")
        return
    if str(p) in nodes:
        #print("Oops")
        return
    nodes.add(str(p))
    #print("\033[H\033[J")
    #showPiles(p)
    #time.sleep(0.1)
    for act in actions:
        seqq.append(act)
        dfs(doAction(np.copy(p),act),h+1)
        if st:
            return
        seqq.pop()

def fining(seq):
    deli=set()
    #deli.clear()
    for i in range(len(seq)):
        if i in deli:
            continue
        for j in range(i+1,len(seq)):
            if j in deli:
                continue
            if seq[i][1]==seq[j][0]:
                flag=True
                for k in range(i+1,j):
                    if seq[i][1]==seq[k][1]:
                        flag=False
                        break
                    if seq[i][0]==seq[k][1]:
                        flag=False
                        break
                    if seq[i][0]==seq[k][0]:
                        flag=False
                        break
                    if seq[i][1]==seq[k][0]:
                        flag=False
                        break
                    if seq[j][1]==seq[k][0]:
                        flag=False
                        break
                    if seq[j][1]==seq[k][1]:
                        flag=False
                        break
                if flag:
                    if seq[i]==[12,11]:
                        print("YES")
                        #print(seq[j],j-i)
                    deli.add(j)
                    seq[i][1]=seq[j][1]
                    if seq[i][0]==seq[i][1]:
                        deli.add(i)
                        #print("AN",i,deli)
                    break
    seqq2=[]
    #print(deli)
    for i in range(len(seq)):
        if i in deli:
            continue
        seqq2.append(seq[i])
    return seqq2

if __name__ == "__main__":
    piles=np.full((4,14), [" "], dtype='object')
    soup = BeautifulSoup(open("sort-ball.html"), "html.parser")
    balls=soup.find_all('div',{'class': "ball"})
    for b in range(len(balls)):
        i=3-b%4
        j=b//4
        try:
            piles[i][j]=balls[b]['class'][3]+balls[b]['class'][4].split('-')[1]
        except:
            piles[i][j]=balls[b]['class'][3]
    showPiles(piles)
    #stack.append(piles)
    #bfs(piles,0)
    dfs(piles,0)
    seq2=seqq
    seq3=fining(seq2)
    while(seq2!=seq3):
        seq2=seq3
        seq3=fining(seq3)
        print("****")
    #seq3=fining2(seq)
    for i in seq3:
        print("From "+str(i[0]+1)+"   To "+str(i[1]+1))