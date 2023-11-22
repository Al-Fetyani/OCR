from pynput.mouse import Listener
from PIL import Image, ImageGrab
import tkinter as tk

def start_listener():
    with Listener(on_move=on_move, on_click=on_click) as listener:
        root.mainloop()

def on_move(x, y):
    global ix, iy, rectangle_id
    if pressed:
        canvas.coords(rectangle_id, ix, iy, x, y)

def on_click(x, y, button, p):
    global ix, iy, rectangle_id, pressed
    pressed = p
    if button == button.left:
        if pressed:
            ix = x
            iy = y
            print('left button pressed at {0}'.format((x, y)))
            rectangle_id = canvas.create_rectangle(ix, iy, x, y, outline='red', width=2)
        else:
            print('left button released at {0}'.format((x, y)))
            root.wm_attributes('-alpha', 0)
            with open('screenshot_coordinates.txt', 'w') as f:
                f.write(f'{ix},{iy},{x},{y}')
            root.quit()

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root_geometry = str(screen_width) + 'x' + str(screen_height)
root.geometry(root_geometry)
root.overrideredirect(True)
root.wait_visibility(root)
root.wm_attributes("-alpha", 0.3)

canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.config(cursor="cross")
canvas.pack()

ix, iy = 0, 0
rectangle_id = None
pressed = False

start_listener()
