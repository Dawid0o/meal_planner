from models.mealplan import MealPlan

class User:
    def __init__(self, name: str, meal_plan: MealPlan = None):
        self.name = name
        self.meal_plan = meal_plan or MealPlan()

    def to_dict(self):
        return {
            "name": self.name,
            "meal_plan": self.meal_plan.to_dict()
        }

    @classmethod
    def from_dict(cls, d):
        mp = MealPlan.from_dict(d.get("meal_plan", {}))
        return cls(d["name"], mp)

    def __repr__(self):
        return f"<User {self.name}>"
