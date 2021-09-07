from remote_minerl_env.environments.client import RemoteClientEnv


def main():
    env = RemoteClientEnv("MineRLObtainDiamond-v0")

    obs = env.reset()
    done = False

    while not done:
        obs, rew, done, _ = env.step(env.action_space.sample())


if __name__ == "__main__":
    main()
