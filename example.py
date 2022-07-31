from ColorController.ColorController import ColorController

blue = ColorController(name="blue")

blue.show_color()

red = ColorController(name="red")

red.show_color()

purple = red + blue

purple.show_color()