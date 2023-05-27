from tkinter import Tk
from MainGui import maingui

def main():
    root = Tk()
    app = maingui(root, "KeepMyTime", "650x250")
    root.protocol("WM_DELETE_WINDOW", app.destroy)  # Call destroy() when the window is closed
    root.mainloop()

if __name__ == '__main__':
    main()