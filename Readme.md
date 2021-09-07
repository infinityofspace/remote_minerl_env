# remote-minerl-env

Remote environment for minerl competition environments

---

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/remote_minerl_env?style=for-the-badge)
[![GitHub](https://img.shields.io/github/license/infinityofspace/remote_minerl_env?style=for-the-badge)](https://github.com/infinityofspace/remote_minerl_env/blob/master/License)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/infinityofspace/remote_minerl_env/pypi%20release?style=for-the-badge)

---

### Table of Contents

1. [About](#about)
2. [Installation](#installation)
    1. [With pip (recommend)](#with-pip-recommend)
    2. [From source](#from-source)
3. [Usage](#usage)
4. [Examples](#examples)
5. [Third party notices](#third-party-notices)
6. [License](#license)

---

### About

This package allows to run the Minecraft Malmo instance for the [minerl](https://github.com/minerllabs/minerl) contest
on any host and allows to access it from another host. The Minecraft instance on the selected host system is not closed
to ensure the fastest possible availability. This allows to test the agent code much faster and in case of an error in
the agent code you don't have to restart the Minecraft instance again. The host on which the Minecraft instance runs can
also be identical to that of the agent.

In addition, the host on which the Malmo instance is running can be on a completely different network and can be
accessed without port forwarding. For this purpose a reverse proxy is used, which forwards the requests to this host via
an external and publicly accessible server.

### Installation

*remote-minerl-env* requires Python 3.6+ to be installed.

#### With pip (recommend)

Use the following command to install *remote-minerl-env* with pip:

```commandline
pip install remote-minerl-env
```

You can also very easily update to a newer version:

```commandline
pip install remote-minerl-env -U
```

#### From source

```commandline
git clone https://github.com/infinityofspace/remote_minerl_env.git
cd remote_minerl_env
pip install .
```

### Usage

After the installation, you can start the remote environment with the following command on the desired host on which you
want to run the Minecraft Malmo instance.

```commandline
remote-minerl-env
```

All available arguments:

```commandline
usage: remote-minerl-env [-e ENV_NAME] [-h HOST] [-p PORT] [--help]

optional arguments:
  -e ENV_NAME, --env-name ENV_NAME
                        ID of the minerl environment.
  -h HOST, --host HOST  Host address to bind to.
  -p PORT, --port PORT  Port to bind to.
  --ngrok NGROK_CONFIG_PATH TUNNEL_NAME
                        Use ngrok reverse proxy to expose the environment publicly
  --help                Show the help of the program.
```

After you have started the remote instance you only need to make minimal adjustments to your existing agent code and
then you are done.

You have to use

```python
from remote_minerl_env.environments.client import RemoteClientEnv

env = RemoteClientEnv("<name of the env>")
```

instead of

```python
env = gym.make("<name of the env>")
```

That was all. The RemoteEnv also supports the functions `step`, `reset` and provides access to the
attribute `action_space` of the original gym environment as class attribute.

Without any additional arguments the instance is only accessible from localhost on port `42424`
To expose the Minecraft instance publicly you can use the `--ngrok` parameter. This uses [ngrok](https://ngrok.com/) to
make your local instance accessible from outside your local network:

```commandline
remote-minerl-env --ngrok /path/to/your/ngrok/config.yml <name-of-the-tunnel-to-use>
```

The tunnel must be a tcp tunnel and the local mapped port should match the port from the instance, which can be
customized with the `--port` parameter (default port is `42424`).

### Third party notices

All modules used by this project are listed below:

| Name                                             | License                                                                    |
|:------------------------------------------------:|:--------------------------------------------------------------------------:|
| [minerl](https://github.com/minerllabs/minerl)   | [LICENSE](https://raw.githubusercontent.com/minerllabs/minerl/dev/LICENSE) |
| [setuptools](https://github.com/pypa/setuptools) | [MIT](https://raw.githubusercontent.com/pypa/setuptools/main/LICENSE)      |
| [pyngrok](https://github.com/alexdlaird/pyngrok) | [MIT](https://raw.githubusercontent.com/alexdlaird/pyngrok/main/LICENSE)   |

Furthermore, this readme file contains embeddings of [Shields.io](https://github.com/badges/shields) badges.

### License

[MIT](License) - Copyright (c) 2021 Marvin Heptner
