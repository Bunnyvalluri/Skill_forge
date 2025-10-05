# SkillForge - Personal Skill Tracker

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
app.geometry("520x600")

# ----------- Widgets -----------
skill_entry = ctk.CTkEntry(app, placeholder_text="Skill Name")
level_option = ctk.CTkOptionMenu(app, values=["Beginner", "Intermediate", "Advanced"])
filter_option = ctk.CTkOptionMenu(app, values=["All", "Beginner", "Intermediate", "Advanced"], command=lambda level: filter_skills(level))

add_button = ctk.CTkButton(app, text="➕ Add Skill", command=lambda: add_skill())
update_button = ctk.CTkButton(app, text="✏️ Update Selected", command=lambda: update_skill())
delete_button = ctk.CTkButton(app, text="🗑 Delete Selected", command=lambda: delete_skill())
summary_button = ctk.CTkButton(app, text="📊 Show Summary", command=lambda: show_summary())

skill_listbox = ctk.CTkTextbox(app, width=460, height=250)

# ----------- Layout -----------
skill_entry.pack(pady=10)
level_option.pack(pady=5)
filter_option.pack(pady=5)
add_button.pack(pady=5)
update_button.pack(pady=5)
delete_button.pack(pady=5)
summary_button.pack(pady=5)
skill_listbox.pack(pady=10)

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
