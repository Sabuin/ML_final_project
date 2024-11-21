import pygame
import agent_config
from config import *
import math
import random
import time

class Player(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height]) #how it looks
        self.image.fill(PINK)

        self.rect = self.image.get_rect() #the hitbox
        self.rect.x = self.x
        self.rect.y = self.y

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'

        self.hp = PLAYER_HP

    def update(self):
        self.movement()
        #self.collide_enemies()

        self.rect.x += self.x_change
        self.collide_blocks('x')

        self.rect.y += self.y_change
        self.collide_blocks('y')

        #temporary variables
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        pass

    def collide_blocks(self,direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
    
    # def collide_enemies(self):
    #    hits = pygame.sprite.spritecollide(self,self.game.enemies,False)
    #    if hits:
    #        self.kill()
    #        self.game.playing = False

    def take_damage(self, damage):
        self.hp -= damage
        agent_config.SCORE += agent_config.PLAYER_HIT

        if self.hp <= 0:
            agent_config.SCORE += agent_config.PLAYER_KILLED
            self.kill()
            self.game.playing = False

class Block(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
        self.image = pygame.Surface((TILESIZE * ENEMY_SIZE, TILESIZE * ENEMY_SIZE))
        self.image.fill(GREEN)

        self.x = x
        self.y = y

        self.x_change = 0
        self.y_change = 0
        self.change_direction_time = random.uniform(1, 3)
        self.last_direction_change = time.time()

        self.set_random_direction()

        self.hp = ENEMY_HP

    def update(self):
       # self.move()

        # Check for collisions with blocks
        self.collide_blocks('x')
        self.collide_blocks('y')

        # Check if it's time to change direction
        if time.time() - self.last_direction_change > self.change_direction_time:
            self.set_random_direction()

    def set_random_direction(self):
        self.facing = random.choice(['left', 'right', 'up', 'down'])
        self.update_speed()
        self.last_direction_change = time.time()  # Reset the timer

    def update_speed(self):
        if self.facing == 'left':
            self.x_change = -ENEMY_SPEED
            self.y_change = 0
        elif self.facing == 'right':
            self.x_change = ENEMY_SPEED
            self.y_change = 0
        elif self.facing == 'up':
            self.y_change = -ENEMY_SPEED
            self.x_change = 0
        elif self.facing == 'down':
            self.y_change = ENEMY_SPEED
            self.x_change = 0

    # def move(self):
    #     # Apply movement based on current speed
    #     self.rect.x += self.x_change
    #     self.rect.y += self.y_change
    #
    #      # Boundary checks
    #     if self.rect.x < 0:
    #         self.rect.x = 0
    #     elif self.rect.x + self.rect.width > WIN_WIDTH:
    #         self.rect.x = WIN_WIDTH - self.rect.width
    #
    #     if self.rect.y < 0:
    #         self.rect.y = 0
    #     elif self.rect.y + self.rect.height > WIN_HEIGHT:
    #         self.rect.y = WIN_HEIGHT - self.rect.height

    def collide_blocks(self, direction):
        collision_occurred = False

        if direction == 'x':
            for block in self.game.blocks:
                if self.rect.colliderect(block.rect):
                    collision_occurred = True
                    if self.x_change > 0:  # Moving right
                        self.rect.right = block.rect.left
                    elif self.x_change < 0:  # Moving left
                        self.rect.left = block.rect.right

        elif direction == 'y':
            for block in self.game.blocks:
                if self.rect.colliderect(block.rect):
                    collision_occurred = True
                    if self.y_change > 0:  # Moving down
                        self.rect.bottom = block.rect.top
                    elif self.y_change < 0:  # Moving up
                        self.rect.top = block.rect.bottom

        # Change direction randomly after a collision
        if collision_occurred:
            self.set_random_direction()

    def take_damage(self, damage):
        self.hp -= damage
        if(self.hp <= 0):
            self.kill()
            self.game.playing = False
            return agent_config.MONSTER_KILLED
        else:
            return agent_config.MONSTER_HIT
           
class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y, angle):
        self.game = game
        self._layer = PROJECTILE_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([10, 10])  # Size of the projectile
        self.image.fill(PINK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Store the angle and calculate the velocity components

        self.angle = angle
        self.dx = PROJECTILE_SPEED * math.cos(math.radians(self.angle))
        self.dy = -PROJECTILE_SPEED * math.sin(math.radians(self.angle))  # Negative for upward movement

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        return self.collide()


    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)

        reward = 0
        for enemy in self.game.enemies:
            if((self.x + self.dx < enemy.x < self.x) or (self.x < enemy.x < self.x + self.dx) or (self.y + self.dy < enemy.y < self.y) or (self.y < enemy.y < self.y + self.dy)):
                reward += enemy.take_damage(DAMAGE_VAL)
                self.kill()

        if hits:
            # Handle what happens when the projectile hits an enemy
            for enemy in hits:
                self.kill()
                reward += enemy.take_damage(DAMAGE_VAL)  # Example action: remove the enemy

        return reward

'''
Shawcode. “Pygame RPG Tutorial #1 - Pygame Tutorial.” 
YouTube, 21 Feb. 2021, youtu.be/crUF36OkGDw?si=g54rCG25-wNusCUJ. 
Accessed 27 Oct. 2024.

Note: resource used to learn how to use pygame, but this is an original file made by us. 
'''

