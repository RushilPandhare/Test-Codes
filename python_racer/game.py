import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

#reset
#reward
#play(action)
#game_iteration
#collision function

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y') #Can access them as Point.x and Point.y
#combined x and y into 1 string as namedtuple only takes 2 positional args, so if we add x & y seperate, then it will become 3


# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 10 #The higher the number the faster your game is

class SnakeGameAI:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
        
       
    def reset(self):#refactoring the init game state for the reset function
         # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE  #random integer between 0 & width - BLOCK_SIZE and obtain multiples of the prev thing using "//BLOCK_SIZE)*BLOCK_SIZE"
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self, action): #need to give action & reward
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
           
        
        # 2. move
        self._move(action) #This should update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward,game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food: #if snake hits the food, score increases as well as reward = +10
            self.score += 1
            reward = 10
            self._place_food() #then new food placed
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score
    
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself(if point is in the snake body then there will be a collision else no collision)
        if pt in self.snake[1:]:#This will happen when the player moves the snake exactly to the opposite of its current direction
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK) #filled the screen with colour black
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, action): #not getting action from user input so removed direction
        #[straight , right , left]

        #the snake will move according to clockwise when not following food
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1,0,0]): #keep current direction/straight
            new_dir = clock_wise[idx] #no change
        elif np.array_equal(action, [0,1,0]):
           next_idx = (idx + 1) % 4 # to loop the directions after up
           new_dir = clock_wise[next_idx] # right turn
        #if we go right, then if we start with a right, the next direction will be down --> left --> up according to how its defined in clockwise
        else: #[0,0,1]
            next_idx = (idx - 1) % 4 # goes counter clockwise
            new_dir = clock_wise[next_idx] # f we go left, then if we start with a right, the next direction will be up --> left --> down then right and so on 
        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        # where block size is a value which defines how big the size of a snake should be in pixels
            
        self.head = Point(x, y)
            

# if __name__ == '__main__':
#     game = SnakeGameAI()
    
#     # game loop
#     while True:
#         game_over, score = game.play_step()
        
#         if game_over == True:
#             break
        
#     print('Final Score', score)
        
        
#     pygame.quit()