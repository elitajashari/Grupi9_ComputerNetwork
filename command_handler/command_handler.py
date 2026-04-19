import os

BASE_DIR = "./storage"


def safe_path(user_path: str):
    path = os.path.normpath(os.path.join(BASE_DIR, user_path))
    abs_base = os.path.abspath(BASE_DIR)

    if not os.path.abspath(path).startswith(abs_base):
        return None

    return path


def handle_command(message: str):
    parts = message.split(maxsplit=1)
    command = parts[0]
    arg = parts[1] if len(parts) > 1 else None

    if command == "/list":
        files = os.listdir(BASE_DIR)
        return "OK|" + ",".join(files)

    if command == "/read":
        if not arg:
            return "ERROR|Missing argument"

        path = safe_path(arg)
        if not path or not os.path.exists(path):
            return "ERROR|File not found"

        with open(path, "r") as f:
            return "OK|" + f.read()

    if command == "/delete":
        if not arg:
            return "ERROR|Missing argument"

        path = safe_path(arg)
        if not path or not os.path.exists(path):
            return "ERROR|File not found"

        os.remove(path)
        return "OK|Deleted"

    if command == "/upload":
        if not arg or "|" not in arg:
            return "ERROR|Format: /upload filename|content"

        filename, content = arg.split("|", 1)

        path = safe_path(filename)
        if not path:
            return "ERROR|Invalid path"

        with open(path, "w") as f:
            f.write(content)

        return "OK|Uploaded"

    if command == "/info":
        if not arg:
            return "ERROR|Missing argument"

        path = safe_path(arg)
        if not path or not os.path.exists(path):
            return "ERROR|File not found"

        stat = os.stat(path)
        return f"OK|Size:{stat.st_size}"

    return "ERROR|Unknown command"