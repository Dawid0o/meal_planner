import json
from models.user import User
from models.recipe import Recipe
import csv

def load_recipes(filename="data/recipes.json") -> list[Recipe]:
    with open(filename, encoding="utf-8") as f:
        return [Recipe.from_dict(d) for d in json.load(f)]

def load_users(filename="data/users.json") -> list[User]:
    with open(filename, encoding="utf-8") as f:
        return [User.from_dict(d) for d in json.load(f)]

def save_users(users: list[User], filename="data/users.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([u.to_dict() for u in users], f, indent=2, ensure_ascii=False)
def save_users_to_csv(users, filename="users.csv"):

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Imię", "Dzień", "Przepis", "Składniki"])
        for user in users:
            for day, recipes in user.meal_plan.days.items():
                for r in recipes:
                    writer.writerow([user.name, day, r.name, ", ".join(r.ingredients)])
