import os
import sys

from pathlib import Path


APP_NAME = "PyPlanner"

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


def resource_path(relative_path):
    return (
        PROJECT_ROOT
        / relative_path
    )


def user_data_directory():
    if sys.platform == "darwin":
        base_directory = (
            Path.home()
            / "Library"
            / "Application Support"
        )

    elif os.name == "nt":
        base_directory = Path(
            os.environ.get(
                "LOCALAPPDATA",
                Path.home()
                / "AppData"
                / "Local"
            )
        )

    else:
        base_directory = Path(
            os.environ.get(
                "XDG_DATA_HOME",
                Path.home()
                / ".local"
                / "share"
            )
        )

    app_directory = (
        base_directory
        / APP_NAME
    )

    app_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    return app_directory


def database_path():
    return (
        user_data_directory()
        / "planner.db"
    )
