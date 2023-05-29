import datetime
import pytz
import json
from tkinter import ttk
from pytz import timezone
from dateutil.relativedelta import relativedelta
from datetime import datetime
from glob import glob


appfilename = glob("*timezones*.json")[0]

class ShowTime_Page:
    def __init__(self, parent, window):
        self.parent = parent
        self.window = window
        self.frame = ttk.Frame(window)
        self.frame = ttk.Treeview(window, columns=('Name', 'Description', 'Date', 'Time', 'HoursDiff'), show='headings')

        # Initialize columns
        self.frame.column('Name', width=100, anchor='center')
        self.frame.column('Description', width=100, anchor='center')
        self.frame.column('Date', width=100, anchor='center')
        self.frame.column('Time', width=50, anchor='w')
        self.frame.column('HoursDiff', width=100, anchor='center')

        # Define headings
        self.frame.heading('Name', text='Name')
        self.frame.heading('Description', text='Description')
        self.frame.heading('Date', text='Date')
        self.frame.heading('Time', text='Time')
        self.frame.heading('HoursDiff', text='HoursDiff')

        self.load_data()
        self.update_treeview()
        self.frame.pack()

    def load_data(self):

        with open(appfilename) as f:
            self.data = json.load(f)

        self.local_tz_data = self.data['local']
        self.other_tzs_data = self.data['others']
        self.time_info = self.create_time_in_zones()

    def create_time_in_zones(self):
        local_timezone = pytz.timezone(self.local_tz_data['zone'])
        local_time = datetime.now(local_timezone)

        time_info = []

        # Add local timezone info
        time_info.append({
            'name': self.local_tz_data['zone'],
            'date': local_time.strftime('%Y-%m-%d'),
            'time': local_time.strftime('%H:%M'),
            'diff': '00',
            'description': self.local_tz_data['description']
        })

        # Add other timezone info
        for tz_data in self.other_tzs_data:
            tz = tz_data['zone']
            timezone2 = pytz.timezone(tz)
            current_time = datetime.now(timezone2)
            iolo = self.local_tz_data['zone']

            utcnow2 = timezone('utc').localize(datetime.utcnow())  # generic time
            here = utcnow2.astimezone(timezone(self.local_tz_data['zone'])).replace(tzinfo=None)
            there = utcnow2.astimezone(timezone(tz_data['zone'])).replace(tzinfo=None)
            time_diff = relativedelta(here, there)
            hoursMinutes = f"{time_diff.hours}:{time_diff.minutes}"
            time_info.append({
                'name': tz,
                'date': current_time.strftime('%Y-%m-%d'),
                'time': current_time.strftime('%H:%M    '),
                'diff': str(hoursMinutes),
                'description': tz_data['description']
            })

        return time_info

    def update_treeview(self):
        # Clear previous contents
        for i in self.frame.get_children():
            self.frame.delete(i)

        # Reload data and update treeview
        self.load_data()

        for info in self.time_info:
            self.frame.insert(
                "",
                "end",
                values=(
                    info["name"],
                    info["description"],
                    info["date"],
                    info["time"],
                    info["diff"],
                ),
            )
        # Autoresize columns
        self.autosize_columns()

        # Reschedule the method after 3000 ms (3 seconds)
        self.window.after(60000, self.update_treeview)

    def autosize_columns(self):
        for column in self.frame['columns']:
            max_width = max(self.frame.column(column, 'width'), max(len(str(self.frame.set(child, column))) for child in self.frame.get_children()))
            self.frame.column(column, width=int(max_width * 1))

    def destroy(self):
        self.frame.destroy()