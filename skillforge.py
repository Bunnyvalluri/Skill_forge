import json
import customtkinter as ctk
from tkinter import messagebox

FILE = "skills.json"

# ----------- File Handling -----------
def load_skills():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_skills(skills):
    with open(FILE, "w") as f:
        json.dump(skills, f, indent=4)

# ----------- GUI Setup -----------
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("SkillForge - Personal Skill Tracker")
app.geometry("600x650")
app.resizable(False, False)

# ----------- Frames -----------
header_frame = ctk.CTkFrame(app)
form_frame = ctk.CTkFrame(app)
button_frame = ctk.CTkFrame(app)
list_frame = ctk.CTkFrame(app)

header_frame.pack(pady=10)
form_frame.pack(pady=10, fill="x", padx=20)
button_frame.pack(pady=10)
list_frame.pack(pady=10)

# ----------- Header -----------
title_label = ctk.CTkLabel(header_frame, text="🛠 SkillForge", font=("Arial", 28, "bold"))
subtitle_label = ctk.CTkLabel(header_frame, text="Track and grow your skills", font=("Arial", 16))
title_label.pack()
subtitle_label.pack()

# ----------- Form Inputs -----------
skill_label = ctk.CTkLabel(form_frame, text="Skill Name:")
skill_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter skill name")

level_label = ctk.CTkLabel(form_frame, text="Skill Level:")
level_option = ctk.CTkOptionMenu(form_frame, values=["Beginner", "Intermediate", "Advanced"])

filter_label = ctk.CTkLabel(form_frame, text="Filter by Level:")
filter_option = ctk.CTkOptionMenu(form_frame, values=["All", "Beginner", "Intermediate", "Advanced"], command=lambda level: filter_skills(level))

skill_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
skill_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
level_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
level_option.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
filter_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
filter_option.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
form_frame.columnconfigure(1, weight=1)

# ----------- Buttons -----------
add_button = ctk.CTkButton(button_frame, text="➕ Add Skill", width=130, command=lambda: add_skill())
update_button = ctk.CTkButton(button_frame, text="✏️ Update Selected", width=130, command=lambda: update_skill())
delete_button = ctk.CTkButton(button_frame, text="🗑 Delete Selected", width=130, command=lambda: delete_skill())
summary_button = ctk.CTkButton(button_frame, text="📊 Show Summary", width=130, command=lambda: show_summary())

add_button.grid(row=0, column=0, padx=10, pady=5)
update_button.grid(row=0, column=1, padx=10, pady=5)
delete_button.grid(row=1, column=0, padx=10, pady=5)
summary_button.grid(row=1, column=1, padx=10, pady=5)

# ----------- Skill List Display -----------
list_label = ctk.CTkLabel(list_frame, text="Your Skills", font=("Arial", 16, "bold"))
skill_listbox = ctk.CTkTextbox(list_frame, width=540, height=250, corner_radius=10)

list_label.pack(pady=5)
skill_listbox.pack()

# ----------- Core Operations -----------
def refresh_skills():
    filter_skills("All")

def filter_skills(level):
    skill_listbox.delete("1.0", "end")
    skills = load_skills()
    filtered = [s for s in skills if level == "All" or s["level"] == level]
    if not filtered:
        skill_listbox.insert("end", "❌ No skills found.\n")
    else:
        for i, s in enumerate(filtered, 1):
            skill_listbox.insert("end", f"{i}. {s['skill']} - {s['level']}\n")

def add_skill():
    name = skill_entry.get().strip()
    level = level_option.get()
    if name:
        skills = load_skills()
        skills.append({"skill": name, "level": level})
        save_skills(skills)
        refresh_skills()
        messagebox.showinfo("Success", f"✅ {name} added successfully!")
        skill_entry.delete(0, "end")
    else:
        messagebox.showerror("Error", "❌ Skill name cannot be empty.")

def update_skill():
    try:
        idx = int(app.clipboard_get()) - 1
        skills = load_skills()
        if 0 <= idx < len(skills):
            new_name = skill_entry.get().strip()
            new_level = level_option.get()
            if new_name:
                skills[idx] = {"skill": new_name, "level": new_level}
                save_skills(skills)
                refresh_skills()
                messagebox.showinfo("Updated", "✅ Skill updated successfully!")
            else:
                messagebox.showerror("Error", "❌ Skill name cannot be empty.")
        else:
            messagebox.showerror("Error", "❌ Invalid skill number.")
    except:
        messagebox.showerror("Error", "❌ Copy the skill number to clipboard to update.")

def delete_skill():
    try:
        idx = int(app.clipboard_get()) - 1
        skills = load_skills()
        if 0 <= idx < len(skills):
            removed = skills.pop(idx)
            save_skills(skills)
            refresh_skills()
            messagebox.showinfo("Deleted", f"🗑 {removed['skill']} deleted successfully!")
        else:
            messagebox.showerror("Error", "❌ Invalid skill number.")
    except:
        messagebox.showerror("Error", "❌ Copy the skill number to clipboard to delete.")

def show_summary():
    skills = load_skills()
    summary = {"Beginner": 0, "Intermediate": 0, "Advanced": 0}
    for s in skills:
        summary[s["level"]] += 1
    messagebox.showinfo("Skill Summary",
        f"📊 Skill Levels:\nBeginner: {summary['Beginner']}\nIntermediate: {summary['Intermediate']}\nAdvanced: {summary['Advanced']}")

# ----------- Start App -----------
refresh_skills()
app.mainloop()
