from distutils.command.bdist import bdist
from operator import truediv
from typing import final

from fontTools.varLib.instancer import axisValuesFromAxisLimits

import config
import game
import agent_config
import torch #pytorch
import random
import numpy as np #numpy
import math

from agent_config import RAND_MULT
from config import WIN_HEIGHT, WIN_WIDTH
from model import Linear_QNet, QTrainer
from collections import deque #data structure to store memory
import matplotlib.pyplot as plt

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=agent_config.MAX_MEMORY)
        self.model = Linear_QNet(agent_config.STATE_COUNT, 128, 5)  # input size, hidden size, output size
        self.trainer = QTrainer(self.model, lr=agent_config.LR, gamma=self.gamma)


    def get_state(self, g: game):
        '''

        Facing up/down/left/right
        willHit True/False
        Monster up/down/left/right
        nearbyWalls up/down/left/right
        playerPos val
        monsterPos val
        dydx val x2
        distance2Sasha val
        '''

        #configs
        facing = True #4
        willHit = False #1
        relativeMonsterPos = True #4
        nearbyWalls = True #4
        playerPos = True #2
        monsterPos = True #2
        dydx = True #2
        distance2Monster = True #1
        bulletNearby = True #4

        state = []

        # player facings
        # if(facing):
        #     if(g.player.facing == "up"):
        #         state.append(1)
        #     else:
        #         state.append(0)
        #
        #     if (g.player.facing == "down"):
        #         state.append(1)
        #     else:
        #         state.append(0)
        #
        #     if (g.player.facing == "left"):
        #         state.append(1)
        #     else:
        #         state.append(0)
        #
        #     if (g.player.facing == "right"):
        #         state.append(1)
        #     else:
        #         state.append(0)

        #delete later ----------
        if (facing):
            directions = ["up", "down", "left", "right"]
            for direction in directions:
                if g.player.facing == direction:
                    state.append(1)
                else:
                    state.append(0)

        if(willHit):
            inLineX = (g.enemy.rect.x <= g.player.rect.x <= g.enemy.rect.x + config.ENEMY_SIZE)
            inLineY = (g.enemy.rect.y <= g.player.rect.y <= g.enemy.rect.y + config.ENEMY_SIZE)
            if((g.player.facing == "up" and inLineX and g.enemy.y < g.player.y) or
               (g.player.facing == "down" and inLineX and g.enemy.y > g.player.y) or
               (g.player.facing == "right" and inLineY and g.enemy.x > g.player.x) or
               (g.player.facing == "left" and inLineY and g.enemy.x < g.player.x)):
                state.append(1)
            else:
                state.append(0)


        #state relative monster position
        if(relativeMonsterPos):
            if(g.player.rect.y > g.enemy.rect.y):
                state.append(1)
            else:
                state.append(0)

            if(g.player.rect.y < g.enemy.rect.y):
                state.append(1)
            else:
                state.append(0)

            if(g.player.rect.x > g.enemy.rect.x):
                state.append(1)
            else:
                state.append(0)

            if (g.player.rect.x < g.enemy.rect.x):
                state.append(1)
            else:
                state.append(0)

        margin = 10
        if(nearbyWalls):
            if(g.player.rect.y < margin):
                state.append(1)
            else:
                state.append(0)

            if(g.player.rect.y > WIN_HEIGHT - margin):
                state.append(1)
            else:
                state.append(0)

            if(g.player.rect.x < margin):
                state.append(1)
            else:
                state.append(0)

            if(g.player.rect.x > WIN_WIDTH - margin):
                state.append(1)
            else:
                state.append(0)

        if(playerPos):
            state.append(g.player.rect.x)
            state.append(g.player.rect.y)

        if(monsterPos):
            state.append(g.enemy.rect.x)
            state.append(g.enemy.rect.y)

        if(dydx):
            state.append((g.player.rect.x - g.enemy.rect.x))
            state.append((g.player.rect.y - g.enemy.rect.y))

        if(distance2Monster):

            # val = g.player.rect.x ** 2 + g.player.rect.y ** 2
            # val = val ** .5
            # val = val/((WIN_WIDTH ** 2 + WIN_HEIGHT ** 2) ** .5)

            state.append(math.dist((g.player.rect.x, g.player.rect.y), (g.enemy.rect.x,g.enemy.rect.y)))

        if(bulletNearby):
            bRight = False
            bLeft = False
            bDown = False
            bUp = False

            for bullet in g.enemyProjectiles:
                xDif = bullet.rect.x - g.player.rect.x
                yDif = bullet.rect.y - g.player.rect.y
                if(xDif < agent_config.DETECT_RADIUS):
                    bRight = True
                if(-agent_config.DETECT_RADIUS < xDif):
                    bLeft = True
                if(yDif < agent_config.DETECT_RADIUS):
                    bDown = True
                if(-agent_config.DETECT_RADIUS < yDif):
                    bUp = True

            if(bRight):
                state.append(1)
            else:
                state.append(0)

            if(bLeft):
                state.append(1)
            else:
                state.append(0)

            if(bDown):
                state.append(1)
            else:
                state.append(0)

            if(bUp):
                state.append(1)
            else:
                state.append(0)


        return np.array(state, dtype=int)


#FROM SNAKE AI VIDEO
    def remember(self, state, action, reward, next_state, done):
            self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > agent_config.BATCH_SIZE:
            mini_sample = random.sample(self.memory, agent_config.BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon= 80 * RAND_MULT - self.n_games #80 - self.n_games
        final_move = [0, 0, 0, 0, 0]

        if random.randint(0, 100) < 1:
            move = random.randint(0, 4)
            final_move[move] = 1
        elif random.randint(0, 100*RAND_MULT) < self.epsilon: #change b=100 to 200
            move = random.randint(0, 4)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

def plotGraph(yAxis1, yAxis2):
    xAxis = range(len(yAxis1))
    fig, ax1 = plt.subplots()
    ax1.set_xlabel("Game #")
    ax1.set_ylabel("Reward (Purple)")
    ax1.plot(xAxis, yAxis1, color="purple")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Duration (Frames) (Pink)")
    ax2.plot(xAxis, yAxis2, color="pink")

    fig.tight_layout()
    plt.show()

def plotTimeVReward(time, reward):
    plt.scatter(time, reward, color="blue")
    plt.show()

def train():
    plot_scores = []
    plot_mean_scores = []
    plot_times = []
    total_score = 0
    record = 0
    agent = Agent()
    g = game.Game()
    g.new()

    score = 0
    duration = 0
    i = 0

    while(i < 200): #DON'T FORGET TO CHANGE

        state_old = agent.get_state(g)
        final_move = agent.get_action(state_old)
        reward, done = g.events(final_move)
        state_new = agent.get_state(g)
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        score += reward
        duration += 1

        if done:
            i+=1
            g.new()
            agent.n_games += 1
            agent.train_long_memory()

           # print('Game', agent.n_games, 'Score:', score)
            print(str(score))

            plot_scores.append(score)
            plot_times.append(duration)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plotGraph(plot_mean_scores, plot_times)
            #plotTimeVReward(plot_times, plot_scores)

            score = 0
            duration = 0


if __name__ == "__main__":
    train()

'''
freeCodeCamp.org. “Python + PyTorch + Pygame Reinforcement Learning –
Train an AI to Play Snake.” YouTube, 25 Apr. 2022, youtu.be/L8ypSXwyBds?si=94UOpnWVmBMUwggG.
Accessed 12 Sep. 2024.

AGENT FILE WAS MODIFIED
'''