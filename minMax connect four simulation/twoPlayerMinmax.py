from two_player_games.player import Player
import unittest
from two_player_games.games.connect_four import ConnectFour
from two_player_games.games.connect_four import ConnectFourMove, ConnectFourState
import math 
import copy
import random

def minimax(node:ConnectFour, depth, pMax,a,b):
    if depth == 0 or node.is_finished():
        #print("Taka jest wartosc konowa w koncowym ruchu: " + str(node.get_score(p1t, p2t)))
        return node.get_score(pMax)
    if node.get_current_player() == pMax:
        value = -1000000
        for i in range(len(node.get_moves())):
            temp = copy.copy(node)
            temp.make_move(node.get_moves()[i])
            #print(str(temp))
            value = max(value, minimax(temp,depth-1,pMax,a,b))
            a = max(value,a)
            if value >= b:
                break
        #print("Dla gracza max glebokosci takiej: " + str(depth) + " jest taka wartosc: " + str(value))
        return value
    else:
        value = 1000000
        for i in range(len(node.get_moves())):
            temp = copy.copy(node)
            temp.make_move(node.get_moves()[i])
            value = min(value, minimax(temp,depth-1, pMax,a,b))
            b = min(value, b)
            if value <= a:
                break
        #print("Dla gracza min glebokosci takiej: " + str(depth) + " jest taka wartosc: " + str(value))
        return value



p1Max = Player('1')
p2Min = Player('2')
depth1 = 3
depth2 = 6
moduloFlag = 0
howManyTimes1Won = 0
howManyTimes2Won = 0
howManyTimesTied = 0
jiterToMeanWin = 0
jiterToMeanLose = 0
jiterToMeanTie = 0

flagIfCPUisOn = 'n'#flagIfCPUisOn = input("Czy chcesz grac z AI? [y/n]: ")

game = ConnectFour(first_player=p1Max, second_player=p2Min)

for iter in range(20):
    game = ConnectFour(first_player=p1Max, second_player=p2Min)
    jiter = 0
    while game.is_finished() == False and jiter<100:
        moduloFlag+=1
        jiter+=1
        if moduloFlag==1:
            depth = depth1
        else:
            moduloFlag = 0
            depth = depth2
        
        biggestValue = - 1000000
        #moveChoice = 0
        if game.get_moves() == None:
            howManyTimesTied += 1
            jiterToMeanTie += jiter
            print("Remis - jest to iteracja nr " + str(iter))
            break
        else:
            for i in range(len(game.get_moves())):
                temp = copy.copy(game)
                temp.make_move(game.get_moves()[i])
                value = minimax(temp,depth,game.get_current_player(),-1000000, 1000000)
                #print(str(temp))
                #print("Wartosc tego ruchu to: " + str(value))
                if value > biggestValue:
                    biggestValue = value
                    moveChoice = game.get_moves()[i]
                elif value == biggestValue:
                    moveChoice = random.choice([moveChoice,game.get_moves()[i]])
            
        #print("mam wybrac: " + str(columnChoice))
        game.make_move(moveChoice)
        ##print(str(game))
        if flagIfCPUisOn=='y':
            playerChoiceColumn= int(input("Enter index of column to put your token: "))
            game.make_move(ConnectFourMove(playerChoiceColumn))
            print(str(game))
            
    
    
    if game.get_winner() == p1Max: 
        howManyTimes1Won += 1
        jiterToMeanWin += jiter
        print("Wygral gracz nr 1 - jest to iteracja nr " + str(iter))
    elif game.get_winner() == p2Min:
        howManyTimes2Won += 1
        jiterToMeanLose += jiter
        print("Wygral gracz nr 2 - jest to iteracja nr " + str(iter))
    else:
        howManyTimesTied += 1
        jiterToMeanTie += jiter
        print("Remis - jest to iteracja nr " + str(iter))
#print(minimax(game,depth,p1Max,p2Min))

print("Gracz jeden z depth " + str(depth1) + " wygral tyle razy: " + str(howManyTimes1Won) + " z srednia ruchow " + str(jiterToMeanWin/howManyTimes1Won))
print("Gracz jeden z depth " + str(depth2) + " wygral tyle razy: " + str(howManyTimes2Won) + " z srednia ruchow " + str(jiterToMeanLose/howManyTimes2Won))
print("Remisow bylo: " + str(howManyTimesTied) + " z srednia ruchow " + str(jiterToMeanTie/howManyTimesTied))