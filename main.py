import random
import string
import json
import os
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.popup import Popup 
from kivymd.uix.label import MDLabel
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogHeadlineText, MDDialogSupportingText
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.tooltip import MDTooltip
from kivymd.uix.widget import MDWidget
#from kivy.core.text import LabelBase
from kivy.properties import StringProperty
from kivy.core.window import Window
from all_word_lists import *

Window.softinput_mode = "below_target"

#LabelBase.register(name='Chiller', 
#                   fn_regular=os.path.join(os.getcwd(), 'fonts/CHILLER.ttf'))


class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        self.checks = []
        self.password = StringProperty()
        self.strength = StringProperty()
        self.dialog = None

    def info_dialog(self):
        ok_btn = MDButton(MDButtonText(text="OK", halign='center', font_style='Title'),
                    on_release=lambda x: self.dialog.dismiss())
        self.dialog = MDDialog(
            MDDialogHeadlineText(text="About MadPass"),
            MDDialogSupportingText(text='''MadPass is a password generator that provides a variety of options to create strong and unique passwords.\n
            Choose the length of the password and character types to include or exclude.\nUse the 'Copy' icon button to copy the generated password to your clipboard. \n\n
            Click on the [b][i]purple right arrow[/b][/i] for additional customization options. \n\n
            [b]Note:[/b] The password strength indicator is based on the length and character types of the generated password. It is for informational purposes ONLY.\n\n'''),
            MDDialogButtonContainer(
                MDWidget(),
                ok_btn,
                MDWidget(),
                spacing=10
            )
        )
        self.dialog.open()

    def copied(self):
        self.ids.copy_btn.text_color = (0, 1, 0, 1)

    def pw_strength(self, pw):
        lower = sum(1 for c in pw if c in string.ascii_lowercase)
        upper = sum(1 for c in pw if c in string.ascii_uppercase)
        digit = sum(1 for c in pw if c in string.digits)
        special = sum(1 for c in pw if c in string.punctuation)
        if len(pw) > 15:
            if lower > 2 and upper > 2 and digit > 0 and special > 0:
                    self.ids.strength.text = "[color=#02eb39]Strong[/color]"
                    self.ids.progress.value = 100
                    self.ids.progress.indicator_color = (0, 1, 0, 1)
            else:
                self.ids.strength.text = "[color=#ed9a1c]Moderate[/color]"
                self.ids.progress.value = 50
                self.ids.progress.indicator_color = (1, 1, 0, 1)
        elif len(pw) < 10:
            self.ids.strength.text = "[color=#d41204]Weak[/color]"
            self.ids.progress.value = 25
            self.ids.progress.indicator_color = (1, 0, 0, 1)
        else:
            self.ids.strength.text = "[color=#ed9a1c]Moderate[/color]"
            self.ids.progress.value = 50
            self.ids.progress.indicator_color = (1, 1, 0, 1)

    def generate_password(self, pw_len):
        self.ids.copy_btn.text_color = (1, 1, 1, 1)
        try:
            elements = string.ascii_letters + string.digits + string.punctuation
            self.password.text = ''.join(random.sample(elements, self.pw_len.value))
        except ValueError:
            elements = string.ascii_letters + string.digits + string.punctuation
        if len(self.checks) == 0:
            self.password.text = ''.join(random.choices(elements, k=self.pw_len.value))
        else:
            elements = self.get_advanced_options(self.checks, elements, self.pw_len.value)
            self.password.text = ''.join(random.choices(elements, k=self.pw_len.value))
        self.pw_strength(self.password.text)
        
    def get_checks(self, instance, value, opts):
        if not value:
            self.checks.append(opts)
        else:
            self.checks.remove(opts)
        return set(self.checks)    

    def get_advanced_options(self, chk_opts, elems, pw_len):
        if len(chk_opts) == 1:
            if 'upper' in chk_opts:
                elems = [element.lower() if isinstance(element, str) else element for element in elems]
            elif 'lower' in self.checks:
                elems = [element.upper() if isinstance(element, str) else element for element in elems]
            elif 'digits' in self.checks:
                elems = [element.replace(element, random.choice(string.ascii_letters)[0]) if element.isdigit() else element for element in elems]
            elif 'special' in self.checks:
                elems = [element.replace(element, random.choice(string.digits)[0]) if not element.isalnum() else element for element in elems]
        elif len(chk_opts)==2:
            if 'upper' in chk_opts and 'lower' in chk_opts:
                elems = [element.replace(element, random.choice(string.digits)[0]) if element.isalpha() else element for element in elems]
            elif 'digits' in chk_opts and 'lower' in chk_opts:
                elems = [element.replace(element, random.choice(string.punctuation)[0]) if element.isdigit() else element for element in elems]
                elems = [element.upper() if isinstance(element, str) else element for element in elems]
            elif 'digits' in chk_opts and 'upper' in chk_opts:
                elems = [element.replace(element, random.choice(string.punctuation)[0]) if element.isdigit() else element for element in elems]
                elems = [element.lower() if isinstance(element, str) else element for element in elems]
            elif 'special' in chk_opts and 'digits' in chk_opts:
                elems = [element.replace(element, random.choice(string.digits)[0]) if not element.isalpha() else element for element in elems]
            elif 'special' in chk_opts and 'lower' in chk_opts:
                elems = [element.replace(element, random.choice(string.digits)[0]) if not element.isalnum() else element for element in elems]
                elems = [element.upper() if isinstance(element, str) else element for element in elems]
            elif 'special' in chk_opts and 'upper' in chk_opts:
                elems = [element.replace(element, random.choice(string.digits)[0]) if not element.isalnum() else element for element in elems]
                elems = [element.lower() if isinstance(element, str) else element for element in elems]
        elif len(chk_opts)==3:
            if 'upper' in chk_opts and 'lower' in chk_opts and 'digits' in chk_opts:
                elems = random.choices(string.punctuation, k=pw_len)
            elif 'upper' in chk_opts and 'lower' in chk_opts and 'special' in chk_opts:
                elems = random.choices(string.digits, k=pw_len)
            elif 'digits' in chk_opts and 'lower' in chk_opts and 'special' in chk_opts:
                elems = random.choices(string.ascii_uppercase, k=pw_len)
            elif 'upper' in chk_opts and 'digits' in chk_opts and 'special' in chk_opts:
                elems = random.choices(string.ascii_lowercase, k=pw_len)
        elif len(chk_opts)==4:
            err_btn = MDButton(MDButtonText(text="My bad", halign='center', font_style='Body'))
            err_btn.bind(on_release=lambda x: self.err.dismiss())
            self.err=MDDialog(
                MDDialogHeadlineText(text="Error"),
                MDDialogSupportingText(text="Please select at least one option.", font_style='Title'),
                MDDialogButtonContainer(
                    err_btn
            )
            )
            self.err.open()
        return elems


class CustomScreen(MDScreen):
    def __init__(self, **kwargs):
        super(CustomScreen, self).__init__(**kwargs)
    
        self.categories = []
        self.category_words = []

    def help_dialog(self):
        ok_btn = MDButton(MDButtonText(text="OK", halign='center', font_style='Body'),
                    on_release=lambda x: self.dialog.dismiss())
        self.dialog = MDDialog(
            MDDialogHeadlineText(text="Customization Options"),
            MDDialogSupportingText(text='''Each option in the drop down menu offers a different way to generate words and characters for a unique password.\n
            Descriptions below: \n 
            - [b]Prompts[/b] - Provides MadLibs style prompts and generates a password using your response.\n
            - [b]Random words[/b] - Generates a password using random words and dividers.\n
            - [b]Word categories[/b] - Generates a password using words from specific categories of your choosing. You can choose up to 4 categories but the generator will always provide 4 words regardless of the number of categories selected\n'''),
            MDDialogButtonContainer(
                MDWidget(),
                ok_btn,
                MDWidget(),
                spacing=10
            )
        )
        self.dialog.open()

    def copied2(self):
        self.ids.mad_copy_btn.text_color = (0, 1, 0, 1)

    def choose_customization(self, value):
        if value:
            self.ids.choice.text = f'Generate using {value}' 
            self.ids.btn.md_bg_color = "#008a15"
            self.ids.btn.disabled = False
            if value == "word categories":
                self.ids.cat_layout.opacity = 1
            elif value != "word categories":
                self.ids.cat_layout.opacity = 0

    def custom_pw(self, min = None, max = None):
        self.ids.mad_copy_btn.text_color = (1, 1, 1, 1)
        if "random words" in self.ids.choice.text:
            words = random.choices(word_list, k=3)
            self.madlibspassword.text = ''.join(words[0] + str(random.choice(dividers)) + words[1] + str(random.choice(dividers)) + words[2] + 
                                    ''.join(random.choices(string.digits, k=random.sample(range(10), 1)[0])))
        elif "prompts" in self.ids.choice.text:
            pass
        elif "word categories" in self.ids.choice.text:
            if len(self.categories) > 4:
                err_btn = MDButton(MDButtonText(text="If you insist", halign='center', font_style='Body'))
                err_btn.bind(on_release=lambda x: self.err.dismiss())
                self.err=MDDialog(
                    MDDialogHeadlineText(text="Error"),
                    MDDialogSupportingText(text="Please limit selections to 4.", font_style='Title'),
                    MDDialogButtonContainer(
                        err_btn
                )
                )
                self.err.open()
            elif len(self.categories) > 0 and len(self.categories) < 5:
                self.category_words = self.get_category_words()
                self.madlibspassword.text = ''.join(self.category_words[0] + str(random.choice(dividers)) + self.category_words[1] + str(random.choice(dividers)) + self.category_words[2] + 
                                    str(random.choice(dividers)) + self.category_words[3] +''.join(random.choices(string.digits, k=random.sample(range(10), 1)[0])))
            else:
                err_btn = MDButton(MDButtonText(text="My bad", halign='center', font_style='Body'))
                err_btn.bind(on_release=lambda x: self.err.dismiss())
                self.err=MDDialog(
                    MDDialogHeadlineText(text="Error"),
                    MDDialogSupportingText(text="Please select at least one option.", font_style='Title'),
                    MDDialogButtonContainer(
                        err_btn
                )
                )
                self.err.open()

    def get_checks(self, instance, value, opts):
        if value:
            self.categories.append(opts)
        else:
            self.categories.remove(opts)
        return set(self.categories)  

    def get_category_words(self):
        #find the correct list based on the category selected
            # Map categories to their respective word lists
        category_map = {
            'adj': adjectives,
            'noun': word_list,
            'animal': animals,
            'science': science,
            'verb': verbs,
            'color': colors
        }

    # Ensure categories exist in the map
        valid_categories = [category_map[cat] for cat in self.categories if cat in category_map]

    # Distribute words evenly across selected categories
        if valid_categories:
            words_per_category = 4 // len(valid_categories)
            self.category_words = [
                word for category in valid_categories
                for word in random.choices(category, k=words_per_category)
            ]

        # Handle any remaining words if 4 is not divisible by the number of categories
        remaining_words = 4 - len(self.category_words)
        if remaining_words > 0:
            self.category_words += random.choices(valid_categories[0], k=remaining_words)

        return random.sample(self.category_words, k=len(self.category_words))


class PromptsScreen(MDScreen):
    def __init__(self, **kwargs):
        super(PromptsScreen, self).__init__(**kwargs)

    def shuffle_prompts(self, *args, **kwargs):
        prompt_opts = random.choices(prompt_list, k=3)
        self.prompt1.text = f'[b]1. {str(prompt_opts[0])}\n\n2. {str(prompt_opts[1])}\n\n3. {str(prompt_opts[2])}[/b]'
        return self.prompt1.text

    def prompts_pw(self, input):
        custom_screen = MobileApp.get_running_app().root.get_screen(name='custom')
        elems = random.sample(input.text.split(), k=len(input.text.split()))
        custom_screen.ids.madlibspassword.text = ''.join(elems) + str(random.choice(dividers)) + ''.join(random.choices(string.digits, k=random.sample(range(10), 1)[0]))
    

screen_helper = '''
MDScreenManager:
    id: screen_manager

    MainScreen: 
        name: "main"
    CustomScreen: 
        name: "custom"
    PromptsScreen: 
        name: "prompts"
'''

class MobileApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.title = "MadPass Better Passwords"
        self.theme_cls.theme_style = "Dark"
        screen = Builder.load_string(screen_helper)
        return screen
    


if __name__ == '__main__':
    MobileApp().run()