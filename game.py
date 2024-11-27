import pygame

import agent_config
import config
from sprites import *
from config import *
import sys
import time
import numpy as np
import math

def max(val1, val2):
   if(val1 > val2):
      return val1
   else:
      return val1

class Game:
   def __init__(self):
      pygame.init()
      self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
      #self.clock = pygame.time.Clock()
      self.level = 0


   def createTilemap(self):
      for i, row in enumerate(tilemap):
         for j, column in enumerate(row):
            if column == "W":
               self.block = Block(self,j,i)
            if column == "P":
               if(self.level != 0):
                  self.players.remove(self.player)
               self.player = Player(self, j, i) #(self, x_axis, y_axis)
               self.players.add(self.player)
            if column == "E":
               if self.level == 0:
                  self.enemy = Enemy(self, j, i) #(self, x_axis, y_axis)
               elif self.level == 1:

                  self.all_sprites.remove(self.enemy)
                  self.enemies.remove(self.enemy)

                  self.enemy = Chaser(self, j, i)
               elif self.level == 2:

                  self.all_sprites.remove(self.enemy)
                  self.enemies.remove(self.enemy)

                  self.enemy = Drunkard(self, j, i)
               elif self.level == 3:

                  self.all_sprites.remove(self.enemy)
                  self.enemies.remove(self.enemy)

                  self.enemy = Sniper(self, j, i)
            

   def new(self):
      self.playing = True
      self.all_sprites = pygame.sprite.LayeredUpdates() #object contains all sprites in the game
      self.players = pygame.sprite.LayeredUpdates()
      self.blocks = pygame.sprite.LayeredUpdates()
      self.enemies = pygame.sprite.LayeredUpdates()
      self.attacks = pygame.sprite.LayeredUpdates()
      self.projectiles = pygame.sprite.LayeredUpdates()
      self.enemyProjectiles = pygame.sprite.LayeredUpdates()

      self.level = 0
      self.createTilemap()

      self.score = 0

      self.fireTime = 0
      self.enemyFiretime = 0
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
      # self.fireTime -= self.clock.get_time()
      self.fireTime -= 1

      # Update player position
      self.player.rect.x += self.player.x_change
      self.player.rect.y += self.player.y_change


   def update(self):
      '''
      Rewards we have:
      * If monster hit: +1
      * If monster kill: 0
      *
      * If idle: -.0001
      * If shoots in right direction: +.5

      :return:
      '''

      reward = 0
      self.player.update()
      self.enemy.update(self)

      for bullet in self.projectiles:
         value = bullet.update()
         if(value != None):
            reward += value

      for bullet in self.enemyProjectiles:
         value = bullet.update()
         if(value != None):
             reward += value

      if(self.enemyFiretime <= 0):
         bulletX = self.enemy.rect.x
         bulletY = self.enemy.rect.y
         if(self.level == 1):
            if(self.player.rect.y < self.enemy.rect.y):
               projectile = enemyAttack(self, bulletX, bulletY, 90)
            elif(self.player.rect.y > self.enemy.rect.y):
               projectile = enemyAttack(self, bulletX, bulletY, 270)
            elif(self.player.rect.x < self.enemy.rect.x):
               projectile = enemyAttack(self, bulletX, bulletY, 180)
            else:
               projectile = enemyAttack(self, bulletX, bulletY, 0)
            self.enemyProjectiles.add(projectile)

         elif(self.level == 2):
            offset = 15
            projectile = enemyAttack(self, bulletX, bulletY, 0 + offset)
            self.enemyProjectiles.add(projectile)
            projectile = enemyAttack(self, bulletX, bulletY, 45 + offset)
            self.enemyProjectiles.add(projectile)
            projectile = enemyAttack(self, bulletX, bulletY, 90 + offset)
            self.enemyProjectiles.add(projectile)
            projectile = enemyAttack(self, bulletX, bulletY, 135 + offset)
            self.enemyProjectiles.add(projectile)
            projectile = enemyAttack(self, bulletX, bulletY, 180 + offset)
            self.enemyProjectiles.add(projectile)
            projectile = enemyAttack(self, bulletX, bulletY, 225 + offset)
            self.enemyProjectiles.add(projectile)
            projectile = enemyAttack(self, bulletX, bulletY, 270 + offset)
            self.enemyProjectiles.add(projectile)
            projectile = enemyAttack(self, bulletX, bulletY, 315 + offset)
            self.enemyProjectiles.add(projectile)

         elif(self.level == 3):
            xDif = self.player.rect.x - self.enemy.rect.x
            yDif = self.enemy.rect.y - self.player.rect.y
            angle = math.atan2(yDif, xDif) * 180 / math.pi
            projectile = enemyAttack(self, bulletX, bulletY, angle)
            self.enemyProjectiles.add(projectile)

         self.enemyFiretime = ENEMY_FIRE_DELAY * self.level
      elif(self.enemyFiretime > 0):
         self.enemyFiretime -= 1

         # if(bullet.angle == 90 and self.enemy.y < self.player.y):
         #    reward += agent_config.NEAR_HIT
         # elif(bullet.angle == 0 and self.enemy.x > self.player.x):
         #    reward += agent_config.NEAR_HIT
         # elif(bullet.angle == 180 and self.enemy.y > self.player.y):
         #    reward += agent_config.NEAR_HIT
         # elif(bullet.angle == 270 and self.enemy.x < self.player.x):
         #    reward += agent_config.NEAR_HIT

      if(reward == 0):
         reward = agent_config.IDLE_PENALTY

      return reward


   def draw(self):
      self.screen.fill(BLACK)
      self.all_sprites.draw(self.screen) #drawing the sprites in window
      #self.clock.tick(FPS)
      pygame.display.update()


   def events(self, action):
      #Game loop events
      # for event in pygame.event.get():
      #    if event.type == pygame.QUIT:
      #       self.playing = False

      reward = self.update()
      self.draw()

      self.agent_move(action)
      # self.duration += self.clock.get_time()
      self.duration += 1

      if(self.duration > (agent_config.DURATION_MOD * max(1, config.ENEMY_HP - self.enemy.hp))):
         self.playing = False
         reward = agent_config.TIMEOUT_PENALTY

      for bullet in self.projectiles:
         if(bullet.x > WIN_WIDTH or bullet.x < 0 or bullet.y > WIN_HEIGHT or bullet.y < 0):
            bullet.kill()

      return reward, not self.playing


g = Game()
g.new()



# pygame.quit()
# sys.exit()
