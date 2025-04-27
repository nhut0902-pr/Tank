from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import random
import os

class TankGame(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.high_score = self.load_high_score()
        self.init_game()

    def init_game(self):
        self.clear_widgets()
        self.lives = 3
        self.score = 0
        self.bullets = []
        self.bot_bullets = []
        self.bots = []

        self.player = Label(text='[color=00ff00]▲[/color]', markup=True, font_size=50,
                            size_hint=(None, None), size=(50, 50), pos=(200, 100))
        self.add_widget(self.player)

        self.lbl_lives = Label(text=f'Mạng: {self.lives}', font_size=20, pos_hint={'x':0, 'y':0.9}, size_hint=(.2, .1))
        self.lbl_score = Label(text=f'Điểm: {self.score}', font_size=20, pos_hint={'x':0.4, 'y':0.9}, size_hint=(.3, .1))
        self.lbl_high = Label(text=f'Kỷ lục: {self.high_score}', font_size=20, pos_hint={'x':0.8, 'y':0.9}, size_hint=(.2, .1))
        self.add_widget(self.lbl_lives)
        self.add_widget(self.lbl_score)
        self.add_widget(self.lbl_high)

        # Điều khiển
        self.add_widget(Button(text='↑', size_hint=(.1, .1), pos_hint={'x':.1, 'y':.2},
                               on_press=lambda x: self.move_player(0, 20)))
        self.add_widget(Button(text='↓', size_hint=(.1, .1), pos_hint={'x':.1, 'y':.0},
                               on_press=lambda x: self.move_player(0, -20)))
        self.add_widget(Button(text='←', size_hint=(.1, .1), pos_hint={'x':.0, 'y':.1},
                               on_press=lambda x: self.move_player(-20, 0)))
        self.add_widget(Button(text='→', size_hint=(.1, .1), pos_hint={'x':.2, 'y':.1},
                               on_press=lambda x: self.move_player(20, 0)))
        self.add_widget(Button(text='Bắn', size_hint=(.15, .1), pos_hint={'x':.8, 'y':.1},
                               on_press=self.fire_bullet))

        Clock.schedule_interval(self.spawn_bot, 3)
        Clock.schedule_interval(self.update_game, 1/30)

    def move_player(self, dx, dy):
        x, y = self.player.pos
        self.player.pos = (max(0, min(x + dx, self.width - 50)), max(0, min(y + dy, self.height - 50)))

    def fire_bullet(self, *args):
        x, y = self.player.pos
        bullet = Label(text='[color=ffff00]|[/color]', markup=True, font_size=30, size_hint=(None, None), size=(10, 30), pos=(x + 20, y + 50))
        self.bullets.append(bullet)
        self.add_widget(bullet)

    def spawn_bot(self, dt):
        x = random.randint(0, int(self.width) - 50)
        bot = Label(text='[color=ff0000]▼[/color]', markup=True, font_size=50, size_hint=(None, None), size=(50, 50), pos=(x, self.height - 60))
        self.bots.append(bot)
        self.add_widget(bot)

    def fire_bot_bullet(self, bot):
        x, y = bot.pos
        bullet = Label(text='[color=ff0000]|[/color]', markup=True, font_size=30, size_hint=(None, None), size=(10, 30), pos=(x + 20, y - 20))
        self.bot_bullets.append(bullet)
        self.add_widget(bullet)

    def update_game(self, dt):
        for bullet in self.bullets[:]:
            bullet.y += 10
            for bot in self.bots[:]:
                if bullet.collide_widget(bot):
                    self.remove_widget(bot)
                    self.bots.remove(bot)
                    self.remove_widget(bullet)
                    self.bullets.remove(bullet)
                    self.score += 1
                    self.lbl_score.text = f'Điểm: {self.score}'
                    break
            if bullet.y > self.height:
                self.remove_widget(bullet)
                self.bullets.remove(bullet)

        for bot in self.bots:
            bot.y -= 2
            if random.random() < 0.01:
                self.fire_bot_bullet(bot)

        for bullet in self.bot_bullets[:]:
            bullet.y -= 5
            if bullet.collide_widget(self.player):
                self.lives -= 1
                self.lbl_lives.text = f'Mạng: {self.lives}'
                self.remove_widget(bullet)
                self.bot_bullets.remove(bullet)
                if self.lives <= 0:
                    self.end_game()
            elif bullet.y < 0:
                self.remove_widget(bullet)
                self.bot_bullets.remove(bullet)

    def end_game(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score(self.high_score)

        self.clear_widgets()
        self.add_widget(Label(text='[b][color=ff0000]GAME OVER[/color][/b]', markup=True,
                              font_size=60, pos_hint={'center_x': 0.5, 'center_y': 0.6}))

        self.add_widget(Label(text=f'Điểm của bạn: {self.score}', font_size=30,
                              pos_hint={'center_x': 0.5, 'center_y': 0.5}))
        self.add_widget(Label(text=f'Kỷ lục: {self.high_score}', font_size=30,
                              pos_hint={'center_x': 0.5, 'center_y': 0.45}))

        self.add_widget(Button(text='Chơi lại', size_hint=(.3, .1), pos_hint={'center_x': 0.5, 'y': 0.2},
                               on_press=lambda x: self.init_game()))

    def save_high_score(self, score):
        with open("high_score.txt", "w") as f:
            f.write(str(score))

    def load_high_score(self):
        if os.path.exists("high_score.txt"):
            with open("high_score.txt", "r") as f:
                return int(f.read())
        return 0

class TankApp(App):
    def build(self):
        root = FloatLayout()
        start_btn = Button(text='Bắt đầu chơi', size_hint=(.4, .2), pos_hint={'center_x': 0.5, 'center_y': 0.5}, font_size=30)
        root.add_widget(start_btn)

        def start_game(instance):
            root.clear_widgets()
            game = TankGame()
            root.add_widget(game)

        start_btn.bind(on_press=start_game)
        return root

TankApp().run()