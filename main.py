import random
import os
import sys

from training import online
from training.offline import offline_wrapper

sys.path.append(os.getcwd() + "/environment")
import time

import gym
import argparse
import torch
from torch.optim import Adam
import torch.nn as nn
import numpy as np
from pynput import keyboard
from environment.gym_tictactoe.gym_tictactoe.env import TicTacToeEnv
from environment.GLOBALS import *
from environment.SnakeWrapper import SnakeWrapper
from environment.TTTWrapper import TTTWrapper
from networks.Network import Net
from scipy.stats import gamma
from datetime import datetime as time
import time as tm
from environment.MountainCarWrapper import MountainCarWrapper

device = torch.device('cpu')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('--num_plays', default=5, type=int, help="number of play runs to collect")
    parser.add_argument('--mode', default=DEFAULT_MODE, type=str, help="Which game to do")
    parser.add_argument('--fps', default=10, type=int, help="max fps at which snake game should run")
    parser.add_argument('--frame_limit', default=200, type=int, help="number of frames before episode cuts off")
    parser.add_argument('--feedback_mode', default="online", type=str, help="online/offline : how feedback will be given?")
    args = parser.parse_args()

    net = Net(args.mode)
    for i in range(args.num_plays):
        if args.feedback_mode == "online":
            data = online.collect_live_data(net, env_name=args.mode, frame_limit=args.frame_limit, snake_max_fps=args.fps)
            print("Data for run " + str(i + 1) + ":\n" + str(data))
        elif args.feedback_mode == "offline":
            offline_wrapper(net, env_name=args.mode, frame_limit=args.frame_limit, snake_max_fps=args.fps)
            print("Didn't collect data, but offline run " + str(i + 1) + " complete.")
        
