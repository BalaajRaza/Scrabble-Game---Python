# Add the implementation logic code here
import pygame
from turtle import *
from graphics import *
from players import *
from game import *
from data import tiles

def play_music():
    pygame.mixer.init()
    pygame.mixer.music.load("game_music.mp3")
    pygame.mixer.music.set_volume(5)
    pygame.mixer.music.play(1)


WIDTH = 800
HEIGHT = 800
cellsize = 40
n = 10 # n is the number of tiles each player gets

start_x = -WIDTH/2
start_y = HEIGHT/2

play_music()
game = Game()
board = ScrabbleBoard(WIDTH,HEIGHT,cellsize,game)
#board.drawGrid()
board.title()

for i in range (0,4):
    player_name = textinput("Enter Player Names" , f"Player{i+1}")
    player = Player(player_name,n)
    game.addPlayer(player)
    board.showPlayer(player , (cellsize*15 + 50)-WIDTH/2 , 300 - (i*100) )
    

game.players[0].isTurn = True
board.highlight_player(game.players[0] , (cellsize * 15 + 50) - WIDTH / 2, 300)


print("Starting the game.")
board.loop()

