import os
import subprocess
from pathlib import Path


WORKSPACE = Path.home() / "daemon-ai" / "workspace"


def setup_workspace():
    WORKSPACE.mkdir(exist_ok=True)


def list_files():
    setup_workspace()

    files = []

    for file in WORKSPACE.rglob("*"):
        if file.is_file():
            files.append(
                str(file.relative_to(WORKSPACE))
            )

    return files


def read_file(filename):
    setup_workspace()

    path = WORKSPACE / filename

    if not path.exists():
        return "File does not exist."

    return path.read_text()


def write_file(filename, content):
    setup_workspace()

    path = WORKSPACE / filename

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(content)

    return f"Created {filename}"


def run_command(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=20
        )

        return (
            result.stdout
            + result.stderr
        )

    except Exception as e:
        return str(e)


def open_app(app):

    apps = {
        "chromium": "chromium",
        "firefox": "firefox",
        "zen": "zen",
        "terminal": "kitty"
    }


    if app in apps:
        subprocess.Popen(
            apps[app]
        )

        return f"Opened {app}"

    return "Unknown application"
