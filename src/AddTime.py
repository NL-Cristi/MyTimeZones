import json
import tkinter
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo
import pytz
from ttkwidgets.autocomplete import AutocompleteCombobox
from glob import glob


appfilename = glob("*timezones*.json")[0]
class AddTime_Page:
    def __init__(self, parent, window):
        self.parent = parent
        self.window = window
        self.frame = ttk.Treeview(window, columns=('Name', 'Description'), show='headings')

        # Initialize columns
        self.frame.column('Name', width=100, anchor='center')
        self.frame.column('Description', width=200, anchor='center')

        # Define headings
        self.frame.heading('Name', text='Name')
        self.frame.heading('Description', text='Description')

        self.load_data()
        self.update_treeview()
        self.myFrame = ttk.Frame()

        allTimezones = pytz.all_timezones

        self.name_label = ttk.Label(self.myFrame,text="TimeZone")
        self.name_entry = entry = AutocompleteCombobox(self.myFrame, width=20, completevalues=allTimezones)
        self.description_label = ttk.Label(self.myFrame,text="Description")
        self.description_entry = ttk.Entry(self.myFrame)
        self.name_label.grid(row=0, column=0)
        self.name_entry.grid(row=0, column=1)
        self.description_label.grid(row=0, column=2)
        self.description_entry.grid(row=0, column=3)

        self.add_button = ttk.Button(self.myFrame, text='Add', command=self.add_timezone)
        self.edit_button = ttk.Button(self.myFrame, text='Modify', command=self.edit_timezone)
        self.delete_button = ttk.Button(self.myFrame, text='Delete', command=self.remove_timezone)
        self.add_button.grid(row=2, column=1, padx=5, pady=5)
        self.edit_button.grid(row=2, column=2, padx=5, pady=5)
        self.delete_button.grid(row=2, column=3, padx=5, pady=5)

        self.myFrame.pack()

        # Bind a function to select event
        self.frame.bind('<<TreeviewSelect>>', self.on_select)
        self.frame.pack()

    def load_data(self):
        with open(appfilename) as f:
            self.data = json.load(f)
        self.local_tz_data = self.data['local']
        self.other_tzs_data = self.data['others']

    def update_treeview(self):
        # Clear previous contents
        for i in self.frame.get_children():
            self.frame.delete(i)

        # Reload data and update treeview
        self.load_data()

        self.frame.insert("", "end", values=(self.local_tz_data["zone"], self.local_tz_data["description"]))
        for tz in self.other_tzs_data:
            self.frame.insert("", "end", values=(tz["zone"], tz["description"]))

        # Autoresize columns
        self.autosize_columns()

    def autosize_columns(self):
        for column in self.frame['columns']:
            max_width = max(self.frame.column(column, 'width'),
                            max(len(str(self.frame.set(child, column))) for child in self.frame.get_children()))
            self.frame.column(column, width=int(max_width * 1))

    def add_timezone(self):
        new_name = self.name_entry.get()
        new_description = self.description_entry.get()

        if new_name and new_description:
            # Add to the list
            self.other_tzs_data.append({"zone": new_name, "description": new_description})

            # Save back to the JSON file
            with open(appfilename, 'w') as f:
                json.dump({"local": self.local_tz_data, "others": self.other_tzs_data}, f)

            # Clear entry fields
            self.name_entry.delete(0, 'end')
            self.description_entry.delete(0, 'end')

            # Update the TreeView
            self.update_treeview()

    def on_select(self, event):
        # Get selected row values
        selected_item = self.frame.item(self.frame.selection())
        selected_values = selected_item["values"]

        # Set the values in entry fields
        self.name_entry.delete(0, 'end')
        self.description_entry.delete(0, 'end')
        self.name_entry.insert(0, selected_values[0])
        self.description_entry.insert(0, selected_values[1])

    def edit_timezone(self):
        # Get selected row values
        selected_item = self.frame.item(self.frame.selection())
        selected_values = selected_item["values"]

        # Get current entries
        current_name = self.name_entry.get()
        current_description = self.description_entry.get()

        # Check if the selected item is the local timezone
        if selected_values[0] == self.local_tz_data["zone"]:
            # Update the local timezone
            self.local_tz_data = {"zone": current_name, "description": current_description}
        else:
            # Update other timezone
            for tz in self.other_tzs_data:
                if tz["zone"] == selected_values[0]:
                    tz["zone"] = current_name
                    tz["description"] = current_description
                    break

        # Save back to the JSON file
        with open(appfilename, 'w') as f:
            json.dump({"local": self.local_tz_data, "others": self.other_tzs_data}, f)

        # Clear entry fields
        self.name_entry.delete(0, 'end')
        self.description_entry.delete(0, 'end')

        # Update the TreeView
        self.update_treeview()

    def remove_timezone(self):
        # Get selected row values
        selected_item = self.frame.item(self.frame.selection())
        selected_values = selected_item["values"]

        # Check if the selected item is the local timezone
        if selected_values[1] == self.local_tz_data["description"]:
            showwarning(
                title='Warning',
                message="You cannot Delete your timezone!!!")
            return

        # Remove the selected timezone
        self.other_tzs_data = [tz for tz in self.other_tzs_data if tz["zone"] != selected_values[0]]

        # Save back to the JSON file
        with open(appfilename, 'w') as f:
            json.dump({"local": self.local_tz_data, "others": self.other_tzs_data}, f)

        # Update the TreeView
        self.update_treeview()

    def destroy(self):
        self.description_entry.destroy()
        self.myFrame.destroy()
        self.name_entry.destroy()
        self.add_button.destroy()
        self.edit_button.destroy()
        self.delete_button.destroy()
        self.frame.destroy()
