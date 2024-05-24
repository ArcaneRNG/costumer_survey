import customtkinter as ctk
from tkinter import messagebox
import mysql.connector

def submit_feedback():
    name = name_entry.get()
    experience = experience_var.get()
    recommend = recommend_var.get()
    comments = comment_text.get("1.0", "end-1c")

    if not (name and experience and recommend and comments):
        messagebox.showwarning("Input Error", "All fields are required!")
        return
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='05315',
            database='survey_db'
        )
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO survey_response (name, experience, recommend, comments) VALUES (%s, %s, %s, %s)''',
                       (name, experience, recommend, comments))
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Feedback Received", "Thank you for your feedback!")

        name_entry.delete(0, "end")
        experience_var.set("")
        recommend_var.set("")
        comment_text.delete("1.0", "end")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Arcane Project")
app.geometry("900x600")

frame = ctk.CTkFrame(app, corner_radius=15)
frame.pack(pady=30, padx=30, fill="both", expand=True)

header = ctk.CTkLabel(frame, text="Customer Survey And Feedback", font=ctk.CTkFont("Arial", size=15, weight="bold"))
header.pack(pady=20)

fields = [("Name:", "name_entry")]
for label_text, var_name in fields:
    ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont("Arial", size=15)).pack(pady=5, anchor="n")
    globals()[var_name] = ctk.CTkEntry(frame, width=400, font=ctk.CTkFont("Arial", size=15))
    globals()[var_name].pack(pady=5)

ctk.CTkLabel(frame, text="On a scale of 1 to 5, with 1 being very dissatisfied and 5 being very satisfied, \n"
                         "how would you rate your overall satisfaction with our service?", font=ctk.CTkFont("Arial",
                            size=15)).pack(pady=5, anchor="n")
experience_var = ctk.StringVar()
experience_frame = ctk.CTkFrame(frame)
experience_frame.pack(pady=20, anchor="n")
for experience in ["1", "2", "3", "4", "5"]:
    ctk.CTkRadioButton(experience_frame, text=experience, variable=experience_var, value=experience, font=ctk.CTkFont("Arial",
     size=15)).pack(side="left", padx=10)

ctk.CTkLabel(frame, text="How likely are you to recommend our service to a friend or colleague?", font=ctk.CTkFont("Arial",
                    size=15)).pack(pady=5, anchor="n")
recommend_var = ctk.StringVar()
recommend_frame = ctk.CTkFrame(frame)
recommend_frame.pack(pady=5, anchor="n")
for recommend in ["1", "2", "3", "4", "5"]:
    ctk.CTkRadioButton(recommend_frame, text=recommend, variable=recommend_var, value=recommend, font=ctk.CTkFont("Arial",
        size=15)).pack(side="left", padx=10)

ctk.CTkLabel(frame, text="Feedback about the service", font=ctk.CTkFont("Arial", size=15)).pack(pady=5, anchor="n")
comment_text = ctk.CTkTextbox(frame, width=400, height=90, font=ctk.CTkFont("Arial", size=15))
comment_text.pack(pady=5)

submit_button = ctk.CTkButton(frame, text="Submit", corner_radius=20, font=ctk.CTkFont("Arial", size=15, weight="bold"), command=submit_feedback)
submit_button.pack(pady=20)
app.mainloop()
