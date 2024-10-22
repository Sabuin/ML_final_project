import pygame
from sprites import *
from config import *
import sys
import time

class Game:
   def __init__(self):
      pygame.init()
      self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
      self.clock = pygame.time.Clock()
      self.running = True

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

   def events(self):
      #Game loop events
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            self.playing = False
            self.running = False 
         
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
               if self.player.facing == "up":
                  angle = 90
               elif self.player.facing == "down":
                  angle = 270
               elif self.player.facing == "left":
                  angle = 180
               elif self.player.facing == "right":
                  angle = 0
               projectile = Attack(self,self.player.rect.x, self.player.rect.y, angle)
               self.projectiles.add(projectile)
   

   def update(self):
      self.all_sprites.update()

   def draw(self):
      self.screen.fill(BLACK)
      self.all_sprites.draw(self.screen) #drawing the sprites in window
      self.clock.tick(FPS)
      pygame.display.update()

   def main(self):

      #game loop 
      while self.playing:
         self.events()
         self.update()
         self.draw()

      self.running = False

   def game_over(self):
      pass

   def intro_screen(self):
      pass


g = Game()
g.intro_screen()
g.new()
while g.running:
   g.main()
   g.game_over()

pygame.quit()
sys.exit()
