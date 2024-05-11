import os
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import datetime
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pytz

def authenticate_google():
    dir_path = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(dir_path, 'credentials.json')

    creds = None
    try:
        creds = Credentials.from_authorized_user_file(os.path.join(dir_path, 'token.json'))
    except Exception as e:
        print("Error loading token.json:", e)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes=['https://www.googleapis.com/auth/calendar'])
                creds = flow.run_local_server(port=0)
            except FileNotFoundError:
                print(f"Failed to find the credentials file at {credentials_path}")
                return None
            except Exception as e:
                print("An error occurred during authentication:", e)
                return None

            with open(os.path.join(dir_path, 'token.json'), 'w') as token:
                token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

def create_event(service, summary, date, start_time, end_time, location, attendees):
    timezone = 'America/Toronto'
    tz = pytz.timezone(timezone)
    start_datetime = datetime.datetime.strptime(f"{date} {start_time}", '%m/%d/%Y %H:%M')
    end_datetime = datetime.datetime.strptime(f"{date} {end_time}", '%m/%d/%Y %H:%M')
    start_datetime = tz.localize(start_datetime)
    end_datetime = tz.localize(end_datetime)

    event = {
        'summary': summary,
        'location': location,
        'start': {'dateTime': start_datetime.isoformat(), 'timeZone': timezone},
        'end': {'dateTime': end_datetime.isoformat(), 'timeZone': timezone},
        'attendees': [{'email': email.strip()} for email in attendees.split(',') if email.strip()]
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    show_confirmation_popup(event['htmlLink'])

def show_confirmation_popup(event_url):
    popup = tk.Toplevel()
    popup.title("Event Created")
    tk.Label(popup, text="The event was created successfully!").pack(pady=10)
    ttk.Button(popup, text="OK", command=popup.destroy).pack(side=tk.LEFT, padx=10, pady=5)
    ttk.Button(popup, text="View Event", command=lambda: webbrowser.open(event_url)).pack(side=tk.RIGHT, padx=10, pady=5)

def open_calendar():
    def set_date():
        date_var.set(cal.selection_get().strftime("%m/%d/%Y"))
        top.destroy()

    top = tk.Toplevel()
    cal = Calendar(top, selectmode='day', year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day)
    cal.pack(pady=20, padx=20)
    ttk.Button(top, text="OK", command=set_date).pack()

def submit_event():
    event_name = event_name_var.get()
    date = date_var.get()
    start_time = start_time_var.get()
    end_time = end_time_var.get()
    location = location_var.get()
    attendees = attendees_var.get()

    service = authenticate_google()
    create_event(service, event_name, date, start_time, end_time, location, attendees)

    event_name_var.set("")
    location_var.set("")
    attendees_var.set("")

root = tk.Tk()
root.title("Google Calendar Event Creator")
root.geometry('300x250')

style = ttk.Style()
style.theme_use('clam')

style.configure('TButton', background='#333', foreground='white', font=('Helvetica', 10))
style.map('TButton', background=[('active', '#666')])

style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))

for i in range(7):
    root.grid_rowconfigure(i, pad=10)
root.grid_columnconfigure(0, pad=10)
root.grid_columnconfigure(2, pad=10)

ttk.Label(root, text="Enter the event name:").grid(row=0, column=0, sticky='w')
event_name_var = tk.StringVar()
ttk.Entry(root, textvariable=event_name_var).grid(row=0, column=1, sticky='ew')

date_var = tk.StringVar()
ttk.Entry(root, textvariable=date_var, state='readonly').grid(row=1, column=1, sticky='ew')
ttk.Button(root, text="Select Date", command=open_calendar).grid(row=1, column=0, sticky='w')

ttk.Label(root, text="Select start time:").grid(row=2, column=0, sticky='w')
start_time_var = tk.StringVar()
ttk.Combobox(root, textvariable=start_time_var, values=[f"{h:02d}:{m:02d}" for h in range(0, 24) for m in range(0, 60, 15)]).grid(row=2, column=1, sticky='ew')

ttk.Label(root, text="Select end time:").grid(row=3, column=0, sticky='w')
end_time_var = tk.StringVar()
ttk.Combobox(root, textvariable=end_time_var, values=[f"{h:02d}:{m:02d}" for h in range(0, 24) for m in range(0, 60, 15)]).grid(row=3, column=1, sticky='ew')

ttk.Label(root, text="Enter location:").grid(row=4, column=0, sticky='w')
location_var = tk.StringVar()
ttk.Entry(root, textvariable=location_var).grid(row=4, column=1, sticky='ew')

ttk.Label(root, text="Invite:").grid(row=5, column=0, sticky='w')
attendees_var = tk.StringVar()
ttk.Entry(root, textvariable=attendees_var).grid(row=5, column=1, sticky='ew')

ttk.Button(root, text="Create Event", command=submit_event).grid(row=6, columnspan=2)

root.mainloop()
