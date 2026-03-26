from __future__ import annotations

import os
from dataclasses import dataclass
from flask import Flask, render_template


@dataclass(frozen=True)
class AppConfig:
    host: str = '0.0.0.0'
    default_port: int = 5000
    debug: bool = False

    def resolve_port(self) -> int:
        return int(os.environ.get('PORT', self.default_port))


class SnakeCvApp:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.app = Flask(__name__)
        self._register_routes()

    def _register_routes(self) -> None:
        @self.app.route('/')
        def index():
            return render_template('index.html')

    def run(self) -> None:
        port = self.config.resolve_port()
        self._print_banner(port)
        self.app.run(host=self.config.host, port=port, debug=self.config.debug)

    @staticmethod
    def _print_banner(port: int) -> None:
        print(f"""
╔══════════════════════════════════════╗
║        🐍  SNAKE CV  🐍              ║
╠══════════════════════════════════════╣
║  Apri il browser su:                 ║
║  http://localhost:{port}               ║
║                                      ║
║  Da mobile sulla stessa rete:        ║
║  http://<tuo-ip>:{port}                ║
║                                      ║
║  Ctrl+C per fermare il server        ║
╚══════════════════════════════════════╝
        """)


if __name__ == '__main__':
    SnakeCvApp(AppConfig()).run()