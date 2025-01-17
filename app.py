from datetime import datetime
from api import OpenAi
from time import sleep
import threading
from flet import *
from dotenv import load_dotenv
load_dotenv()

bg = '#444654'
fg = '#202123'
side_bar_width = 260


openai = OpenAi(str(datetime.now()))
print(openai.chat)


class Main(UserControl):
    def __init__(self, page: Page,):
        page.padding = 0
        page.title = 'KapsülGPT'
        # COLOR THEME BLUE & DARK BLUE & WHITE
        # page.theme = Theme(color_scheme_seed="black")
        page.update()
        self.blinking = False
        self.chat_response = ''

        self.page = page
        self.prompt = [
            {
                "role": "system",
                'content': 'As a large AI language model. You know almost everything. Your job is to provide solution / suggestion to problems.'
            }
        ]
        self.init()

    def init(self):
        self.chat_gpt_label = Container(
            padding=padding.only(top=120),
            alignment=alignment.center,
            content=Text(
                value='KapsülGPT',
                size=35, weight=FontWeight.BOLD,
            )
        )
        self.cursor = Container(
            width=8, height=20,
            # bgcolor='#3e3f4b',
        )

        self.message_field = TextField(
            border=InputBorder.NONE,
            expand=True,
            multiline=True,
            content_padding=0,
            # max_lines=5,
            # max_length=100,
            # min_lines=5,


        )

        self.content_area = Column(
            auto_scroll=True,
            spacing=30,
            scroll='auto',
            controls=[
                self.chat_gpt_label,
                Row(
                    alignment='center',
                    controls=[
                        Column(
                            controls=[
                                Container(
                                    alignment=alignment.center,
                                    width=250,
                                    content=Column(
                                        horizontal_alignment='center',
                                        controls=[
                                            Icon(icons.BRIGHTNESS_7_OUTLINED),
                                            Text('Hızlı sorular')
                                        ]
                                    )
                                ),
                                Container(
                                    alignment=alignment.center,
                                    width=250,
                                    # height=100,
                                    padding=padding.only(
                                        top=20, bottom=30, left=20, right=20),
                                    border_radius=8,
                                    on_hover=self.hover2,
                                    # bgcolor='#3e3f4b',
                                    content=Text(
                                        'Kapsül Ne Zaman Kuruldu?',
                                        text_align='center',
                                    )
                                ),

                                Container(
                                    alignment=alignment.center,
                                    width=250,
                                    # height=100,
                                    padding=padding.only(
                                        top=20, bottom=30, left=20, right=20),
                                    border_radius=8,
                                    on_hover=self.hover2,
                                    # bgcolor='#3e3f4b',
                                    content=Text(
                                        'Gönüllü başvurularını nereden yapabilirim?',
                                        text_align='center',
                                    )
                                ),

                                Container(
                                    alignment=alignment.center,
                                    width=250,
                                    # height=100,
                                    padding=padding.only(
                                        top=20, bottom=30, left=20, right=20),
                                    border_radius=8,
                                    on_hover=self.hover2,
                                    # bgcolor='#3e3f4b',
                                    content=Text(
                                        'Kapsül Teknoloji Platformunun misyonu nedir?',
                                        text_align='center',
                                    )
                                ),

                            ]
                        )
                    ]
                )



            ]
        )

        self.main_content = Container(
            padding=padding.only(top=20,),
            expand=True,
            # bgcolor=bg,
            content=Column(
                alignment='spaceBetween',
                horizontal_alignment='center',
                controls=[
                    Container(
                        width=1000,
                        expand=True,
                        content=self.content_area


                    ),

                    Container(
                        margin=margin.only(top=30),
                        height=100,
                        content=Column(
                            horizontal_alignment='center',
                            spacing=0,
                            controls=[
                                Card(
                                    elevation=5,
                                    content=Container(
                                        border_radius=10,
                                        # bgcolor='#40414f',
                                        padding=padding.only(
                                            top=5, right=4, left=10, bottom=5),
                                        height=50,
                                        width=1000,
                                        content=Row(
                                            controls=[
                                                self.message_field,
                                                Container(
                                                    on_click=self.send_clicked,
                                                    height=40,
                                                    width=40,
                                                    content=Icon(
                                                        icons.SEND,
                                                    ),
                                                    on_hover=self.hover,
                                                    border_radius=8

                                                )
                                            ]
                                        )
                                    )
                                ),
                                Row(
                                    expand=True,
                                    controls=[
                                        Text(
                                            expand=True,
                                            value='Bu app, kapsül teknoloji platformu için demo olarak geliştirilmiştir.',
                                            text_align='center'
                                        )
                                    ]
                                )
                            ]
                        )


                    ),

                ]
            )


        )

        self.page.add(
            Container(
                expand=True,
                # bgcolor=bg,
                content=Row(
                    spacing=0,
                    controls=[
                        # self.side_bar,
                        self.main_content,
                    ]
                )

            )
        )

    def new_chat_hover(self, e: HoverEvent):
        if e.data == 'true':

            e.control.bgcolor = '#e0e0e0'
        else:
            e.control.bgcolor = None
        e.control.update()

    def hover(self, e):
        if e.data == 'true':
            e.control.bgcolor = '#c0c0c0'
        else:
            e.control.bgcolor = None
        e.control.update()

    def hover2(self, e):
        if e.data == 'true':
            e.control.bgcolor = '#c0c0c0'
        else:
            e.control.bgcolor = '#e0e0e0'
        e.control.update()

    def send_clicked(self, e: TapEvent):
        message = self.message_field.value
        if message != '':
            self.message_field.value = ''
            self.message_field.update()

            if self.chat_gpt_label in self.content_area.controls:
                self.content_area.controls.clear()
                self.content_area.update()

            gpt_message = Row(
                vertical_alignment='center',
                controls=[
                    Container(
                        height=35, width=35,
                        content=Image(
                            src='assets/chatgpt.png',
                            fit=ImageFit.COVER,
                        )

                    ),
                    self.cursor
                ]
            )

            response_label = Text('', expand=True, size=16)
            if self.blinking is False:
                self.blinking = True

                self.content_area.controls.append(
                    Container(

                        # light shadow
                        bgcolor='#FAF7F9',
                        padding=padding.only(
                            top=20, bottom=60, left=20, right=20
                        ),
                        content=Row(
                            controls=[
                                Container(
                                    border_radius=8,
                                    clip_behavior=ClipBehavior.ANTI_ALIAS,
                                    height=35, width=35,
                                    content=Image(
                                        src='assets/user.png',
                                        fit=ImageFit.COVER,
                                    )

                                ),
                                Text(
                                    message,
                                    expand=True,
                                    size=16,
                                    selectable=True
                                )
                            ]
                        )
                    )

                )
                self.content_area.update()

                sleep(.1)

                self.content_area.controls.append(
                    Container(
                        padding=padding.only(
                            top=20, bottom=10, left=20, right=20),

                        content=gpt_message
                    ),
                )
                self.content_area.update()

                t = threading.Thread(target=self.blink)
                t.start()

                chat_response = self.call_chatgpt(message)

                self.blinking = False
                sleep(0.4)
                self.blinking = True
                if self.cursor in gpt_message.controls:
                    gpt_message.controls.remove(self.cursor)
                    gpt_message.update()
                if response_label not in gpt_message.controls:
                    gpt_message.controls.append(response_label)
                    gpt_message.vertical_alignment = 'start'
                    gpt_message.update()
                    for char in chat_response:
                        response_label.value += char
                        response_label.update()
                        sleep(0.02)
                self.blinking = False

    def call_chatgpt(self, text):
        self.prompt.append(
            {
                "role": "user",
                "content": text
            }
        )
        openai.addMessage(text)
        chat_response = openai.getAiResponse()
        self.prompt.append(chat_response)
        return chat_response["content"]

    def blink(self,):
        while True:
            if self.blinking == False:
                break
            if self.cursor.opacity == 100:
                self.cursor.opacity = 0
            else:
                self.cursor.opacity = 100
            self.cursor.update()

            sleep(.4)


app(target=Main, assets_dir='assets')
