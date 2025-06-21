import os
from json import dump, load, JSONDecodeError

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QGridLayout, QWidget, QLabel, QTabWidget,
    QLineEdit, QPushButton
)
from win32api import GetSystemMetrics


class Recipe:
    def __init__(self, name, description, ingredients, instructions, recipe_folder='recipes'):
        self.__RECIPE_FOLDER = recipe_folder
        if not os.path.exists(self.__RECIPE_FOLDER):
            os.makedirs(self.__RECIPE_FOLDER)
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

    # RECIPE_FOLDER Setter/Getter
    @property
    def RECIPE_FOLDER(self):
        return self.__RECIPE_FOLDER

    @RECIPE_FOLDER.setter
    def RECIPE_FOLDER(self, value):
        if not os.path.exists(value):
            os.makedirs(value)
        self.__RECIPE_FOLDER = value

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recipe Manager")
        self.__ScreenWidth = GetSystemMetrics(0)
        self.__ScreenHeight = GetSystemMetrics(1)
        self.__appWidth = 800
        self.__appHeight = 600
        self.setGeometry(
            self.__ScreenWidth / 2 - self.__appWidth / 2,
            self.__ScreenHeight / 2 - self.__appHeight / 2,
            self.__appWidth,
            self.__appHeight
        )

        layout = QGridLayout()
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        titleLabel = QLabel("Recipe Manager", self)
        titleLabel.setStyleSheet("font-size: 24px; font-weight: normal; font-family: Brass Mono;")

        layout.addWidget(titleLabel, 0, 0, Qt.AlignmentFlag.AlignCenter)

        layout.setContentsMargins(10, 10, 10, 10)

        self.loadingPage = QWidget()
        self.savePage = QWidget()
        self.settingsPage = QWidget()

        self.currentSaveFolder = os.path.join(os.getcwd(), 'recipes')

        tabWidget = QTabWidget()
        tabWidget.addTab(self.loadingPage, "Loading")
        tabWidget.addTab(self.savePage, "Saving")
        tabWidget.addTab(self.settingsPage, "Settings")

        layout.addWidget(tabWidget, 1, 0, 1, 1)

        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 1)

        layout.setColumnStretch(0, 1)

        self.initLoadTab()
        self.initSaveTab()
        self.initSettingsTab()

    def initSaveTab(self):
        layout = QGridLayout(self.savePage)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(20, 20, 20, 20)

        # Add input fields for recipe details
        titleLabel = QLabel("Title", self)
        layout.addWidget(titleLabel, 0, 0)
        self.titleInput = QLineEdit(self, placeholderText="Enter recipe title")
        layout.addWidget(self.titleInput, 0, 1)

        # Add input fields for recipe description
        descriptionLabel = QLabel("Description", self)
        layout.addWidget(descriptionLabel, 1, 0)
        self.descriptionInput = QLineEdit(self, placeholderText="Enter recipe description")
        layout.addWidget(self.descriptionInput, 1, 1)

        # Add input fields for ingredients
        ingredientsLabel = QLabel("Ingredients (comma separated)", self)
        layout.addWidget(ingredientsLabel, 2, 0)
        self.ingredientsInput = QLineEdit(self, placeholderText="Enter ingredients")
        layout.addWidget(self.ingredientsInput, 2, 1)

        # Add input fields for instructions
        instructionsLabel = QLabel("Instructions (comma separated)", self)
        layout.addWidget(instructionsLabel, 3, 0)
        self.instructionsInput = QLineEdit(self, placeholderText="Enter instructions")
        layout.addWidget(self.instructionsInput, 3, 1)

        # Add a button to save the recipe
        saveButton = QPushButton("Save Recipe", self)
        saveButton.clicked.connect(lambda: self.saveRecipe())
        layout.addWidget(saveButton, 4, 0, 1, 2, Qt.AlignmentFlag.AlignRight)

    def initLoadTab(self):
        layout = QGridLayout(self.loadingPage)
        label = QLabel("Load your recipe here", self)
        layout.addWidget(label, 0, 0, Qt.AlignmentFlag.AlignCenter)

    def initSettingsTab(self):
        layout = QGridLayout(self.settingsPage)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(20, 20, 20, 20)

        # Add input for recipe folder
        folderLabel = QLabel("Recipe Folder", self)
        layout.addWidget(folderLabel, 0, 0)
        self.folderInput = QLineEdit(self, placeholderText="Enter folder path")
        layout.addWidget(self.folderInput, 0, 1)

        # Add a button to set the recipe folder
        setFolderButton = QPushButton("Set Recipe Folder", self)
        setFolderButton.clicked.connect(self.setRecipeFolder)
        layout.addWidget(setFolderButton, 1, 0, 1, 2, Qt.AlignmentFlag.AlignRight)

        # Display current recipe folder
        self.currentFolderLabel = QLabel(f"Current Recipe Folder: {self.currentSaveFolder}", self)
        layout.addWidget(self.currentFolderLabel, 2, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

    def saveRecipe(self):
        name = self.titleInput.text()
        description = self.descriptionInput.text()
        ingredients = self.ingredientsInput.text().split(',')
        instructions = self.instructionsInput.text().split(',')
        try:
            recipe = Recipe(name, description, ingredients, instructions, self.currentSaveFolder)
            recipe.saveRecipe()
            print(f"Recipe '{name}' saved successfully.")
        except ValueError as e:
            print(f"Error saving recipe: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            self.titleInput.clear()
            self.descriptionInput.clear()
            self.ingredientsInput.clear()
            self.instructionsInput.clear()

    def setRecipeFolder(self):
        new_folder = self.folderInput.text().strip()
        if not new_folder:
            print("Folder path cannot be empty.")
            return

        try:
            abs_folder = os.path.abspath(new_folder)
            os.makedirs(abs_folder, exist_ok=True)
            self.currentSaveFolder = abs_folder
            self.currentFolderLabel.setText(f"Current Recipe Folder: {self.currentSaveFolder}")
            print(f"Recipe folder set to: {self.currentSaveFolder}")
        except Exception as e:
            print(f"Failed to set recipe folder: {e}")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
