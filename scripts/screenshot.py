from PIL import ImageGrab


def handle_screenshot():
    global encoded_message, command_tag, message
    command_tag = "SCR"
    with open("screenshot_client.png", "rb") as f:
        encoded_message = f.read()
    message = 1
    # print("Screenshot uspješno napravljen.")


screenshot = ImageGrab.grab()
screenshot.save("screenshot_client.png")
handle_screenshot()