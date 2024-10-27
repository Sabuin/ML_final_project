import game
import agent_config
import torch #pytorch
import random
import numpy as np #numpy
from model import Linear_QNet, QTrainer
from collections import deque #data structure to store memory
import matplotlib.pyplot as plot

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=agent_config.MAX_MEMORY)
        self.model = Linear_QNet(agent_config.STATE_COUNT, 256, 5)  # input size, hidden size, output size
        self.trainer = QTrainer(self.model, lr=agent_config.LR, gamma=self.gamma)


    def get_state(self, g: game):
        '''

        Facing up/down/left/right
        Monster up/down/left/right
        '''

        state = []

        #player facings
        if(g.player.facing == "up"):
            state.append(1)
        else:
            state.append(0)

        if (g.player.facing == "down"):
            state.append(1)
        else:
            state.append(0)

        if (g.player.facing == "left"):
            state.append(1)
        else:
            state.append(0)

        if (g.player.facing == "right"):
            state.append(1)
        else:
            state.append(0)

        #state relative monster position
        if(g.player.y > g.enemy.y):
            state.append(1)
        else:
            state.append(0)

        if(g.player.y < g.enemy.y):
            state.append(1)
        else:
            state.append(0)

        if(g.player.x > g.enemy.x):
            state.append(1)
        else:
            state.append(0)

        if (g.player.x < g.enemy.x):
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
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0, 0, 0]

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 4)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    g = game.Game()
    g.new()

    score = 0
    while True:

        state_old = agent.get_state(g)
        final_move = agent.get_action(state_old)
        reward, done = g.events(final_move)
        state_new = agent.get_state(g)
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        score += reward

        if done:
            g.new()
            agent.n_games += 1
            agent.train_long_memory()

            print('Game', agent.n_games, 'Score:', score)


            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot.plot(plot_scores)

            plot.show()

            score = 0

if __name__ == "__main__":
    train()

'''
freeCodeCamp.org. “Python + PyTorch + Pygame Reinforcement Learning –
Train an AI to Play Snake.” YouTube, 25 Apr. 2022, youtu.be/L8ypSXwyBds?si=94UOpnWVmBMUwggG.
Accessed 12 Sep. 2024.

AGENT FILE WAS MODIFIED
'''
