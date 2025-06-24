import customtkinter as ctk
import tkinter as tk
import tkinter.messagebox as mb
from models.user import User
from models.recipe import Recipe
from models.mealplan import MealPlan
from utils.storage import load_users, save_users, load_recipes

class MealPlannerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Planer posiłków")
        self.geometry("1000x600")
        self.users = load_users()
        self.recipes = load_recipes()
        self.selected_user: User | None = None

        self.build_ui()
        self.refresh_users()

    def build_ui(self):
        # Panel użytkowników
        left = ctk.CTkFrame(self, width=200)
        left.pack(side="left", fill="y", padx=10, pady=10)
        ctk.CTkLabel(left, text="Użytkownicy", font=("Arial", 18)).pack(pady=5)
        self.user_listbox = tk.Listbox(left)
        self.user_listbox.pack(fill="y", expand=True)
        self.user_listbox.bind("<<ListboxSelect>>", self.on_user_select)
        ctk.CTkButton(left, text="Dodaj", command=self.add_user_dialog).pack(fill="x", pady=5)
        ctk.CTkButton(left, text="Usuń", command=self.delete_user).pack(fill="x", pady=5)

        # Panel przepisów
        mid = ctk.CTkFrame(self)
        mid.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        ctk.CTkLabel(mid, text="Przepisy", font=("Arial", 18)).pack()
        self.filter_entry = ctk.CTkEntry(mid, placeholder_text="Filtruj składnik...", width=200)
        self.filter_entry.pack(pady=5)
        self.filter_entry.bind("<KeyRelease>", lambda e: self.filter_recipes())
        self.recipe_listbox = tk.Listbox(mid)
        self.recipe_listbox.pack(fill="both", expand=True)

        # Dodano wybór dnia tygodnia
        self.day_combobox = ctk.CTkComboBox(mid, values=[
            "Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"
        ])
        self.day_combobox.pack(pady=5)
        self.day_combobox.set("Poniedziałek")

        ctk.CTkButton(mid, text="Dodaj do planu", command=self.add_recipe_to_plan).pack(pady=5)

        # Panel planu + zakupów
        right = ctk.CTkFrame(self, width=300)
        right.pack(side="left", fill="y", padx=10, pady=10)
        ctk.CTkLabel(right, text="Plan posiłków", font=("Arial", 18)).pack()
        self.plan_text = tk.Text(right, height=20, width=30)
        self.plan_text.pack(pady=5)
        ctk.CTkButton(right, text="Generuj listę zakupów", command=self.generate_shopping_list).pack(pady=5)

    def refresh_users(self):
        self.user_listbox.delete(0, "end")
        for u in self.users:
            self.user_listbox.insert("end", u.name)

    def on_user_select(self, e=None):
        idxs = self.user_listbox.curselection()
        if not idxs: return
        self.selected_user = self.users[idxs[0]]
        self.refresh_plan()

    def add_user_dialog(self):
        dlg = ctk.CTkToplevel(self)
        dlg.geometry("300x150")
        ctk.CTkLabel(dlg, text="Imię użytkownika:").pack(pady=5)
        ent = ctk.CTkEntry(dlg)
        ent.pack(pady=5)
        ctk.CTkButton(dlg, text="Dodaj", command=lambda: self._add_user(ent.get(), dlg)).pack(pady=5)

    def _add_user(self, name, dlg):
        if name.strip():
            u = User(name.strip())
            self.users.append(u)
            save_users(self.users)
            self.refresh_users()
        dlg.destroy()

    def delete_user(self):
        if not self.selected_user: return
        if mb.askyesno("Usuń?", f"Usunąć {self.selected_user.name}?"):
            self.users.remove(self.selected_user)
            save_users(self.users)
            self.refresh_users()
            self.selected_user = None
            self.plan_text.delete("1.0", "end")

    def filter_recipes(self):
        kw = self.filter_entry.get().lower()
        filtered = [r for r in self.recipes if kw in " ".join(r.ingredients).lower()]
        self.recipe_listbox.delete(0, "end")
        for r in filtered:
            self.recipe_listbox.insert("end", r.name)

    def add_recipe_to_plan(self):
        if not self.selected_user:
            mb.showwarning("", "Wybierz użytkownika")
            return
        sel = self.recipe_listbox.curselection()
        if not sel: return
        recipe = [r for r in self.recipes if r.name == self.recipe_listbox.get(sel)][0]
        day = self.day_combobox.get()
        self.selected_user.meal_plan.add_recipe(day, recipe)
        save_users(self.users)
        self.refresh_plan()

    def refresh_plan(self):
        self.plan_text.delete("1.0", "end")
        if not self.selected_user: return
        for day, recs in self.selected_user.meal_plan.days.items():
            self.plan_text.insert("end", f"{day}:\n")
            for r in recs:
                self.plan_text.insert("end", f" - {r.name}\n")
            self.plan_text.insert("end", "\n")

    def generate_shopping_list(self):
        if not self.selected_user:
            mb.showwarning("", "Brak użytkownika")
            return
        ing = []
        for recs in self.selected_user.meal_plan.days.values():
            for r in recs:
                ing += r.ingredients
        unique = sorted(set(ing))
        mb.showinfo("Lista zakupów", "\n".join(unique))

if __name__ == "__main__":
    MealPlannerApp().mainloop()
