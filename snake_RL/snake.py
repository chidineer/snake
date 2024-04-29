import gym
from snake_env import register_env
import snake_env
# import pybullet_envs
import pybullet as p
import numpy as np
import math
from collections import defaultdict
import pickle
import torch
import random

env = gym.make('Snake-v0')

env.reset()
for i in range(100):  # Run game steps
    env.render()
    action = env.action_space.sample()
    env.step(action)
env.close()
