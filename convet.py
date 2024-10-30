from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import Color, Line, RoundedRectangle


# Custom TextInput with only bottom border
class BottomBorderTextInput(TextInput):
    def __init__(self, **kwargs):
        super(BottomBorderTextInput, self).__init__(**kwargs)
        with self.canvas.after:
            # Set the color and draw a line at the bottom
            Color(1, 1, 1, 1)  # White color for the bottom border
            self.line = Line(points=[self.x, self.y, self.x + self.width, self.y], width=2)

        # Bind the position and size to update the line dynamically
        self.bind(pos=self.update_line, size=self.update_line)

    def update_line(self, *args):
        # Update the position of the bottom border line when the size or position changes
        self.line.points = [self.x, self.y, self.x + self.width, self.y]


# Custom Button with rounded corners and purple background
class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.rect_color = Color(0.6, 0.3, 0.9, 1)  # Purple color for the button
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])  # Set radius for round edges
            self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class NumberConverterApp(App):
    def build(self):
        # Set app background color (similar to Android's holo_blue_light)
        Window.clearcolor = (0.0, 0.68, 0.93, 1)

        # Create the main layout
        layout = GridLayout(cols=1, padding=20, spacing=10)

        # Title label
        self.title_label = Label(text='Number Converter', font_size=32, color=(1, 1, 1, 1))
        layout.add_widget(self.title_label)

        # Input TextInput with only bottom border
        self.input_number = BottomBorderTextInput(hint_text="Enter number", multiline=False, font_size=24)
        layout.add_widget(self.input_number)

        # Spinner for selecting base (removed 'Select' text)
        self.base_spinner = Spinner(
            text='Decimal',  # Default to 'Decimal'
            values=('Decimal', 'Binary', 'Octal', 'Hexadecimal'),
            font_size=20
        )
        layout.add_widget(self.base_spinner)

        # Rounded purple button for conversion
        convert_button = RoundedButton(text="Convert", font_size=24)
        convert_button.bind(on_press=self.convert_number)
        layout.add_widget(convert_button)

        # Output label to display results
        self.output_label = Label(text='', font_size=24, color=(1, 1, 1, 1))
        layout.add_widget(self.output_label)

        return layout

    def convert_number(self, instance):
        input_value = self.input_number.text
        selected_base = self.base_spinner.text

        if not input_value:
            self.show_popup("Error", "Please enter a number.")

            return

        try:
            # Convert based on selected base
            if selected_base == 'Decimal':
                decimal_value = int(input_value)
            elif selected_base == 'Binary':
                decimal_value = int(input_value, 2)
            elif selected_base == 'Octal':
                decimal_value = int(input_value, 8)
            elif selected_base == 'Hexadecimal':
                decimal_value = int(input_value, 16)
            else:
                raise ValueError("Unknown base")

            # Display the converted values
            self.output_label.text = (
                f"Binary: {bin(decimal_value)[2:]}\n"
                f"Octal: {oct(decimal_value)[2:]}\n"
                f"Hexadecimal: {hex(decimal_value)[2:].upper()}"
            )
        except ValueError:
            self.show_popup("Error", "Invalid input or base. Please try again.")

    def show_popup(self, title, message):
        # Show an error popup
        popup_content = GridLayout(cols=1, padding=10)
        popup_content.add_widget(Label(text=message, font_size=18))
        close_button = Button(text="Close", size_hint_y=None, height=50)
        popup_content.add_widget(close_button)

        popup = Popup(title=title, content=popup_content, size_hint=(0.8, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == "__main__":
    NumberConverterApp().run()
