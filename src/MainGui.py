from tkinter import Menu
from AddTime import *
from ShowTime import *

class maingui:
    def __init__(self, root, title, geometry):
        self.root = root
        self.root.title(title)
        self.menubar = Menu(root)
        self.root.config(menu=self.menubar)
        self.current_page = None
        # create a menu
        self.file_menu = Menu(
            self.menubar,
            tearoff=0
        )
        # add menu items to the File menu
        self.file_menu.add_command(label='ShowTime', command=self.showTime)
        self.file_menu.add_command(label='EditZones', command=self.editTime)
        self.file_menu.add_command(label='Close', command=self.root.destroy)
        self.file_menu.add_separator()
        # add the File menu to the menubar
        self.menubar.add_cascade(
            label="File",
            menu=self.file_menu
        )
        # create the Help menu
        # create the Help menu
        self.help_menu = Menu(
            self.menubar,
            tearoff=0
        )
        self.help_menu.add_command(label='Welcome')
        self.help_menu.add_command(label='About...')

        # add the Help menu to the menubar
        self.menubar.add_cascade(
            label="Help",
            menu=self.help_menu
        )
        self.current_page= ShowTime_Page(self, self.root)

    def showTime(self):
        if isinstance(self.current_page, ShowTime_Page):
            return  # Do nothing if the current page is already ShowTime_Page

        if self.current_page:
            self.current_page.destroy()

        if isinstance(self.current_page, AddTime_Page):
            self.current_page.destroy()  # Call destroy_buttons() to destroy the buttons in AddTime_Page

        self.root.title("ShowTime")
        self.current_page = ShowTime_Page(self, self.root)

    def editTime(self):
        if isinstance(self.current_page, AddTime_Page):
            return  # Do nothing if the current page is already AddTime_Page

        if self.current_page:
            self.current_page.destroy()

        if isinstance(self.current_page, ShowTime_Page):
            self.current_page.destroy()  # Call destroy_buttons() to destroy the buttons in ShowTime_Page

        self.root.title("AddTime")
        self.current_page = AddTime_Page(self, self.root)

    def destroy(self):
        if self.current_page:
            self.current_page.destroy()
        self.root.destroy()
