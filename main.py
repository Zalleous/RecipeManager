from json import dump, load, JSONDecodeError

class Recipe:
    def __init__(self, name, description, ingredients, instructions):
        self.__RECIPE_FOLDER = 'recipes'
        try:
            with open(f'{self.__RECIPE_FOLDER}/{name}.json', 'r') as file:
                raise ValueError("Recipe file already exists. Please delete it before creating a new recipe.")
        except FileNotFoundError:
            self._name = name
            self._description = description
            self._ingredients = ingredients
            self._instructions = instructions

    # Name Setter/Getter
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        if value == '':
            raise ValueError("Recipe name cannot be empty.")
        self._name = value

    # Description Setter/Getter
    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, value):
        if value == '':
            raise ValueError("Description name cannot be empty.")
        self._description = value

    # Ingredients Setter/Getter
    @property
    def ingredients(self):
        return self._ingredients
    @ingredients.setter
    def ingredients(self, value):
        for ingredient in value:
            if not isinstance(ingredient, str) or ingredient == '':
                raise ValueError('Each ingredient must be a non-empty string.')
        self._ingredients = value
    
    # Instructions Setter/Getter
    @property
    def instructions(self):
        return self._instructions
    @instructions.setter
    def instructions(self, value):
        for instructions in value:
            if not isinstance(instructions, str) or instructions == '':
                raise ValueError('Each ingredient must be a non-empty string.')
        self._instructions = value

    def saveRecipe(self):
        recipe_data = {
            "Recipe Name": self.name,
            "Description": self.description,
            "Ingredients": self.ingredients,
            "Instructions": self.instructions
        }
        with open(f'{self.__RECIPE_FOLDER}/{self.name.replace(' ', '_')}.json', 'w') as file:
            dump(recipe_data, file, indent=4)
    
    def loadRecipe(self, recipe_name):
        try:
            with open(f'{self.__RECIPE_FOLDER}/{recipe_name.replace(" ", "_")}.json', 'r') as file:
                recipe_data = load(file)
                self.name = recipe_data['Recipe Name']
                self.description = recipe_data['Description']
                self.ingredients = recipe_data['Ingredients']
                self.instructions = recipe_data['Instructions']
                return recipe_data
        except FileNotFoundError:
            raise FileNotFoundError(f"Recipe '{recipe_name}' not found.")
        except JSONDecodeError:
            raise ValueError("Error decoding the recipe file.")

    
    
if __name__ == "__main__":
    pass