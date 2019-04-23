from collections import deque
import random

class Robot:

   def __init__(self):

       self.direction = 'right'

       self.currentPos = (0, 0)

       self.grabbed = False

       self.nextMove = deque()

       self.Found_product = False

       self.back = False
   def getAction(self, bump):

       if bump:


   def takeMove(self, move):
       # qprint("direction: "+self.direction)
       if self.back == True:

   # def uTurn(self):
   #     actionL = [Agent.Action.TURN_LEFT,Agent.Action.TURN_LEFT]

   def construct_graph(self):
       path_graph = dict()
       for position in self.currentPos_list:
           path_graph[position] = set()
       for key in path_graph:
           for position in self.currentPos_list:
               if position[0] == key[0] - 1 and position[1] == key[1]:
                   path_graph[key].add(position)
               elif position[0] == key[0] + 1 and position[1] == key[1]:
                   path_graph[key].add(position)
               elif position[0] == key[0] and position[1] == key[1] + 1:
                   path_graph[key].add(position)
               elif position[0] == key[0] and position[1] == key[1] - 1:
                   path_graph[key].add(position)
       return path_graph

   def shortest_path(self, graph, start, goal, path = None):
       # print(start,goal)
       if path is None:
           path = list()
       path = path + [start]
       if start == goal:
           self.found_shorest_back = True
           return path
       if start not in graph:
           return None
       # shortest = None
       paths = []
       for node in graph[start]:
           if not self.found_shorest_back:
               if node not in path:
                   new_path = self.shortest_path(graph, node, goal, path)
                   for p in new_path:
                       paths.append(p)
       return paths



