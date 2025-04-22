from pynput import keyboard

# =============================================
# Function: on_press
# Purpose: Called every time a key is pressed.
#          Handles both alphanumeric and special keys.
# =============================================
def on_press(key):
    try:
        # Attempt to print alphanumeric key (e.g., a, b, 1)
        print(key.char, end='', flush=True)
    except AttributeError:
        # Handle special keys like Enter, Shift, etc.
        if key == keyboard.Key.enter:
            print()  # Print a newline on Enter
        # You can log other special keys if needed
        # elif key == keyboard.Key.space:
        #     print(' ', end='')

# =============================================
# Function: on_release
# Purpose: Called when a key is released.
#          Returns False if the escape key is pressed, stopping the listener.
# =============================================
def on_release(key):
    if key == keyboard.Key.esc:
        return False  # Stop the listener

# =============================================
# Main Listener (Blocking Version)
# Description: Starts the keyboard listener and blocks the program until ESC is pressed.
# =============================================
if __name__ == "__main__":
    print("Start typing... (Press ESC to quit)")
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
        listener.join()  # This will block until the listener is stopped
