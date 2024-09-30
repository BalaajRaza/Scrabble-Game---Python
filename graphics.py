# Add the graphics (turtle) related code in this file
from turtle import Turtle,Screen,TK
import itertools
import random
import os
import json
from players import *
from tiles import *
from game import *
from data import game_data

initial_ys = [300 , 200 , 100 , 0]



pickedTile = ""
# Class for a single box of board
class BoardBox:
    def __init__(self, x, y, color, box_id):
        self.x = x
        self.y = y
        self.color = color
        self.value = ''
        self.id = box_id

    def draw(self, turtle, cellsize):
        self.cellsize = cellsize
        turtle.penup()
        turtle.goto(self.x, self.y)
        turtle.pendown()
        turtle.color("black", self.color)
        turtle.begin_fill()
        for _ in range(4):
            turtle.forward(cellsize)
            turtle.right(90)
        turtle.end_fill()

        if self.value:
            turtle.penup()
            turtle.goto(self.x + cellsize / 2, self.y - cellsize)
            turtle.pendown()
            turtle.write(self.value, align="center", font=("Poppins", 15, "normal"))

    def set_value(self, value):
        self.value = value

    def is_clicked(self, click_x, click_y, cellsize):
        box_right = self.x + cellsize
        box_bottom = self.y - cellsize
        return self.x <= click_x <= box_right and box_bottom <= click_y <= self.y

# Class for complete board
class ScrabbleBoard :
    def __init__(self , width , height, cellsize,game):
        self.width = width
        self.height = height
        self.cellsize = cellsize
        self.game = game
        self.screen = Screen()
        self.screen.tracer(0)
        self.screen.setup(width=width, height=height)
        self.screen.title("Scrabble")
        self.screen.bgcolor("gray10")
        self.turtle = Turtle()
        self.turtle.speed(0.7)
        self.turtle.hideturtle()
        self.turtle.pensize(3)
        self.screen.onscreenclick(self.handle_Click)
        self.boardBoxes = []
        self.initializeBoard()
        self.turnCount = 0
        self.placed_tiles = []
        self.made_words = []
        self.submit_button_position = (self.width // 2 +100 , -self.height // 2 + 300)
        self.hint_button_position = (self.submit_button_position[0] - 200, self.submit_button_position[1] )
        self.draw_submit_button()
        self.draw_hint_button()
        #self.highlight_player(self.game.players[0] ,(self.cellsize * 15 + 100) - self.width / 2, 300 )

    def draw_hint_button(self):
        x , y  = self.hint_button_position[0], self.hint_button_position[1]
        self.turtle.penup()
        self.turtle.goto(x , y)
        self.turtle.pendown()
        self.turtle.color("gray10" ,"azure")
        self.turtle.begin_fill()
        for _ in range(2):
            self.turtle.forward(100)
            self.turtle.right(90)
            self.turtle.forward(50)
            self.turtle.right(90)
        self.turtle.end_fill()

        self.turtle.penup()
        self.turtle.penup()
        self.turtle.goto(x + 50, y - 38)
        self.turtle.pendown()
        self.turtle.write("Hint", align="center", font=("Roboto", 14, "bold"))
        self.screen.update()

    def display_message(self, message):
        hint = Turtle()
        hint.hideturtle()
        hint.penup()
        hint.goto(self.hint_button_position[0] + 50, self.hint_button_position[1]+20)
        hint.pendown()
        hint.color("azure")
        hint.write(message, align="center", font=("Roboto", 14, "bold"))
        #self.screen.ontimer(self.clear_message , 5000)
        hint.getscreen().ontimer(hint.clear , 3000)
    
    def clear_message(self):
        self.turtle.penup()
        self.turtle.goto(self.hint_button_position[0]-50, self.hint_button_position[1]+20)
        self.turtle.pendown()
        self.turtle.color("gray10")
        self.turtle.write(" " * len("No hints for you :( "), align="center", font=("Roboto", 14, "bold"))
        self.screen.update()

    def give_hint(self):
        print("Checking hints....")
        print(f"Made Words : {self.made_words}")
        current_player = self.game.players[self.turnCount % len(self.game.players)]

        if current_player.hints_left <= 0:
            self.display_message("No hints for you :( ")
            return
        current_player.hints_left -= 1
        possible_words = []
        tile_values = [tile.tileValue for tile in current_player.tiles]

        for word in self.made_words:
            for i in range(1 , 3):
                for combination in itertools.combinations(tile_values , i):
                    tile_string = ''.join(combination)

                    postfix_word = word + tile_string
                    print(f"PostFix Words : {postfix_word}")
                    if postfix_word in words:
                        possible_words.append(postfix_word)
                        postfix_score = self.calculate_word_score(postfix_word)

                    prefix_word = tile_string + word
                    print(f"PreFix Words : {prefix_word}")
                    if prefix_word in words:
                        possible_words.append(prefix_word)
                        prefix_score = self.calculate_word_score(prefix_word)
                    
            for i in range(1,3):
                for combination2 in itertools.combinations(tile_values , i):
                    pre = ''.join(combination2)
                    for j in range(1,3):
                        for combination3 in itertools.combinations(tile_values , j):
                            post = ''.join(combination3)
                            new_word = pre + word + post
                            print(f"Post + Pre Fix Word : {new_word}")
                            if new_word in words:
                                possible_words.append(new_word)
                                new_word_score = self.calculate_word_score(new_word)
                    
            print(f"Possible Words : {possible_words}")

        if possible_words:
            bestWord = max(possible_words , key = lambda x : x[1])
            print(f"BestWord : {bestWord}")
            self.display_message(f"Hint: {bestWord} for score {self.calculate_word_score(bestWord)}")
        
        else:
            self.display_message("No possible words")
            

    def calculate_word_score(self,word):
        total_score = 0
        for letter in word:
            letter_score = next((item["score"] for item in game_data["alphabet_score"] if item["alphabet"] == letter), 0)
            total_score += letter_score
        return total_score

    def draw_submit_button(self):
        x, y = self.submit_button_position
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.turtle.pendown()
        self.turtle.color("gray10", "azure")
        self.turtle.begin_fill()
        for _ in range(2):
            self.turtle.forward(100)
            self.turtle.right(90)
            self.turtle.forward(50)
            self.turtle.right(90)
        self.turtle.end_fill()

        self.turtle.penup()
        self.turtle.goto(x + 50, y - 38)
        self.turtle.pendown()
        self.turtle.write("Submit", align="center", font=("Roboto", 14, "bold"))
        self.screen.update()

    def initializeBoard(self):
        colors = ["orangered", "lawngreen", "gold", "deepskyblue2"]
        x = -self.width / 2
        y = self.height / 2
        box_id = 1

        for i in range(15):
            row = []
            for j in range(15):
                color = random.choice(colors)
                box = BoardBox(x, y, color, box_id)
                row.append(box)
                box_id += 1
                x += self.cellsize
            self.boardBoxes.append(row)
            x = -self.width / 2
            y -= self.cellsize

        self.drawGrid()

    def drawGrid(self):
        for row in self.boardBoxes:
            for box in row:
                box.draw(self.turtle, self.cellsize)

    def drawTile(self,x,y,tile):
        tile.x = x
        tile.y = y
        tile.cellsize = self.cellsize
        if tile.color == '':
            tile.color = random.choice(colors)
        tile.draw(self.turtle)


    def showPlayer(self,player,x,y):
        self.turtle.penup()
        self.turtle.goto(x,y)
        self.turtle.pendown()
        self.turtle.color("azure2")
        self.turtle.write(player.name+": "+str(player.score), font=("Arial", 12, "normal"))
        for i,tile in  enumerate(player.tiles):
            if tile.tileValue :
                self.turtle.color('black')
                self.drawTile(x+(self.cellsize*i) , y,tile)
                
    def highlight_player(self,player,x,y):
        self.turtle.penup()
        self.turtle.goto(x,y+20)
        self.turtle.pendown()
        self.turtle.color("azure")
        self.turtle.write(f"{player.name}'s turn", font=("Roboto", 16,))

    def title(self):
        self.turtle.penup()
        self.turtle.goto((self.cellsize * 15 + 180) - self.width / 2, 360)
        self.turtle.pendown()
        self.turtle.color("azure")
        self.turtle.write("SCRABBLE", font=("Agency FB", 30, "normal"))

    def find_tile_by_cords(self, click_x, click_y, player):
        for tile in player.tiles:
            tile_left = tile.x
            tile_right = tile.x + self.cellsize
            tile_top = tile.y
            tile_bottom = tile.y - self.cellsize

            if tile_left <= click_x <= tile_right and tile_bottom <= click_y <= tile_top:
                return tile
        return None


    def handle_Click(self, x, y):
        global pickedTile
        print(f"Clicked at: ({x},{y})")

        current_player = self.game.players[self.turnCount % len(self.game.players)]
        
        if current_player.isTurn:
            tile = self.find_tile_by_cords(x , y , current_player)
            if tile:
                pickedTile = tile.tileValue
                self.removeTilefromDisplay(current_player, tile)
        
        if self.is_submit_button_clicked(x, y):
            self.submit_word()
        
        if self.is_hint_clicked(x,y):
            self.give_hint()
        else:
            self.boxClick(x, y)
        
        self.redraw()
    
    def is_submit_button_clicked(self, click_x, click_y):
        x, y = self.submit_button_position
        button_right = x + 100
        button_top = y
        button_bottom = y - 50
        return x <= click_x <= button_right and button_bottom <= click_y <= button_top
    
    def is_hint_clicked(self , click_x , click_y):
        x , y = self.hint_button_position
        button_right = x + 100
        button_top = y
        button_bottom = y - 50
        return x <= click_x <= button_right and button_bottom <= click_y <= button_top
    
    def submit_word(self):
        current_player = self.game.players[self.turnCount % len(self.game.players)]
        if self.valid_word():
            self.updateScore()
            self.replace_tiles()
            #current_player.replaceEmptyTiles() 
        else:
            self.returnTiles() 
        
        self.end_turn()
        self.redraw()

    def end_turn(self):
        current_player =  self.game.players[self.turnCount % len(self.game.players)]
        current_player.turn_count += 1

        if self.check_game_ended():
            self.end_game()
            return

        self.turnCount += 1
        for player in self.game.players:
            player.isTurn = False

        current_player = self.game.players[self.turnCount % len(self.game.players)]
        current_player.isTurn = True
        print(f"It's now {current_player.name}'s turn!")
        self.redraw()
    

    def boxClick(self,x,y):
        global pickedTile
        box = self.find_box_by_cords(x, y)
        if box:
            if box.value == '':
                if pickedTile == '-':
                    pickedTile = self.screen.textinput("Choose a letter" , "Enter a letter to replace blank tile:")
                    if len(pickedTile) != 1 or not pickedTile.isalpha():
                        pickedTile = '-'
                        return 

                box.set_value(pickedTile)
                self.placed_tiles.append(box)
                pickedTile = ""
                self.redraw()   

    def removeTilefromDisplay(self,player,tile):
        player.removeTile(tile)
        self.redraw()

    def redraw(self):
        self.turtle.clear()
        self.drawGrid()
        self.draw_submit_button()
        self.draw_hint_button()
        for i,p in enumerate(self.game.players):
            self.showPlayer(p, (self.cellsize * 15 + 50) - self.width/2, 300 - (i * 100))
        
        current_player = self.game.players[self.turnCount % len(self.game.players)]
        self.highlight_player(current_player, (self.cellsize * 15 + 50) - self.width / 2, 300)
        self.title()
        self.screen.update()

    def find_box_by_cords(self, click_x, click_y):
        for row in self.boardBoxes:
            for box in row:
                if box.is_clicked(click_x, click_y, self.cellsize):
                    return box
        
        return None

    def valid_word(self):

        h_word = self.get_h_word()
        v_word = self.get_v_word()

        valid_word = False

        if h_word and (h_word in words):
            valid_word = True

        if v_word and v_word in words:
            valid_word = True
        
        return valid_word

    def get_box_at(self,x,y):
        for row in self.boardBoxes:
            for box in row:
                if box.x == x and box.y == y:
                    return box
        return None


    def get_h_word(self):
        word = []
        if self.placed_tiles:
            sorted_by_x = sorted(self.placed_tiles , key=lambda box : box.x)
            current_box = sorted_by_x[0]

            while current_box and self.box_is_filled(current_box):
                current_box = self.get_box_at(current_box.x - self.cellsize , current_box.y)
                if current_box is None or current_box.value == '':
                    break
                
            current_box = self.get_box_at(current_box.x + self.cellsize , current_box.y)

            while current_box and self.box_is_filled(current_box):
                word.append(current_box.value)
                current_box = self.get_box_at(current_box.x + self.cellsize , current_box.y)
                if current_box is None or current_box.value == '':
                    break

            return (''.join(word))


    def get_v_word(self):
        word = []
        if self.placed_tiles:
            sorted_by_y = sorted(self.placed_tiles , key=lambda box : box.y , reverse=True)
            current_box = sorted_by_y[0]

            while current_box and self.box_is_filled(current_box):
                current_box = self.get_box_at(current_box.x, current_box.y + self.cellsize)
                if current_box is None or current_box.value == '':
                    break
                
            current_box = self.get_box_at(current_box.x , current_box.y - self.cellsize)

            while current_box and self.box_is_filled(current_box):
                word.append(current_box.value)
                current_box = self.get_box_at(current_box.x , current_box.y - self.cellsize)
                if current_box is None or current_box.value == '':
                    break
            
            return (''.join(word))

    def box_is_filled(self, box):
        if box.value!='':
            return True
        else:
            return False
        
    
    def updateScore(self):
        current_player = self.game.players[self.turnCount % len(self.game.players)]
        total_score = 0
        h_word = self.get_h_word()
        
        if h_word and h_word in words:
            h_word_score = sum(self.getTileScore(letter) for letter in h_word)
            total_score += h_word_score
            self.add_word_to_json(current_player.name , h_word , h_word_score)
            words.remove(h_word)

        v_word = self.get_v_word()
        if v_word and v_word in words:
            v_word_score = sum(self.getTileScore(letter) for letter in v_word)
            total_score += v_word_score
            self.add_word_to_json(current_player.name , v_word , v_word_score)
            words.remove(v_word)

        current_player.score += total_score

        self.redraw()

    def getTileScore(self,letter):
         return next(item['score'] for item in game_data['alphabet_score'] if item['alphabet'] == letter)

    def replace_tiles(self):
        current_player = self.game.players[self.turnCount % len(self.game.players)]

        for i,tile in enumerate(current_player.tiles) :
            if tile.tileValue == '' :

                if tiles:
                    color = random.choice(colors)
                    tilevalue = random.choice(tiles)
                    tiles.remove(tilevalue)
                    newTile = Tiles(tile.x,tile.y,self.cellsize , color , tilevalue)
                    current_player.tiles[i] = newTile
                else:
                    print("No more tiles available")
            
        self.placed_tiles = []
        self.redraw()

    def returnTiles(self):
        current_player = self.game.players[self.turnCount % len(self.game.players)]
        
        start_x = (self.cellsize * 15 + 50) - self.width / 2
        start_y = initial_ys[self.turnCount % len(self.game.players)]
        
        for i, box in enumerate(self.placed_tiles):
            for tile in current_player.tiles:
                if tile.tileValue == '': 

                    tile_value = box.value 
                    tile.x = start_x + (self.cellsize * i) 
                    tile.y = start_y
                    tile.tileValue = tile_value
                    tile.color = random.choice(colors)
                    break
            box.set_value('')

        self.placed_tiles = []

        self.redraw()

    def check_game_ended(self):
        all_player_turns_done = all(player.turn_count>=5 for player in self.game.players)

        tile_bag_empty = (len(tiles) == 0)
        all_tiles_used = all(not player.tiles for player in self.game.players)

        if all_player_turns_done or (tile_bag_empty and all_tiles_used):
            return True
        
        return False

    def end_game(self):
        self.turtle.clear()
        self.turtle.penup()
        self.turtle.goto(0,150)
        self.turtle.pendown()
        self.turtle.write("--Game Over--" , align="center" , font = ("Poppins" , 25 , "bold"))

        winner = self.check_winner()
        self.turtle.penup()
        self.turtle.goto(0,100)
        self.turtle.pendown()
        self.turtle.write(f"Winner: {winner.name}" , align="center" , font =("Poppins" , 20 , "bold"))


        for i, player in enumerate(self.game.players):
            self.turtle.penup()
            self.turtle.goto(0 , -i*30)
            self.turtle.pendown()
            self.turtle.write(f"{player.name} : {player.score} points" , align="center", font=("Poppins", 15, "normal"))

        self.screen.update()
        self.write_winner_data()
        self.screen.exitonclick()

    def add_word_to_json(self, player_name , word , score):
        folder_name = "game"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        player_file = os.path.join(folder_name , f"{player_name}.json")

        if os.path.exists(player_file):
            with open(player_file , "r") as file:
                player_data = json.load(file)
        else:
            player_data = {}
        
        player_data[word] = str(score)
        self.made_words.append(word)

        with open(player_file , 'w') as file:
            json.dump(player_data,file,indent=4)
    
    def check_winner(self):
        winner = max(self.game.players , key = lambda player : player.score)
        return winner
    
    def get_winner_data(self):
        winner = self.check_winner()
        winner_file = os.path.join("game" , f"{winner.name}.json")
        with open(winner_file , "r") as file:
            return json.load(file)
    
    def write_winner_data(self):
        winner_data = self.get_winner_data()
        winner = self.check_winner().name
        with open("winner.txt" , "w") as file:
            file.write(f"Winner : {winner}")
            for word in winner_data.items():
                file.write(f"\n{word[0]} : {word[1]}")
        


    def loop(self):
        self.screen.mainloop()