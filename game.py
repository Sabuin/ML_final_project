import pygame

import agent_config
import config
from sprites import *
from config import *
import sys
import time

def max(val1, val2):
   if(val1 > val2):
      return val1
   else:
      return val1

class Game:
   def __init__(self):
      pygame.init()
      self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
      self.clock = pygame.time.Clock()

   def createTilemap(self):
      for i, row in enumerate(tilemap):
         for j, column in enumerate(row):
            if column == "W":
               self.block = Block(self,j,i)
            if column == "P":
               self.player = Player(self, j, i) #(self, x_axis, y_axis)
            if column == "E":
               self.enemy = Enemy(self, j, i) #(self, x_axis, y_axis)
            

   def new(self):
      self.playing = True
      self.all_sprites = pygame.sprite.LayeredUpdates() #object contains all sprites in the game
      self.blocks = pygame.sprite.LayeredUpdates()
      self.enemies = pygame.sprite.LayeredUpdates()
      self.attacks = pygame.sprite.LayeredUpdates()
      self.projectiles = pygame.sprite.LayeredUpdates()

      self.createTilemap()

      self.score = 0

      self.fireTime = 0
      self.duration = 0

   def agent_move(self, action):
      if action[0]:
         self.player.x_change -= PLAYER_SPEED
         self.player.facing = 'left'

      if action[1]:
         self.player.x_change += PLAYER_SPEED
         self.player.facing = 'right'

      if action[2]:
         self.player.y_change -= PLAYER_SPEED  # in pygame, y axis starts at the top at 0.
         self.player.facing = 'up'

      if action[3]:
         self.player.y_change += PLAYER_SPEED
         self.player.facing = 'down'

      if action[4]:
         if self.player.facing == "up":
            angle = 90
         elif self.player.facing == "down":
            angle = 270
         elif self.player.facing == "left":
            angle = 180
         elif self.player.facing == "right":
            angle = 0

         if(self.fireTime < 0):
            projectile = Attack(self, self.player.rect.x, self.player.rect.y, angle)
            self.projectiles.add(projectile)
            self.fireTime += config.PROJECTILE_INTERVAL
      self.fireTime -= self.clock.get_time()


      # Update player position
      self.player.rect.x += self.player.x_change
      self.player.rect.y += self.player.y_change


   def update(self):
      reward = 0
      self.player.update()
      self.enemy.update()

      for bullet in self.projectiles:
         value = bullet.update()
         if(value != None):
            reward += bullet.update()

      if(reward == 0):
         reward = agent_config.IDLE_PENALTY

      return reward


   def draw(self):
      self.screen.fill(BLACK)
      self.all_sprites.draw(self.screen) #drawing the sprites in window
      self.clock.tick(FPS)
      pygame.display.update()



   def events(self, action):
      #Game loop events
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            self.playing = False

      reward = self.update()
      self.draw()

      self.agent_move(action)
      self.duration += self.clock.get_time()

      if(self.duration > (agent_config.DURATION_MOD * max(1, config.ENEMY_HP - self.enemy.hp))):
         self.playing = False
         reward = agent_config.TIMEOUT_PENALTY


      return reward, not self.playing


g = Game()
g.new()



# pygame.quit()
# sys.exit()
