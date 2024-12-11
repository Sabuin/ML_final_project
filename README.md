# Beating the Game: The Power of Deep Reinforcement Learning

## Introduction
Through machine learning, specifically deep reinforcement learning, we have created an agent that learns how to beat all of the levels of a game we have created through trial and error. By the final iterations, the agent is capable of learning its purpose, that is, to win the game by defeating all the enemies present in the game by adapting to unpredictable environments through experience.

## Problem Definition and Algorithm 

### Task Definition
The game is challenging, with increasing complexity in every level. The inputs to the model are the relative location of enemy projectiles, the relative position of the monster, the absolute positions of the monster and the player, the direction of “facing” of the player entity, nearby walls, the ‘x’ and ‘y’ positional difference of the player and the enemy, and the absolute distance between the two. The outputs are the actions the agent can take: moving in each of the cardinal directions or firing a projectile. 

### Algorithm Definition

Our deep Q-Learning algorithm uses a feedforward network. Currently, we have 23 inputs (which represent the state of the environment), 6 hidden layers of 128 nodes, and 5 outputs. 

We have two classes in our model file. The first class, Linear_QNet, initializes six linear layers and sets up the ReLU activation function for the hidden layers. This class makes the network. 

QTrainer is the class that trains the neural network. It first initializes important hyperparameters like the learning rate and gamma, variables representing the loss function (MSE), and the optimizer. In our case, we are using the Adam optimizer, which is a “stochastic gradient descent method that is based on adaptive estimation of first-order and second-order moments” (Keras) The optimizer automatically adjusts the learning rate depending on performance. To continue, the Qtrainer class defines a train step function that takes as inputs the state, action, reward, the next step, and if the iteration of the game is completed. The final task of the Qtrainer class is to calculate the loss function and execute the next step. 

## Experimental Evaluation 
We have used a reinforcement learning approach: we are rewarding for damaging and destroying the enemies while penalizing taken damage, self-destruction, and procrastination. 

### Methodology
Our project does not depend on an already existing dataset because the environment does not have a definitive right action. Thus, the agent has to learn through experiencing the game itself, and then utilizing the feedback from each game run to change its actions in subsequent iterations. We are using a reinforcement learning algorithm because we are using unlabeled data. The “dataset” consists of the game states that the environment produces as a result of the deep learning model’s actions.

The agent receives a positive or negative reward (a penalty) based on their performance on an instance of the game. If the agent hits the monster, then it gets a reward of 1, and if it kills it, then it gets a reward of 2. If the agent fails to defeat the monster within a time frame, it receives a penalty of 3. This system of reward or penalty encourages the agent to perform certain actions in the next instance of the game based on the results of the current instance, as it looks to maximize the reward at each iteration. Moreover, as a secondary result of the agent’s performance, we looked to optimize the time taken to finish the game.

### Results and Discussion
The selection of hyperparameters are of great importance to every machine-learning model, but for our model we realized early on that these were crucial for success. We came to this discovery after countless experiments with combinations of hyperparameters. For example, by increasing the maximum batch size from 1000 to 1200 we would get drastically different results. Thus, for most of the duration of the project, we had to test many combinations of hyperparameters. Below is a table showing some of the combinations that we have used when we were running the model on the first level only.

![graphs with different hyperparameter combinations](https://github.com/Sabuin/ML_final_project/blob/d621b31b596a8582cc722d86fed6d7556e2468f3/GRAPHS/Graphs_2.png "Graph")

Taking a quick glance at the graphs, they might seem to indicate that the model appears to be underperforming. Thus, we went through all of our program files to see if any bugs would explain our agent’s behaviour, but could not find any. Therefore, for subsequent runs, we decided to record the game states to see if we could identify what could be causing those results. Particularly, we paid close attention to our agent’s actions during the earlier iterations when randomness is high and the actions taken during the final iterations*. This choice was particularly useful because it showed us that in fact, our model was going in the right direction. We could see that in the last iterations, the agent knew exactly what it needed to do. Instead of randomly moving around the play area, it would directly follow the monster. This was particularly noticeable in the last level, where the monster shoots at the agent while trying to get as far away from it as possible. In the earlier iterations, it was elementary for the monster to escape the player, while in the last ones, we could see the agent actively following it. 

We have concluded that the reason for the results shown in the graph can be mostly blamed on the low number of games that we have. The exploration time stops at about the 120th - 130th iteration, but at this point, the agent could only properly explore the first three levels and only made it to the last one a couple of times. Hence, the agent did not have enough time to experiment with the behaviour of the last monster during the assigned exploration time, and had to do it during exploitation time instead. This explains the high variability in the graph. In the clips* showing the last iterations, we can see that it takes very little time for the agent to beat the first three levels, but a longer time is needed for the last enemy. However,  it is still able to beat it eventually. This illustrates that even though the agent had experienced the last level for only a few attempts, in the end, it is able to adapt and quickly understands that it has to follow it. This reveals that our model is capable of creating an agent that can adjust to similar environments that it has not encountered, which is the goal of deep reinforcement learning. 

Moreover, we knew that by the final iterations, the agent’s actions were no longer random, so we were confused as to why the graphs showed a struggling agent where it was supposed to be performing well. However, at the time, we did not consider the randomness present in the enemies’ behaviour, specifically the third enemy. The third enemy randomly moves around the screen, shooting many projectiles at once. This is a fundamental thing to consider because the little exploration time the agent has is not enough to make it “understand” that the monster’s behaviour is not predetermined. When analyzing the clips of the third level, for some iterations the agent would perform the same actions (for example, going to a particular location and shooting from there) which could defeat the enemy. Consequently, for subsequent iterations, it would try to repeat those actions but would be defeated because of this randomness. 

All things considered, we cannot say that the graphs were not beneficial. From them, we could also determine what combinations of hyperparameters resulted in better performance. For example, we can see that for certain values, the agent was able to beat all levels more times than with others, showing us which hyperparameters to keep for future work. 

 *The videos can be found under the *VIDEOS* folder. 
 
## Related Work
Some video game designers have implemented deep learning models to find the best way to beat other video games or to use them as a tool to enhance an already-made game. Our approach is different because the model is being implemented on a game that we have made, so we have more understanding of how the program works and what features should be considered. 

The biggest guidance for our project was a deep Q-learning implementation of Snake by Patrick Loeber, though the environment that we implemented is different in genre and representation. Moreover, our game forces a more hostile environment on the agent because we have levels with increasing complexity, which the agent must adapt to. Furthermore, Snake is simpler in design because the player can take fewer actions while in our game, 5 actions must be considered. Additionally, our method shows an agent that can adapt to our various environments due to the fact that it has to fight enemies with unique behaviours. 

## Conclusion 
After robust testing, experimentation, and analysis, we conclude that our model has been successful in creating an agent that is able to accomplish the goal of the game by learning from its actions and acting accordingly. Due to hardware limitations and time constraints, we unfortunately could not increase the number of iterations, which consequently limited the model’s performance by shortening the exploration phase for the agent, which is crucial for performance in subsequent runs. We believe that if more exploration time could be allocated, then we would have gotten the expected graphs containing the optimal results (a purple line at the top, and a pink line at the bottom of the graph). 

The topic of reinforcement deep learning brings great discussions about model optimization. With future work being considered as an option, there are many possible choices to explore in order to improve our model, including but not limited to:
* Adjusting the exploration and exploitation time.
* Continue our search for the best combinations of hyperparameters and states. 
* Adjusting the neural network.
* Considering different information about the environment that the agent can receive.

## BIBLIOGRAPHY 
[1] R. Agarwal, "Complete Guide to the Adam Optimization Algorithm | Built In," Builtin.com, 13 Sept. 2023. [Online]. Available: https://builtin.com/machine-learning/adam-optimization. [Accessed: Oct. 27, 2024].

[2] "Bellman Equation," GeeksforGeeks, 23 Sept. 2021. [Online]. Available: https://www.geeksforgeeks.org/bellman-equation/. [Accessed: Oct. 27, 2024].

[3] M. Comi, "How to Teach AI to Play Games: Deep Reinforcement Learning," Medium, Towards Data Science, 15 Nov. 2018. [Online]. Available: https://towardsdatascience.com/how-to-teach-an-ai-to-play-games-deep-reinforcement-
learning-28f9b920440a. [Accessed: Oct. 27, 2024].

[4] "Deep Learning Tutorial," GeeksforGeeks, 10 Apr. 2023. [Online]. Available: https://www.geeksforgeeks.org/deep-learning-tutorial/. [Accessed: Oct. 27, 2024].

[5] "Environments," TensorFlow, 2023. [Online]. Available: https://www.tensorflow.org/agents/tutorials/2_environments_tutorial. [Accessed: Sept. 26, 2024].

[6] freeCodeCamp.org, "Python + PyTorch + Pygame Reinforcement Learning – Train an AI to Play Snake," YouTube, 25 Apr. 2022. [Online]. Available: https://youtu.be/L8ypSXwyBds?si=94UOpnWVmBMUwggG. [Accessed: Oct. 27, 2024].

[7] "Implementing Deep QLearning Using Tensorflow," GeeksforGeeks, 14 June 2019. [Online]. Available: https://www.geeksforgeeks.org/implementing-deep-q-learning-using-tensorflow/. [Accessed: Oct. 27, 2024].

[8] "Introduction to RL and Deep Q Networks | TensorFlow Agents," TensorFlow. [Online]. Available: https://www.tensorflow.org/agents/tutorials/0_intro_rl. [Accessed: Oct. 27, 2024].

[9] "Introduction to Thompson Sampling | Reinforcement Learning," GeeksforGeeks, 22 Aug. 2019. [Online]. Available: https://www.geeksforgeeks.org/introduction-to-thompson-sampling-reinforcement-learning/. [Accessed: Oct. 27, 2024].

[10] "Keras Documentation: Adam," Keras.io. [Online]. Available: https://keras.io/api/optimizers/adam/. [Accessed: Oct. 27, 2024].

[11] "Markov Decision Process - GeeksforGeeks," GeeksforGeeks, 4 Jan. 2018. [Online]. Available: https://www.geeksforgeeks.org/markov-decision-process/. [Accessed: Oct. 27, 2024].

[12] "Meta-Learning in Machine Learning," GeeksforGeeks, 18 May 2019. [Online]. Available: https://www.geeksforgeeks.org/meta-learning-in-machine-learning/. [Accessed: Oct. 27, 2024].

[13] "ML | Reinforcement Learning Algorithm : Python Implementation Using Q-Learning," GeeksforGeeks, 30 May 2019. [Online]. Available: https://www.geeksforgeeks.org/ml-reinforcement-learning-algorithm-python-implementation-using-q-learning/. [Accessed: Oct. 27, 2024].

[14] "Q-Learning in Python - GeeksforGeeks," GeeksforGeeks, 6 Feb. 2019. [Online]. Available: https://www.geeksforgeeks.org/q-learning-in-python/. [Accessed: Oct. 27, 2024].

[15] Shawcode, "Pygame RPG Tutorial #1 - Pygame Tutorial," YouTube, 21 Feb. 2021. [Online]. Available: https://youtu.be/crUF36OkGDw?si=g54rCG25-wNusCUJ. [Accessed: Oct. 27, 2024].

[16] "Torch.nn — PyTorch Master Documentation," Pytorch.org. [Online]. Available: https://pytorch.org/docs/stable/nn.html. [Accessed: Oct. 27, 2024].

[17] "Understanding Reinforcement Learning In-Depth," GeeksforGeeks, 19 Feb. 2022. [Online]. Available: https://www.geeksforgeeks.org/understanding-reinforcement-learning-in-depth/. [Accessed: Oct. 27, 2024].













