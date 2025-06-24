from models.recipe import Recipe

class MealPlan:
    def __init__(self):
        # dni tygodnia: lista przepisów (śniadanie, obiad, kolacja razem)
        self.days: dict[str, list[Recipe]] = {
            day: [] for day in [
                "Poniedziałek", "Wtorek", "Środa",
                "Czwartek", "Piątek", "Sobota", "Niedziela"
            ]
        }

    def add_recipe(self, day: str, recipe: Recipe):
        if day not in self.days:
            raise ValueError(f"Nieprawidłowy dzień tygodnia: {day}")
        self.days[day].append(recipe)

    def to_dict(self):
        return {
            day: [r.to_dict() for r in recipes]
            for day, recipes in self.days.items()
        }

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls()
        for day, recipes in data.items():
            obj.days[day] = [Recipe.from_dict(r) for r in recipes]
        return obj
