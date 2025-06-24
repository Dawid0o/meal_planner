from flask import Flask, jsonify, request
from storage import load_users, save_users, load_recipes
from models.user import User
from models.recipe import Recipe
from models.mealplan import MealPlan

app = Flask(__name__)

@app.route('/')
def index():
    return "API działa dobrze!"

@app.route('/users', methods=['GET'])
def get_users():
    users = load_users()
    return jsonify([u.to_dict() for u in users])

@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = load_recipes()
    ingredient = request.args.get('ingredient', "")
    if ingredient:
        recipes = [r for r in recipes if ingredient.lower() in " ".join(r.ingredients).lower()]
    return jsonify([r.to_dict() for r in recipes])

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get("name", "").strip()
    if not name:
        return jsonify({"error": "Pole 'name' jest wymagane"}), 400
    users = load_users()
    if any(u.name == name for u in users):
        return jsonify({"error": "Użytkownik już istnieje"}), 400
    new = User(name)
    users.append(new)
    save_users(users)
    return jsonify(new.to_dict()), 201

@app.route('/mealplan/<username>', methods=['GET'])
def get_mealplan(username):
    users = load_users()
    u = next((u for u in users if u.name == username), None)
    if not u:
        return jsonify({"error": "Nie znaleziono użytkownika"}), 404
    return jsonify(u.meal_plan.to_dict())

@app.route('/mealplan/<username>', methods=['POST'])
def add_recipe_to_plan(username):
    data = request.get_json()
    day = data.get("day")
    recipe_data = data.get("recipe")
    if not day or not recipe_data:
        return jsonify({"error": "Brak parametrów 'day' lub 'recipe'"}), 400
    users = load_users()
    u = next((u for u in users if u.name == username), None)
    if not u:
        return jsonify({"error": "Nie znaleziono użytkownika"}), 404
    recipe = Recipe(recipe_data["name"], recipe_data["ingredients"])
    try:
        u.meal_plan.add_recipe(day, recipe)
    except AssertionError:
        return jsonify({"error": "Niepoprawny dzień tygodnia"}), 400
    save_users(users)
    return jsonify(u.to_dict()), 200

if __name__ == '__main__':
    app.run()
