from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage

import os
import pandas as pd

MENU_PATH = "imgs/menu"
PRICE_PATH = "price.csv"

price_df = pd.read_csv(PRICE_PATH)
print(price_df)

class MenuItemButton(BoxLayout):
    def __init__(self, name, price, image_path, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.name = name
        self.price = price
        self.image_path = image_path

        self.image = AsyncImage(source=self.image_path, size_hint_x=0.3)
        self.add_widget(self.image)

        self.details = BoxLayout(orientation='vertical', size_hint_x=0.7)
        self.name_label = Button(text=self.name, size_hint_y=0.5, background_color=(1, 1, 1, 0))
        self.price_label = Button(text=f'€{self.price}', size_hint_y=0.5, background_color=(1, 1, 1, 0))
        self.details.add_widget(self.name_label)
        self.details.add_widget(self.price_label)
        self.add_widget(self.details)

class MenuScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        for name, price in zip(price_df['name'], price_df['price']):
            image_path = os.path.join(MENU_PATH, f"{name.lower().replace(' ', '_')}.jpg")
            item_button = MenuItemButton(name, price, image_path)
            self.add_widget(item_button)

class RestaurantApp(App):
    def build(self):
        return MenuScreen()

if __name__ == '__main__':
    RestaurantApp().run()
