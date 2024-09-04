from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage, Image
from kivy.core.text import LabelBase
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
import os
import pandas as pd

LabelBase.register(name='Roboto', fn_regular='./font/msyh.ttc')

MENU_PATH = "imgs/menu"
PRICE_PATH = "price.csv"
APP_IMG_PATH = "imgs/app_img"
bg_img_name = "background.jpg"  # Background image path
cover_img_name = "cover.png"  # App icon image

price_df = pd.read_csv(PRICE_PATH)

# Class to store selected dishes and manage total price
class OrderManager:
    def __init__(self):
        self.selected_items = {}  # Store selected dishes and quantities

    def add_item(self, name, price):
        if name in self.selected_items:
            self.selected_items[name]['quantity'] += 1
        else:
            self.selected_items[name] = {'price': price, 'quantity': 1}

    def remove_item(self, name):
        if name in self.selected_items:
            if self.selected_items[name]['quantity'] > 1:
                self.selected_items[name]['quantity'] -= 1
            else:
                del self.selected_items[name]

    def get_total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.selected_items.values())

    def get_selected_items(self):
        return self.selected_items

# Define a custom button for each menu item
class MenuItemButton(BoxLayout):
    def __init__(self, name, price, image_path, order_manager, update_callback, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.name = name
        self.price = price
        self.image_path = image_path
        self.order_manager = order_manager
        self.update_callback = update_callback

        # Display the image of the dish
        self.image = AsyncImage(source=self.image_path, size_hint_x=0.3)
        self.add_widget(self.image)

        # Details (name, price, quantity controls)
        self.details = BoxLayout(orientation='vertical', size_hint_x=0.5)
        self.name_label = Button(text=self.name, size_hint_y=0.5, background_color=(1, 1, 1, 0), font_name='Roboto', bold=True)
        self.price_label = Button(text=f'€{self.price}', size_hint_y=0.5, background_color=(1, 1, 1, 0), font_name='Roboto', bold=True)
        self.details.add_widget(self.name_label)
        self.details.add_widget(self.price_label)
        self.add_widget(self.details)

        # Quantity buttons (add and remove)
        self.quantity_controls = BoxLayout(orientation='horizontal', size_hint_x=0.2)
        self.add_btn = Button(text='+', on_press=self.add_to_order)
        self.remove_btn = Button(text='-', on_press=self.remove_from_order)
        self.quantity_controls.add_widget(self.add_btn)
        self.quantity_controls.add_widget(self.remove_btn)
        self.add_widget(self.quantity_controls)

    def add_to_order(self, instance):
        self.order_manager.add_item(self.name, self.price)
        self.update_callback()

    def remove_from_order(self, instance):
        self.order_manager.remove_item(self.name)
        self.update_callback()

# The main menu screen layout
class MenuScreen(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.order_manager = OrderManager()

        # Add background image with opacity
        bg_image = Image(source=os.path.join(APP_IMG_PATH, bg_img_name), allow_stretch=True, keep_ratio=False, opacity=0.5)
        self.add_widget(bg_image)

        # Optional: Add a semi-transparent overlay to darken the background further
        overlay = Widget()
        with overlay.canvas:
            Color(0, 0, 0, 0.3)  # Black color with 30% opacity
            self.rect = Rectangle(size=self.size, pos=self.pos)
            overlay.bind(size=self._update_rect, pos=self._update_rect)
        self.add_widget(overlay)

        # Main layout (left side with menu items and right side with selected items)
        main_layout = BoxLayout(orientation='horizontal')

        # Left side: Menu items list
        menu_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)

        for name, price in zip(price_df['name'], price_df['price']):
            image_path = os.path.join(MENU_PATH, f"{name.lower().replace(' ', '_')}.jpg")
            item_button = MenuItemButton(name, price, image_path, self.order_manager, self.update_selected_items)
            menu_layout.add_widget(item_button)

        # Right side: Selected items and total price
        self.selected_items_layout = BoxLayout(orientation='vertical', size_hint_x=0.3)
        self.selected_items_label = Label(text="Selected Items", font_name='Roboto', bold=True)
        self.selected_items_layout.add_widget(self.selected_items_label)

        self.selected_items_box = BoxLayout(orientation='vertical')
        self.selected_items_layout.add_widget(self.selected_items_box)

        self.total_price_label = Label(text="Total: €0", font_name='Roboto', bold=True)
        self.selected_items_layout.add_widget(self.total_price_label)

        # Add both sides to the main layout
        main_layout.add_widget(menu_layout)
        main_layout.add_widget(self.selected_items_layout)
        self.add_widget(main_layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    # Update selected items display and total price
    def update_selected_items(self):
        self.selected_items_box.clear_widgets()  # Clear the previous list

        # Update selected items list
        selected_items = self.order_manager.get_selected_items()
        for name, info in selected_items.items():
            item_label = Label(text=f"{name} x {info['quantity']} - €{info['price'] * info['quantity']:.2f}", font_name='Roboto')
            self.selected_items_box.add_widget(item_label)

        # Update total price
        total_price = self.order_manager.get_total_price()
        self.total_price_label.text = f"Total: €{total_price:.2f}"

# The main app class
class JinshiApp(App):
    def build(self):
        # Set the app icon
        self.icon = os.path.join(APP_IMG_PATH, cover_img_name)
        return MenuScreen()

if __name__ == '__main__':
    JinshiApp().run()
