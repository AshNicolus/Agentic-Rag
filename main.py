"""CLI entrypoint for Adaptive RAG.

This module simply imports and runs the `main` function from `src.cli.main` so
the project can be launched with `python main.py`.
"""

from src.cli.main import main


if __name__ == "__main__":
    main()
    