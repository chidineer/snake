from gym.envs.registration import register


register(
    id='Snake-v0',
    entry_point='snake_env.snake_environment:SnakeEnv',
)