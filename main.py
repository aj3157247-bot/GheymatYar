import os
import json
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label


# =========================================================
# Persian RTL
# =========================================================

try:
    import arabic_reshaper
    from bidi.algorithm import get_display

    def fa(text):
        if not text:
            return ""
        try:
            return get_display(arabic_reshaper.reshape(str(text)))
        except Exception:
            return str(text)

except Exception:

    def fa(text):
        return str(text)


# =========================================================
# Paths
# =========================================================

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(APP_DIR, "gheymatyar_data.json")

FONT_FILE = os.path.join(APP_DIR, "assets", "Vazirmatn-Regular.ttf")

if os.path.exists(FONT_FILE):
    LabelBase.register(
        name="Vazirmatn",
        fn_regular=FONT_FILE
    )
    FONT = "Vazirmatn"
else:
    FONT = "Roboto"


# =========================================================
# Storage
# =========================================================

def load_data():
    default = {
        "products": [],
        "shopping_list": []
    }

    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, dict):
                data.setdefault("products", [])
                data.setdefault("shopping_list", [])
                return data
    except Exception:
        pass

    return default


def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=2
            )
        return True
    except Exception:
        return False


# =========================================================
# Home Screen
# =========================================================

class HomeScreen(Screen):

    def on_enter(self):
        self.update_stats()

    def update_stats(self):
        app = App.get_running_app()

        products = app.data["products"]
        shopping = app.data["shopping_list"]

        self.ids.product_count.text = fa(
            f"{len(products)} کالا"
        )

        self.ids.shopping_count.text = fa(
            f"{len(shopping)} مورد"
        )


# =========================================================
# Add Product Screen
# =========================================================

class AddProductScreen(Screen):

    def clear_fields(self):
        self.ids.product_name.text = ""
        self.ids.product_price.text = ""
        self.ids.product_unit.text = ""

    def add_product(self):

        name = self.ids.product_name.text.strip()
        price = self.ids.product_price.text.strip()
        unit = self.ids.product_unit.text.strip()

        if not name:
            self.show_message("لطفاً نام کالا را وارد کنید.")
            return

        if not price:
            self.show_message("لطفاً قیمت کالا را وارد کنید.")
            return

        try:
            price_number = float(
                price.replace(",", "").replace("٬", "")
            )
        except Exception:
            self.show_message("قیمت واردشده صحیح نیست.")
            return

        if not unit:
            unit = "عدد"

        app = App.get_running_app()

        product = {
            "id": int(datetime.now().timestamp() * 1000),
            "name": name,
            "price": price_number,
            "unit": unit,
            "date": datetime.now().strftime("%Y-%m-%d")
        }

        app.data["products"].append(product)
        app.save()

        self.clear_fields()

        self.show_message("کالا با موفقیت ثبت شد.")

        self.manager.current = "products"

    def show_message(self, message):

        popup = Popup(
            title=fa("پیام"),
            content=Label(
                text=fa(message),
                font_name=FONT,
                font_size=dp(17),
                halign="center"
            ),
            size_hint=(0.85, 0.3)
        )

        popup.open()


# =========================================================
# Products Screen
# =========================================================

class ProductsScreen(Screen):

    def on_enter(self):
        self.refresh()

    def refresh(self):

        container = self.ids.products_container
        container.clear_widgets()

        app = App.get_running_app()

        products = app.data["products"]

        if not products:

            label = Label(
                text=fa("هنوز هیچ کالایی ثبت نشده است."),
                font_name=FONT,
                font_size=dp(18),
                size_hint_y=None,
                height=dp(70)
            )

            container.add_widget(label)
            return

        for product in reversed(products):

            text = (
                f"{product['name']}\n"
                f"{format_price(product['price'])} افغانی / {product['unit']}\n"
                f"{product['date']}"
            )

            from kivy.uix.button import Button

            button = Button(
                text=fa(text),
                font_name=FONT,
                font_size=dp(16),
                size_hint_y=None,
                height=dp(95),
                halign="right",
                valign="middle"
            )

            button.bind(
                on_release=lambda btn, p=product:
                self.add_to_shopping(p)
            )

            container.add_widget(button)

    def add_to_shopping(self, product):

        app = App.get_running_app()

        item = {
            "name": product["name"],
            "price": product["price"],
            "unit": product["unit"]
        }

        app.data["shopping_list"].append(item)
        app.save()

        self.show_message(
            f"{product['name']} به لیست خرید اضافه شد."
        )

    def show_message(self, message):

        popup = Popup(
            title=fa("قیمت‌یار"),
            content=Label(
                text=fa(message),
                font_name=FONT,
                font_size=dp(17)
            ),
            size_hint=(0.85, 0.3)
        )

        popup.open()


# =========================================================
# Shopping Screen
# =========================================================

class ShoppingScreen(Screen):

    def on_enter(self):
        self.refresh()

    def refresh(self):

        container = self.ids.shopping_container
        container.clear_widgets()

        app = App.get_running_app()

        items = app.data["shopping_list"]

        if not items:

            label = Label(
                text=fa("لیست خرید شما خالی است."),
                font_name=FONT,
                font_size=dp(18),
                size_hint_y=None,
                height=dp(70)
            )

            container.add_widget(label)
            return

        total = 0

        for item in items:

            price = float(item.get("price", 0))
            total += price

            from kivy.uix.button import Button

            button = Button(
                text=fa(
                    f"{item['name']}   "
                    f"{format_price(price)} افغانی"
                ),
                font_name=FONT,
                font_size=dp(16),
                size_hint_y=None,
                height=dp(70),
                halign="right"
            )

            container.add_widget(button)

        total_label = Label(
            text=fa(
                f"مجموع تقریبی: {format_price(total)} افغانی"
            ),
            font_name=FONT,
            font_size=dp(20),
            size_hint_y=None,
            height=dp(70)
        )

        container.add_widget(total_label)


# =========================================================
# About Screen
# =========================================================

class AboutScreen(Screen):
    pass


# =========================================================
# Number Formatting
# =========================================================

def format_price(value):

    try:
        value = float(value)

        if value.is_integer():
            return f"{int(value):,}"

        return f"{value:,.2f}"

    except Exception:
        return str(value)


# =========================================================
# KV
# =========================================================

KV = r'''
#:import dp kivy.metrics.dp

<MainButton@Button>:
    font_name: app.font_name
    font_size: dp(18)
    size_hint_y: None
    height: dp(58)
    background_normal: ""
    background_color: .12, .42, .78, 1
    color: 1, 1, 1, 1

<TitleLabel@Label>:
    font_name: app.font_name
    font_size: dp(25)
    bold: True
    color: .10, .20, .30, 1

<HomeScreen>:

    BoxLayout:
        orientation: "vertical"
        padding: dp(18)
        spacing: dp(12)

        Label:
            text: app.fa("قیمت‌یار")
            font_name: app.font_name
            font_size: dp(30)
            bold: True
            size_hint_y: None
            height: dp(65)

        Label:
            text: app.fa("دستیار هوشمند خرید و قیمت")
            font_name: app.font_name
            font_size: dp(17)
            size_hint_y: None
            height: dp(40)

        Widget:

        MainButton:
            text: app.fa("➕ افزودن کالا")
            on_release:
                root.manager.current = "add"

        MainButton:
            text: app.fa("📦 کالاهای من")
            on_release:
                root.manager.current = "products"

        MainButton:
            text: app.fa("🛒 لیست خرید")
            on_release:
                root.manager.current = "shopping"

        MainButton:
            text: app.fa("ℹ️ درباره قیمت‌یار")
            on_release:
                root.manager.current = "about"

        Widget:

        Label:
            id: product_count
            text: app.fa("۰ کالا")
            font_name: app.font_name
            font_size: dp(16)
            size_hint_y: None
            height: dp(35)

        Label:
            id: shopping_count
            text: app.fa("۰ مورد")
            font_name: app.font_name
            font_size: dp(16)
            size_hint_y: None
            height: dp(35)

<AddProductScreen>:

    BoxLayout:
        orientation: "vertical"
        padding: dp(18)
        spacing: dp(12)

        Label:
            text: app.fa("افزودن کالا")
            font_name: app.font_name
            font_size: dp(27)
            bold: True
            size_hint_y: None
            height: dp(60)

        TextInput:
            id: product_name
            hint_text: app.fa("نام کالا")
            font_name: app.font_name
            font_size: dp(18)
            multiline: False
            halign: "right"
            size_hint_y: None
            height: dp(58)

        TextInput:
            id: product_price
            hint_text: app.fa("قیمت به افغانی")
            font_name: app.font_name
            font_size: dp(18)
            multiline: False
            input_filter: "float"
            halign: "right"
            size_hint_y: None
            height: dp(58)

        TextInput:
            id: product_unit
            hint_text: app.fa("واحد - مثلاً کیلو، عدد، بسته")
            font_name: app.font_name
            font_size: dp(18)
            multiline: False
            halign: "right"
            size_hint_y: None
            height: dp(58)

        Widget:

        MainButton:
            text: app.fa("💾 ذخیره کالا")
            on_release: root.add_product()

        MainButton:
            text: app.fa("↩ بازگشت")
            on_release: root.manager.current = "home"

<ProductsScreen>:

    BoxLayout:
        orientation: "vertical"
        padding: dp(12)
        spacing: dp(10)

        Label:
            text: app.fa("📦 کالاهای من")
            font_name: app.font_name
            font_size: dp(27)
            bold: True
            size_hint_y: None
            height: dp(60)

        ScrollView:

            GridLayout:
                id: products_container
                cols: 1
                spacing: dp(8)
                size_hint_y: None
                padding: dp(5)
                height: self.minimum_height

        MainButton:
            text: app.fa("↩ بازگشت")
            on_release: root.manager.current = "home"

<ShoppingScreen>:

    BoxLayout:
        orientation: "vertical"
        padding: dp(12)
        spacing: dp(10)

        Label:
            text: app.fa("🛒 لیست خرید")
            font_name: app.font_name
            font_size: dp(27)
            bold: True
            size_hint_y: None
            height: dp(60)

        ScrollView:

            GridLayout:
                id: shopping_container
                cols: 1
                spacing: dp(8)
                size_hint_y: None
                padding: dp(5)
                height: self.minimum_height

        MainButton:
            text: app.fa("↩ بازگشت")
            on_release: root.manager.current = "home"

<AboutScreen>:

    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(15)

        Label:
            text: app.fa("درباره قیمت‌یار")
            font_name: app.font_name
            font_size: dp(28)
            bold: True
            size_hint_y: None
            height: dp(60)

        Label:
            text: app.fa("قیمت‌یار یک دستیار ساده برای ثبت و مدیریت قیمت کالاها و لیست خرید است.")
            font_name: app.font_name
            font_size: dp(17)
            halign: "center"
            valign: "middle"

        Label:
            text: app.fa("نسخه 1.0")
            font_name: app.font_name
            font_size: dp(16)
            size_hint_y: None
            height: dp(45)

        Widget:

        MainButton:
            text: app.fa("↩ بازگشت")
            on_release: root.manager.current = "home"
'''


# =========================================================
# App
# =========================================================

class GheymatYarApp(App):

    def build(self):

        self.title = "قیمت‌یار"

        self.font_name = FONT

        self.data = load_data()

        Builder.load_string(KV)

        manager = ScreenManager()

        manager.add_widget(
            HomeScreen(
                name="home"
            )
        )

        manager.add_widget(
            AddProductScreen(
                name="add"
            )
        )

        manager.add_widget(
            ProductsScreen(
                name="products"
            )
        )

        manager.add_widget(
            ShoppingScreen(
                name="shopping"
            )
        )

        manager.add_widget(
            AboutScreen(
                name="about"
            )
        )

        return manager

    def save(self):
        save_data(self.data)

    def fa(self, text):
        return fa(text)


if __name__ == "__main__":
    GheymatYarApp().run()
