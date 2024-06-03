import inspect
import os
from pathlib import Path


def get_caller_name():
    # Get the current stack frame
    stack = inspect.stack()

    # Find stack frame for the calling script
    for frame in stack:
        frame_path = os.path.abspath(inspect.getframeinfo(frame[0]).filename)

        if frame_path.find("common") == -1:
            path = Path(frame_path)
            parent = path.parent

            if path.parent.name == "src":
                parent = parent.parent

            return (parent, path.stem)

    return None
