from flet import *

class Horarios(UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route

        def slider_changed(e):
            self.slider_text.value = f"Slider changed to {e.control.value}"

        #CONTROLS

        #TEXT
        self.slider_text = Text()

        self.professores_slider = Slider(min=0, max=100, divisions=10, label="{value}%", on_change=slider_changed)

        #CARDS
        self.slider_card = Card(
            expand=5,
            surface_tint_color=colors.SURFACE_VARIANT,
            elevation=10.0,
            content = Container(
                padding=20,
                ink=True,
                content=Column(
                    spacing=15,
                    horizontal_alignment='center',
                    alignment='center',
                    controls=[
                        Text("Slider with 'on_change' event:", style=TextThemeStyle.TITLE_MEDIUM),
                        self.professores_slider,
                    ]
                )
            )
        )

    def initialize(self):
        print("Initializing Home Page")

        self.route.menu.nnrail.selected_index = 2
        self.route.menu.update()

    def build(self):
        self.config_content = Container(
            expand=True,
            margin=35,
            content=Column(    
                expand=True,
                spacing=40,                                                            
                controls=[
                    Row(
                        expand=4,
                        spacing=40,
                        controls=[
                            self.slider_card,
                        ],
                    ),
                ]
            )
        )

        self.content = Row(
            expand=True,
            spacing=10,
            controls=[                
                self.config_content,             
            ]
        )
        return self.content     