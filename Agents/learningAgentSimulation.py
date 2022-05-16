import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import style
import pickle
import time
import cv2

style.use('ggplot')

SIZE = 10
NO_EPISODES = 25000
MOVE_PENALTY = 1
ENEMY_PENALTY = 300
FOOD_REWARD = 25
epsilon = 0.9
EPS_DECAY = 0.9998
SHOW_EVERY = 3000

start_move_table = None

LEARNING_RATE = 0.1
DISCOUNT = 0.95
PLAYER_N = 1
ENEMY_N = 3
FOOD_N = 2

# Color BGR
d = {1: (255, 175, 0),
     2: (0, 255, 0),
     3: (0, 0, 255)}

class Player:
    def __init__(self):
        self.x = np.random.randint(0, SIZE)
        self.y = np.random.randint(0, SIZE)
    
    def __str__(self):
        return f"{self.x}, {self.y}"
    
    def __sub__(self, other):
        return (self.x-other.x, self.y-other.y)
    
    def action(self, choice):
        if choice == 0:
            self.move(x=1, y=0) # Down
        elif choice == 1:
            self.move(x=0, y=1) # Right
        elif choice == 2:
            self.move(x=-1, y=0) # Up
        elif choice == 3:
            self.move(x=0, y=-1) # Left
    
    def move(self, x=False, y=False):
        if (not x) and (not y):
            if(np.random.randint(0, 2)):
                self.x += np.random.randint(-1, 2)
            else:
                self.y += np.random.randint(-1, 2)
        else:
            if not x:
                self.x += np.random.randint(-1, 2)
            else:
                self.x += 1
            if not y:
                self.y += np.random.randint(-1, 2)
            else:
                self.y += 1
        
        if self.x < 0:
            self.x = 0
        elif self.x > SIZE-1:
            self.x = SIZE-1
        if self.y < 0:
            self.y = 0
        elif self.y > SIZE-1:
            self.y = SIZE-1

class Food:
    def __init__(self, x=None, y=None):
        if(x == None):
            self.x = np.random.randint(0, SIZE)
            self.y = np.random.randint(0, SIZE)
        else:
            self.x = x
            self.y = y
    
    def __str__(self):
        return f"{self.x}, {self.y}"
    
    def __sub__(self, other):
        return (self.x-other.x, self.y-other.y)
    
    def action(self, choice):
        if choice == 0:
            self.move(x=1, y=0) # Down
        elif choice == 1:
            self.move(x=0, y=1) # Right
        elif choice == 2:
            self.move(x=-1, y=0) # Up
        elif choice == 3:
            self.move(x=0, y=-1) # Left
    
    def move(self, x=False, y=False):
        if (not x) and (not y):
            if(np.random.randint(0, 2)):
                self.x += np.random.randint(-1, 2)
            else:
                self.y += np.random.randint(-1, 2)
        else:
            if not x:
                self.x += np.random.randint(-1, 2)
            else:
                self.x += 1
            if not y:
                self.y += np.random.randint(-1, 2)
            else:
                self.y += 1
        
        if self.x < 0:
            self.x = 0
        elif self.x > SIZE-1:
            self.x = SIZE-1
        if self.y < 0:
            self.y = 0
        elif self.y > SIZE-1:
            self.y = SIZE-1

if start_move_table is None:
    move_table = {}
    for x1 in range(-SIZE+1, SIZE):
        for y1 in range(-SIZE+1, SIZE):
            for x2 in range(-SIZE+1, SIZE):
                for y2 in range(-SIZE+1, SIZE):
                    move_table[((x1, y1), (x2, y2))] = [np.random.uniform(-5, 0) for i in range(4)]
else:
    with open(start_move_table, "rb") as f:
        move_table = pickle.load(f)

episode_rewards = []
for episode in range(NO_EPISODES):
    player = Player()
    enemy = Player()
    food = Player()

    if episode % SHOW_EVERY == 0:
        print(f"on # {episode}, epsilon: {epsilon}")
        print(f"{SHOW_EVERY} ep mean {np.mean(episode_rewards[-SHOW_EVERY:])}")
        show = True
    else:
        show = False
    episode_reward = 0
    for i in range(200):
        obs = (player - food, player-enemy)
        if np.random.random() > epsilon:
            action = np.argmax(move_table[obs])
        else:
            action = np.random.randint(0, 4)
        
        player.action(action)
        enemy.move()
        food.move()

        if player.x == enemy.y and player.y == enemy.y:
            reward = -ENEMY_PENALTY
        elif player.x == food.x and player.y == food.y:
            reward = FOOD_REWARD
        else:
            reward = -MOVE_PENALTY
        
        new_obs = (player-food, player-enemy)
        max_future_q = np.max(move_table[new_obs])
        current_q = move_table[obs][action]

        if reward == FOOD_REWARD:
            new_q = FOOD_REWARD
        elif reward == -ENEMY_PENALTY:
            new_q = -ENEMY_PENALTY
        else:
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

        move_table[obs][action] = new_q

        if show:
            env = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
            env[food.y][food.x] = d[FOOD_N]
            env[player.y][player.x] = d[PLAYER_N]
            env[enemy.y][enemy.x] = d[ENEMY_N]

            img = Image.fromarray(env, "RGB")
            img = img.resize((300, 300), resample=Image.BOX)
            cv2.imshow("", np.array(img))
            if reward == FOOD_REWARD or reward == -ENEMY_PENALTY:
                if cv2.waitKey(500) & 0xFF == ord("q"):
                    break
            else:
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        
        episode_reward += reward
        if reward == FOOD_REWARD or reward == -ENEMY_PENALTY:
            break
    episode_rewards.append(episode_reward)
    epsilon *= EPS_DECAY

moving_avg = np.convolve(episode_rewards, np.ones((SHOW_EVERY,)) / SHOW_EVERY, mode="valid")
plt.plot([i for i in range(len(moving_avg))], moving_avg)
plt.ylabel(f"reward {SHOW_EVERY}ma")
plt.xlabel("episode #")
plt.show()

with open(f"qtable-{int(time.time())}.pickle", "wb") as f:
    pickle.dump(move_table, f)