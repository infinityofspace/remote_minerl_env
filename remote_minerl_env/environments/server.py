import logging
import socket

import gym
import minerl

from remote_minerl_env import proto
from remote_minerl_env.sock.socket import Socket


class RemoteServerEnv:

    def __init__(self, env_name: str = None, host: str = "localhost", port: int = proto.PORT):
        self._env_name = env_name
        self.__host = host
        self.__port = port

        self._env = None
        self._obs = None

    def _handle_requests(self, sock: Socket):
        while True:
            method, *payload = sock.receive()

            if method == "env":
                if len(payload) == 2:
                    env_name, reuse_instance = payload

                    if self._env and (not reuse_instance or self._env.spec.id != env_name):
                        self._env.close()
                        self._env = None

                    if self._env and self._env.spec.id == env_name:
                        sock.send((proto.OK, self._env.action_space, True))
                    else:
                        try:
                            self._env = gym.make(env_name)
                            sock.send((proto.OK, self._env.action_space, False))
                        except Exception as e:
                            sock.send((proto.ERROR, e))
                            return
                else:
                    sock.send((proto.ERROR, Exception("bad payload")))
            elif self._env and method == "reset":
                try:
                    self._obs = self._env.reset()
                    sock.send((proto.OK, self._obs))
                except Exception as e:
                    sock.send((proto.ERROR, e))
                    return
            elif self._env and method == "step":
                if len(payload) == 1:
                    actions = payload[0]
                    try:
                        obs, rew, done, info = self._env.step(actions)
                        sock.send((proto.OK, obs, rew, done, info))
                    except Exception as e:
                        sock.send((proto.ERROR, e))
                        return
                else:
                    sock.send((proto.ERROR, Exception("bad payload")))
            elif not self._env:
                sock.send((proto.ERROR, Exception("environment not initialised")))
            else:
                sock.send((proto.ERROR, Exception("unsupported method")))

    def start(self):
        if self._env_name:
            self._env = gym.make(self._env_name)

        sock = Socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.__host, self.__port))
        sock.listen(1)

        logging.info("Server started successfully on {}:{}".format(self.__host, self.__port))

        while True:
            s = None
            try:
                s, addr = sock.accept()

                logging.info("connection from {}:{}".format(*addr))

                try:
                    self._handle_requests(s)
                except Exception as e:
                    logging.info(e)
            finally:
                # close the server socket
                if s:
                    s.close()
