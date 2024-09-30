#This file stores player informations.
import random
from data import *
from tiles import *


class Player:
    def __init__(self, name,n):
        self.name = name
        self.score = 0
        self.n = n # number of tiles player gets
        self.tilesValues = []
        self.tiles = []
        self.isTurn = False
        self.turn_count = 0
        self.hints_left = 2
        self.words = {}
        for i in range(0,n):
            tile_value = random.choice(tiles)
            tiles.remove(tile_value)
            self.tilesValues.append(tile_value)
            self.tiles.append(Tiles(0,0,0,'',tile_value))
    
    def addTile(self,tile):
        self.tiles.append(tile)
    
    def removeTile(self, tile):
        for i, t in enumerate(self.tiles):
            if t == tile:
                dummy_tile = Tiles(t.x, t.y, self.tiles[i].cellsize, "white", '')
                self.tiles[i] = dummy_tile
                break
    
    def replaceEmptyTiles(self):
        print("Replacing Empty Tiles")
        for tile in self.tiles:
            if tile.tileValue == '0':
                if tiles:
                    tile_value = random.choice(tiles)
                    tiles.remove(tile_value)
                    color = random.choice(colors)
                    newTile = Tiles(tile.x , tile.y,tile.cellsize , color , tile_value)
                    tile = newTile
    
    def addWord(self,word,score):
        self.words[word] = score
        
        