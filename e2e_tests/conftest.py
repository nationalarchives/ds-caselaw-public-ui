import os
import socket

import pytest


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    vite_host = os.environ.get("E2E_VITE_HOST")
    if not vite_host:
        return browser_type_launch_args

    # Vite runs on the host, while the E2E browser runs in Docker.
    vite_address = socket.gethostbyname(vite_host)
    return {
        **browser_type_launch_args,
        "args": [
            *browser_type_launch_args.get("args", []),
            f"--host-resolver-rules=MAP localhost:5173 {vite_address}:5173",
        ],
    }
