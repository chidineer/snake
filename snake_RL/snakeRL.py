
import gym
import snake_env
# import pybullet_envs
import pybullet as p
import numpy as np
import math
from collections import defaultdict
import pickle
import torch
import random
import matplotlib.pyplot as plt
from snake_imports import DQN_Solver
import time

TRAIN = False

# Hyper parameters that will be used in the DQN algorithm

EPISODES = 10000                 # number of episodes to run the training for
LEARNING_RATE = 0.00025         # the learning rate for optimising the neural network weights
MEM_SIZE = 50000                # maximum size of the replay memory - will start overwritting values once this is exceed
REPLAY_START_SIZE = 10000       # The amount of samples to fill the replay memory with before we start learning
BATCH_SIZE = 32                 # Number of random samples from the replay memory we use for training each iteration
GAMMA = 0.99                    # Discount factor
EPS_START = 0.9                 # Initial epsilon value for epsilon greedy action sampling
EPS_END = 0.0001                # Final epsilon value
EPS_DECAY = 4 * MEM_SIZE        # Amount of samples we decay epsilon over
MEM_RETAIN = 0.1                # Percentage of initial samples in replay memory to keep - for catastrophic forgetting
NETWORK_UPDATE_ITERS = 5000     # Number of samples 'C' for slowly updating the target network \hat{Q}'s weights with the policy network Q's weights

FC1_DIMS = 128                   # Number of neurons in our MLP's first hidden layer
FC2_DIMS = 128                   # Number of neurons in our MLP's second hidden layer

# metrics for displaying training status
best_reward = 0
average_reward = 0
episode_history = []
episode_reward_history = []
np.bool = np.bool_

if TRAIN:
    env = gym.make('Snake-v0')

    state, info = env.reset()

    ## DQN START ##
    print("DQN")
    env.action_space.seed(0)
    random.seed(0)
    np.random.seed(0)
    torch.manual_seed(0)
    episode_batch_score = 0
    episode_reward = 0
    agent = DQN_Solver(env)  # create DQN agent
    plt.clf()

    for i in range(EPISODES):
        state, info = env.reset()  # this needs to be called once at the start before sending any actions
        while True:
            # sampling loop - sample random actions and add them to the replay buffer
            action = agent.choose_action(state)
            state_, reward, done, _, info = env.step(action)
            reward += -abs(state_[1])
            # if done == True:
            #   reward = -50

            ####### add sampled experience to replay buffer ##########
            agent.memory.add(state, action, reward, state_, done)
            ##########################################################

            # only start learning once replay memory reaches REPLAY_START_SIZE
            if agent.memory.mem_count > REPLAY_START_SIZE:
                agent.learn()

            state = state_
            episode_batch_score += reward
            episode_reward += reward

            if done:
                break

        episode_history.append(i)
        episode_reward_history.append(episode_reward)
        episode_reward = 0.0

        # save our model every batches of 100 episodes so we can load later. (note: you can interrupt the training any time and load the latest saved model when testing)
        if i % 100 == 0 and agent.memory.mem_count > REPLAY_START_SIZE:
            torch.save(agent.policy_network.state_dict(), "C:/Users/alber/OneDrive - UTS/5th Year/1/AIR/asst3/rl_car_driving/model/policy_network.pkl")
            
            print("average total reward per episode batch since episode ", i, ": ", episode_batch_score/ float(100))
            episode_batch_score = 0
        elif agent.memory.mem_count < REPLAY_START_SIZE:
            print("waiting for buffer to fill...")
            episode_batch_score = 0

    plt.plot(episode_history, episode_reward_history)
    plt.show()
    env.close()


 
############################################################################################
# Test trained policy
env = gym.make('Snake-v0')
agent = DQN_Solver(env)
agent.policy_network.load_state_dict(torch.load("C:/Users/alber/OneDrive - UTS/5th Year/1/AIR/asst3/rl_car_driving/model/policy_network_10000_200.pkl"))
state, info = env.reset()
agent.policy_network.eval()

while True:
    with torch.no_grad():
        q_values = agent.policy_network(torch.tensor([state], dtype=torch.float32))
    action = torch.argmax(q_values).item() # select action with highest predicted q-value
    state, reward, done, _, info = env.step(action)
    env.render()
    time.sleep(1/30)
    if done:
        break

env.close()
