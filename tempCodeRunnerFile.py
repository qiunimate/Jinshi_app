from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage, Image
from kivy.core.text import LabelBase
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

import os
import pandas as pd

LabelBase.register(name='Roboto', fn_regular='./font/msyh.ttc')

MENU_PATH = "imgs/menu"
PRICE_PATH = "price.csv"
APP_IMG_PATH = "imgs/app_img"
bg_img_name = "background.jpg"  # Background image path
cover_img_name = "cover"

price_df = pd.read_csv(PRICE_PATH)

class MenuItemButton(BoxLayout):
    def __init__(self, name, price, image_path, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.name = name
        self.price = price
        self.image_path = image_path

        self.image = AsyncImage(source=self.image_path, size_hint_x=0.3)
        self.add_widget(self.image)

        self.details = BoxLayout(orientation='vertical', size_hint_x=0.7)
        self.name_label = Button(text=self.name, size_hint_y=0.5, background_color=(1, 1, 1, 0), font_name='Roboto', bold=True)
        self.price_label = Button(text=f'€{self.price}', size_hint_y=0.5, background_color=(1, 1, 1, 0), font_name='Roboto', bold=True)
        self.details.add_widget(self.name_label)
        self.details.add_widget(self.price_label)
        self.add_widget(self.details)


class MenuScreen(RelativeLayout):  # Use RelativeLayout for layered widgets
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Add background image with opacity
        bg_image = Image(source=os.path.join(APP_IMG_PATH, bg_img_name), allow_stretch=True, keep_ratio=False, opacity=0.5)
        self.add_widget(bg_image)

        # Optional: Add a semi-transparent overlay to darken the background further
        overlay = Widget()
        with overlay.canvas:
            Color(0, 0, 0, 0.3)  # Black color with 40% opacity
            self.rect = Rectangle(size=self.size, pos=self.pos)
            overlay.bind(size=self._update_rect, pos=self._update_rect)
        self.add_widget(overlay)

        # Create BoxLayout for menu items
        menu_layout = BoxLayout(orientation='vertical')

        for name, price in zip(price_df['name'], price_df['price']):
            image_path = os.path.join(MENU_PATH, f"{name.lower().replace(' ', '_')}.jpg")
            item_button = MenuItemButton(name, price, image_path)
            menu_layout.add_widget(item_button)

        # Add menu items layout on top of the background and overlay
        self.add_widget(menu_layout)

    # Helper method to update the rectangle size with window resizing
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
class JinshiApp(App):
    def build(self):
        return MenuScreen()

if __name__ == '__main__':
    JinshiApp().run()
