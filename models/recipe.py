class Recipe:
    def __init__(self, name: str, ingredients: list[str]):
        assert isinstance(name, str)
        assert isinstance(ingredients, list)
        self.name = name
        self.ingredients = ingredients

    def to_dict(self):
        return {"name": self.name, "ingredients": self.ingredients}

    @classmethod
    def from_dict(cls, d):
        return cls(d["name"], d["ingredients"])

    def __repr__(self):
        return f"<Recipe {self.name}: {self.ingredients}>"
