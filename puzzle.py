import numpy as np
from bs4 import BeautifulSoup
import requests
import os
import time
from selenium import webdriver
from utils import Pile, Piles, State
import heapq

#URL='https://sumx.ir'
#headers={'User-Agent': 'Chrome/39.0.2171.95'}


def dfs(piles):
    stack = [[i,0,-1] for i in p.available_actions()]
    
    p.set_state()
    
    while(len(stack)):
      action, level, order = stack[-1]
      #print(action)
      #time.sleep(2)
      if order>=0:
        stack.pop()
        p.undo_action(action)
        continue
      stack[-1][-1] += 1
      p.perform_action(action)
      #time.sleep(2)
      ret = p.set_state()
      if ret == -1:
        stack.pop()
        p.undo_action(action)
        continue
      state = p.get_state()
      state.visited+=1
      if p.is_win_state():
        break
      if p.get_state().visited > 1:
        stack.pop()
        p.undo_action(action)
        continue
      available_actions = sorted(p.available_actions())
      if len(available_actions)==0:
        stack.pop()
        p.undo_action(action)
        continue
      #stack = [[action, level+1, -1] for action in available_actions] + stack
      for actions in available_actions:
        stack.append([actions, level+1, -1])
    
    return [i[0] for i in stack if i[-1]>=0]
        
def parse_html(html):
    print("HEY")
    piles=np.full((4,14), [" "], dtype='object')
    soup = BeautifulSoup(open(html), "html.parser")
    balls=soup.find_all('div',{'class': "ball"})
    for b in range(len(balls)):
        i=3-b%4
        j=b//4
        try:
            piles[i][j]=balls[b]['class'][3]+balls[b]['class'][4].split('-')[1]
        except:
            piles[i][j]=balls[b]['class'][3]
    return piles
   
if __name__ == "__main__":
    
    piles = parse_html("sort-ball.html")
    
    p = Piles()
    for i in range(14):
      p.add_pile(Pile(piles[:,i]))
    p.set_original_piles()
    #p.show_piles()
    ans = dfs(p)
    print("Total Steps: {}".format(len(ans)))
    with open('output'+str(len(ans))+'.txt', 'w') as f:
      for step in ans:
        f.write(str(step)+'\n')
    #for step in ans:
     #   print(step)