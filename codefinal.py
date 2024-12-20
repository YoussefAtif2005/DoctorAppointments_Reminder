import datetime
import pywhatkit
import schedule
import time
import threading
import customtkinter as ctk

# Function to schedule and send the WhatsApp message
def schedule_message():
    try:
        phone_number = entry_phone.get()
        message = entry_message.get()
        numb_days = int(entry_days.get())

        # Validate inputs
        if not phone_number.startswith('+') or not phone_number[1:].isdigit():
            result_label.configure(text="Error: Enter a valid phone number (e.g., +123456789).")
            return

        if not message:
            result_label.configure(text="Error: Message cannot be empty.")
            return

        # Calculate execution date
        time_diff = datetime.timedelta(days=numb_days - 1)
        todays_date = datetime.datetime.now()
        execution_date = todays_date + time_diff

        # Function to send the WhatsApp message
        def send_message():
            pywhatkit.sendwhatmsg_instantly(phone_number, message, 5, True, 3)
            result_label.configure(text="Message sent successfully!")

        # Schedule the message
        def schedule_task():
            while True:
                current_date = datetime.datetime.now()
                if str(current_date).split(" ")[0] == str(execution_date).split(" ")[0]:
                    send_message()
                    break
                time.sleep(1)

        threading.Thread(target=schedule_task, daemon=True).start()
        result_label.configure(text=f"Message scheduled for {execution_date.date()}.")

    except ValueError:
        result_label.configure(text="Error: 'Après combien de jours' must be a number.")

# Initialize the CustomTkinter window
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

app = ctk.CTk()
app.title("WhatsApp Message Scheduler")
app.geometry("500x400")

# Input fields
label_phone = ctk.CTkLabel(app, text="Numéro du patient (e.g., +123456789):")
label_phone.pack(pady=5)
entry_phone = ctk.CTkEntry(app, width=300)
entry_phone.pack(pady=5)

label_message = ctk.CTkLabel(app, text="Message à envoyer:")
label_message.pack(pady=5)
entry_message = ctk.CTkEntry(app, width=300)
entry_message.pack(pady=5)

label_days = ctk.CTkLabel(app, text="Après combien de jours:")
label_days.pack(pady=5)
entry_days = ctk.CTkEntry(app, width=300)
entry_days.pack(pady=5)

# Schedule button
schedule_button = ctk.CTkButton(app, text="Schedule Message", command=schedule_message)
schedule_button.pack(pady=20)

# Result label
result_label = ctk.CTkLabel(app, text="")
result_label.pack(pady=10)

# Run the GUI
app.mainloop()
