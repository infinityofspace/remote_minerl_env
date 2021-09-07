import logging
import socket
from typing import Tuple

from remote_minerl_env import proto
from remote_minerl_env.sock.socket import Socket


class RemoteClientEnv:

    def __init__(self, env_name: str, reuse_instance: bool = True, host: str = "localhost", port: int = proto.PORT):
        assert env_name is not None

        self._sock = Socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((host, port))

        self._sock.send(("env", env_name, reuse_instance))

        res, *payload = self._sock.receive()

        if res == proto.OK:
            self.action_space, new_env = payload
            if not new_env:
                logging.info(f"A running instance of the requested environment with id \"{env_name}\" was reused.")
        else:
            raise payload[0]

    def reset(self) -> object:
        self._sock.send(("reset",))

        res, *payload = self._sock.receive()

        if res == proto.OK:
            obs = payload[0]
            return obs
        else:
            raise payload[0]

    def step(self, actions) -> Tuple[object, float, bool, dict]:
        self._sock.send(("step", actions))

        res, *payload = self._sock.receive()

        if res == proto.OK:
            obs, rew, env_done, info = payload
            return obs, rew, env_done, info
        else:
            raise payload[0]
