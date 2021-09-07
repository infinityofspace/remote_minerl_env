import argparse
import textwrap
from pathlib import Path

from pyngrok import ngrok, conf

from remote_minerl_env import proto
from remote_minerl_env.environments.server import RemoteServerEnv


def main():
    parser = argparse.ArgumentParser(
        description="Remote environment for minerl competition environments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
                                        License:
                                        MIT - Copyright (c) 2021 Marvin Heptner
                                        """),
        add_help=False
    )

    parser.add_argument("-e", "--env-name", help="ID of the minerl environment.", default=None)
    parser.add_argument("-h", "--host", help="Host address to bind to.", default="localhost")
    parser.add_argument("-p", "--port", help="Port to bind to.", default=proto.PORT, type=int)
    parser.add_argument("--ngrok", nargs=2, help="Use ngrok reverse proxy to expose the environment publicly",
                        metavar=("NGROK_CONFIG_PATH", "TUNNEL_NAME"))
    parser.add_argument("--help", action="help", help="Show the help of the program.")

    args = parser.parse_args()

    if args.ngrok:
        ngrok_config_path, tunnel_name = args.ngrok
        if not Path(ngrok_config_path).exists():
            raise FileNotFoundError(f"{ngrok_config_path} does not exists")
        pyngrok_config = conf.PyngrokConfig(config_path=ngrok_config_path)
        ngrok_connection = ngrok.connect(pyngrok_config=pyngrok_config, name=tunnel_name)
        print(f"Remote environment is publicly available at {ngrok_connection.public_url}")

    env = RemoteServerEnv(env_name=args.env_name, host=args.host, port=args.port)
    env.start()


if __name__ == "__main__":
    main()
