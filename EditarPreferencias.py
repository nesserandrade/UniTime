from flet import *

class EditarPreferencias(UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route

        #CONTROLES

        self.btn_calc = OutlinedButton(text='Calcular', icon=icons.CALCULATE_OUTLINED, on_click=self.calc_clicked)
    
        self.dt_horarios = DataTable(     
            width=1000,                                       
            expand=True,
            divider_thickness=0,
            sort_ascending=True,
            show_checkbox_column=True,
            checkbox_horizontal_margin=0,
            heading_row_height=100,
            columns=[
                DataColumn(Text('Horários')), 
                DataColumn(Text('Segunda-feira')),
                DataColumn(Text('Terça-feira')), 
                DataColumn(Text('Quarta-feira')), 
                DataColumn(Text('Quinta-feira')), 
                DataColumn(Text('Sexta-feira')), 
            ],
        )

        self.listview_horarios = ListView(
                                    expand=True,
                                    controls=[
                                            self.dt_horarios,
                                             ]
                                    )
        #DATA

        #CARDS
    
    #FUNÇÕES

    def initialize(self):
        self.route.menu.nnrail.selected_index = 1
        self.route.menu.update()
        self.update()
        self.route.page.update()
        self.load_horarios()

    def build(self):
        self.config_content = Container(
            expand=True,
            margin=35,
            content=Column(    
                expand=False,
                spacing=40,
                alignment="start",
                controls=[
                    Row(
                        expand=4,
                        spacing=20,
                        alignment="center",
                        controls=[
                            self.listview_professores
                        ],
                    ),
                    Row(expand=2,
                        spacing=20,
                        alignment="center",
                        controls=[
                            self.btn_calc,
                        ]
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

    def calc_clicked(self, e):
        raise NotImplementedError

    def load_horarios(self):
        raise NotImplementedError