from tkinter import Tk
from MainGui import maingui
from glob import glob
from ttkthemes import ThemedTk

appfilename = glob("*timezones*.json")[0]
apptheme = appfilename.split("-")[0].lower()

def main():
    #root = Tk()
    root = ThemedTk(theme=apptheme)
    app = maingui(root, "KeepMyTime", "650x250")
    root.protocol("WM_DELETE_WINDOW", app.destroy)  # Call destroy() when the window is closed
    root.mainloop()

if __name__ == '__main__':
    main()