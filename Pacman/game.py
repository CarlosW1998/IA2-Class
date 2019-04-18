import arcade
from maze import make_maze
from states import State, AgentState
from random import randint
from agents import Player, Gosth, Coin
from heapq import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pacman"


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.size_block = 20
        self.maze = make_maze(width//(self.size_block*3), height//(self.size_block*2))
        self.agents = []
        self.coins = []
        self.player = None
        

    def setup(self):
        # Create your sprites and sprite lists here
        self.agents = []
        self.coins = []
        self.state = State.MAIN_MENU
        
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j] == 0 and randint(0, 100) > 95:
                    self.coins.append(Coin(j, i, self.size_block // 5, self.size_block))
        
        y = randint(0, len(self.maze)-1)
        x = randint(0, len(self.maze[0])-1)
        while self.maze[y][x] == 1:
            y = randint(0, len(self.maze)-1)
            x = randint(0, len(self.maze[0])-1)
        self.player = Player(x, y, self.size_block//4, self.size_block)
        arcade.set_background_color(arcade.color.BLACK_OLIVE)
        
        for i in range(10):
            y = randint(0, len(self.maze)-1)
            x = randint(0, len(self.maze[0])-1)
            while self.maze[y][x] == 1:
                y = randint(0, len(self.maze)-1)
                x = randint(0, len(self.maze[0])-1)
            self.agents.append(Gosth(x, y, self.size_block // 4, self.size_block, self.maze))
            #self.agents.push(Gosth(x + (self.size_block // 2), y + (self.size_block // 2), self.size_block // 4)
        
    
    def drow_maze(self):
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j] == 1:
                    arcade.draw_point(j*self.size_block, i*self.size_block, arcade.color.BLUE, self.size_block)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()
        if self.state == State.MAIN_MENU:
            arcade.draw_text("Press ENTER to play", 3, 405, arcade.color.BLACK, 50)
        
        if self.state == State.PLAYING:
            self.drow_maze()
            for i in self.coins:
                i.drawn()
            for i in self.agents:
                i.drawn()
            self.player.drawn()
        if self.state == State.GAME_OVER:
            arcade.draw_text("Press ENTER to play Agin", 3, 405, arcade.color.BLACK, 50)

        # Call draw() on all your sprite lists below

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        if self.state == State.PLAYING:
            self.player.time += delta_time
            for i in self.agents:
                if i.x == self.player.x and i.y == self.player.y:
                    self.state = State.GAME_OVER
                    break

                elif ((i.x - self.player.x)**2 + (i.y - self.player.y)**2 )**(1/2) < 10 and i.state != AgentState.STALk:
                    print(id(i)," - Find Target: ", (self.player.x, self.player.y))
                    i.state = AgentState.STALk
                    i.target = (self.player.x, self.player.y)
                    i.trajecoty = i.getPath()
                    queue = []
                    for j in self.agents:
                        if i != j and ((i.x - j.x)**2 + (i.y - j.y)**2)**(1/2) <= 20 and j.state != AgentState.STALk:
                            print(id(j), ' - Recive Target: ', (self.player.x, self.player.y))
                            j.target = (self.player.x, self.player.y)
                            j.state = AgentState.STALk
                elif i.state == AgentState.STALk:
                    if ((i.x - self.player.x)**2 + (i.y - self.player.y)**2 )**(1/2) < 10 :
                        i.target = (self.player.x, self.player.y)   
                        i.trajecoty = i.getPath()
                    else:
                        i.state = AgentState.SEARCH
                else :
                    i.state = AgentState.SEARCH

                i.time += delta_time
            
                if i.time >= 0.75:
                    print(id(i)," - Find Target: ", (self.player.x, self.player.y))
                    if i.move():
                        queue = []
                        for j in self.agents:
                            if i != j and ((i.x - j.x)**2 + (i.y - j.y)**2)**(1/2) <= 20 and j.state != AgentState.STALk:
                                print(id(j), ' - Recive Target: ', (self.player.x, self.player.y))
                                j.target = (self.player.x, self.player.y)
                                j.state = AgentState.STALk
                        i.time = 0
        for i in range(len(self.coins)):
            if self.coins[i].x == self.player.x and self.coins[i].y == self.player.y:
                self.coins.pop(i)
                self.player.score += 10
                break


    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """

        if key == arcade.key.SPACE and self.state == State.MAIN_MENU:
            # If the game is starting, just change the state and return
            self.state = State.PLAYING
            return
        if key == arcade.key.SPACE and self.state == State.GAME_OVER:
            # If the game is starting, just change the state and return
            self.setup()
            self.state = State.PLAYING
            return
        
        if self.state == State.PLAYING:
            if key == arcade.key.D and self.player.time > 0.2:
                if self.player.move(1, self.maze):
                    self.player.time = 0
            if key == arcade.key.A and self.player.time > 0.2:
                if self.player.move(2, self.maze):
                    self.player.time = 0
            if key == arcade.key.W and self.player.time > 0.2:
                if self.player.move(3, self.maze):
                    self.player.time = 0
            if key == arcade.key.S and self.player.time > 0.2:
                if self.player.move(4, self.maze):
                    self.player.time = 0


    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
