import gym
from RL_brain import DeepQNetwork
import time

env = gym.make('CartPole-v0')
env = env.unwrapped

RL = DeepQNetwork(n_actions=env.action_space.n,
                  n_features=env.observation_space.shape[0],
                  learning_rate=0.0001,
                  e_greedy=0.9,
                  replace_target_iter=300,
                  memory_size=20000,
                  e_greedy_increment=0.0002,)

flag = False
total_steps = 0
S_start_time = time.time()
for i_episode in range(10000):
    observation = env.reset()
    ep_r = 0
    start_time = time.time()
    step = 0
    while True:
        if i_episode % 10 == 0 or flag: 
            env.render()
            pass
        action = RL.choose_action(observation)
        observation_, reward, done, info = env.step(action)

        position, velocity, angle, velocity_at_tip = observation_
        r1 = (2.4 - abs(position) ) / 2.4 - 0.5
        r2 = (0.209 - abs(angle) ) / 0.209 - 0.5
        reward = r1 * 2 + r2 * 0.5

        RL.store_transition(observation, action, reward, observation_)

        ep_r += reward
        step += 1
        if total_steps > 1000:
            RL.learn()
        if abs(position) > 4.1 or abs(angle) > 1.5 or ep_r < -500 or step > 5000:
            if step > 5000:
                flag = True
            else:
                flag = False
            print('episode: ', i_episode,
                  'ep_r: ', round(ep_r, 2),
                  ' epsilon: ', round(RL.epsilon, 2),
                  ' step: ', step,
                  ' time: ', int(time.time() - start_time))
            print("tot time", int(time.time() - S_start_time))
            break

        observation = observation_
        total_steps += 1

RL.plot_cost()