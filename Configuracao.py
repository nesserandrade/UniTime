from ConfirmDialog import ConfirmDialog
from flet import *
from Database import Database

class Configuracao(UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        self.database = Database()

        #FUNÇÕES

        def slider_changed(e):
            self.route.page.client_storage.set("temp_aulas_semana", e.control.value)
            self.slider_text.value = f"Número de aulas na semana: {int(e.control.value * 5)}"
            self.update()

        #CONTROLES

        self.slider_text = Text("Número de aulas na semana: ", expand=1, visible=True)

        self.aulas_dia_slider = Slider(expand=2, min=2, max=10, divisions=8, value=2, label="{value}", on_change=slider_changed)

        self.btn_save_teachers = OutlinedButton(text='Salvar', icon=icons.SAVE_OUTLINED, on_click=self.save_clicked)

        self.btn_novo_professor = IconButton(expand=1, icon=icons.ADD_OUTLINED, tooltip="Novo Professor(a)", icon_color="primary", icon_size=36, on_click=self.new_professor_clicked)

        self.btn_delete = IconButton(expand=1, icon=icons.DELETE_OUTLINED, tooltip="Deletar Professores",icon_color='red', on_click=self.delete_clicked)
    
        self.dt_professores = DataTable(     
            width=1000,                                       
            expand=True,
            divider_thickness=0,
            sort_ascending=True,
            show_checkbox_column=True,
            checkbox_horizontal_margin=0,
            heading_row_height=100,
            columns=[
                DataColumn(Text('Professor(a)')), 
                DataColumn(Text('Disciplina')), 
                DataColumn(Text('Número de aulas'), numeric=True),
            ],
            rows=[],
        )

        self.listview_professores = ListView(
                                    expand=True,
                                    controls=[
                                            self.dt_professores,
                                             ]
                                    )
        #DATA

        self.checked_list = []
    
    #FUNÇÕES
        
    def new_professor_clicked(self, e):
        self.dt_professores.rows.append(
            DataRow(on_select_changed=lambda e: self.checked_row(e), selected=False,
                    cells=[
                        DataCell(TextField(hint_text="Escreva o nome do professor(a)", value="Professor")),
                        DataCell(TextField(hint_text="Escreva o nome da disciplina", value="Disciplina")),
                        DataCell(TextField(hint_text="Escreva o número de aulas",value="1")),
                    ],
                ))
        self.dt_professores.update()
        self.route.page.update()

    def initialize(self):
        self.route.menu.nnrail.selected_index = 0
        self.route.menu.update()
        self.update()
        self.route.page.update()
        self.load_professores()

    def build(self):
        self.config_content = Container(
            expand=True,
            margin=10,
            content=Column(    
                expand=False,
                spacing=5,
                alignment="start",
                controls=[
                    Row(expand=1,
                        spacing=5,
                        alignment="center",
                        controls=[
                            Text("Número de aulas por dia:", style=TextThemeStyle.TITLE_MEDIUM),
                            self.aulas_dia_slider,
                            self.slider_text,
                            self.btn_novo_professor,
                            self.btn_delete,]),
                    Row(
                        expand=4,
                        spacing=5,
                        alignment="center",
                        controls=[
                            self.listview_professores
                        ],
                    ),
                    Row(expand=1,
                        spacing=5,
                        alignment="center",
                        controls=[
                            self.btn_save_teachers,
                        ]
                    ),
                ]
            )
        )

        self.content = Row(
            expand=True,
            spacing=5,
            controls=[                
                self.config_content,             
            ]
        )
        return self.content

    def checked_row(self,e):
        if e.data == "true":
            e.control.selected = True
            self.checked_list.append(e.control)
        else:
            e.control.selected = False
            i = e.control
            for i in self.checked_list:
                try:
                    self.checked_list.remove(i)
                except ValueError:
                    pass

        self.route.page.update()

    def delete_clicked(self, e):
        dialog = ConfirmDialog(self.delete_teachers, "Por favor, confirme:", "Tem certeza que deseja excluir os professores?")
        dialog.data = self.checked_list
        self.route.page.dialog = dialog
        dialog.open = True
        self.route.page.update()

    def delete_teachers(self, e):
        for i in self.checked_list:
            try:
                self.dt_professores.rows.remove(i)
            except ValueError:
                pass
        self.checked_list.clear()
        self.route.page.update()
        self.dt_professores.update()

    def save_clicked(self, e):
        # Conectar ao banco de dados SQLite (cria o arquivo do banco se não existir)
        self.database.iniciar()

        # Inserir dados na tabela
        self.database.delete_all_professores()
        for row in self.dt_professores.rows:
            nome_professor = row.cells[0].content.value
            disciplina = row.cells[1].content.value
            num_aulas = int(row.cells[2].content.value)

            self.database.inserir_professores(nome_professor,disciplina,num_aulas)

        self.database.disconnect()
        self.route.page.update()
        self.dt_professores.update()

    def load_professores(self):
        self.database.iniciar()
        professores = self.database.get_all_professores()

        self.dt_professores.rows.clear()
        for professor in professores:
            row = DataRow(on_select_changed=lambda e: self.checked_row(e), selected=False,
                cells=[
                    DataCell(TextField(value=professor[1], hint_text="Escreva o nome do professor(a)")),  # NomeProfessor
                    DataCell(TextField(value=professor[2], hint_text="Escreva o nome da disciplina")),  # Disciplina
                    DataCell(TextField(value=str(professor[3]), hint_text="Escreva o número de aulas")),  # NumAulas
                ],
            )
            self.dt_professores.rows.append(row)

        self.database.disconnect()

        self.dt_professores.update()
