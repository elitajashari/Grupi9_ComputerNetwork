ALLOWED_COMMANDS = {
    "/list": False,
    "/read": True,
    "/upload": True,
    "/download": True,
    "/delete": True,
    "/search": True,
    "/info": True,
}


def validate_message(raw_data: bytes):
    if not raw_data:
        return False, "Empty message"

    if len(raw_data) > 4096:
        return False, "Message too long"

    try:
        message = raw_data.decode("utf-8").strip()
    except UnicodeDecodeError:
        return False, "Invalid UTF-8 message"

    if not message:
        return False, "Empty message after decoding"

    if not message.startswith("/"):
        return False, "Command must start with '/'"

    parts = message.split(maxsplit=1)
    command = parts[0]

    if command not in ALLOWED_COMMANDS:
        return False, "Unknown command"

    requires_argument = ALLOWED_COMMANDS[command]

    if requires_argument:
        if len(parts) < 2 or not parts[1].strip():
            return False, f"{command} requires an argument"

    return True, message
