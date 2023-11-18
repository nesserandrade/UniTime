from ConfirmDialog import ConfirmDialog
from flet import *
import json

class Configuracao(UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route

        #CONTROLES

        self.btn_save_teachers = OutlinedButton(text='Salvar', icon=icons.SAVE_OUTLINED, on_click=self.save_clicked)

        self.btn_novo_professor = IconButton(icon=icons.ADD_OUTLINED, tooltip="Novo Professor(a)", icon_color="primary", icon_size=36, on_click=self.new_professor_clicked)

        self.btn_delete = IconButton(icon=icons.DELETE_OUTLINED, tooltip="Deletar Professores",icon_color='red', on_click=self.delete_clicked)
    
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
            rows=[
                DataRow(on_select_changed=lambda e: self.checked_row(e), selected=False,
                    cells=[
                        DataCell(TextField(hint_text="Escreva o nome do professor(a)", value="Professor")),
                        DataCell(TextField(hint_text="Escreva o nome da disciplina", value="Disciplina")),
                        DataCell(TextField(hint_text="Escreva o número de aulas",value="1")),
                    ],
                ),
                DataRow(on_select_changed=lambda e: self.checked_row(e), selected=False,
                    cells=[
                        DataCell(TextField(hint_text="Escreva o nome do professor(a)", value="Professor")),
                        DataCell(TextField(hint_text="Escreva o nome da disciplina", value="Disciplina")),
                        DataCell(TextField(hint_text="Escreva o número de aulas",value="1")),
                    ],
                ),
            ],
        )

        self.listview_professores = ListView(
                                    expand=True,
                                    controls=[
                                            self.dt_professores,
                                             ]
                                    )
        #DATA

        self.checked_list = []

        #CARDS
    
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
            margin=35,
            content=Column(    
                expand=False,
                spacing=40,
                alignment="start",
                controls=[
                    Row(expand=2,
                        spacing=20,
                        alignment="center",
                        controls=[
                            self.btn_novo_professor,
                            self.btn_delete,]),
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
                            self.btn_save_teachers,
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
        rows_data = [
        [cell.content.value for cell in row.cells] for row in self.dt_professores.rows
        ]

        # Cria um dicionário para armazenar os dados
        data = {
            "rows": rows_data
        }

        # Converte a estrutura serializável para uma string JSON
        json_data = json.dumps(data, indent=2)
        self.route.page.client_storage.set("temp_data", json_data)

    def load_professores(self):
        if self.route.page.client_storage.contains_key("temp_data"):
            json_data = self.route.page.client_storage.get("temp_data")
            data = json.loads(json_data)
            rows = []
            for row_data in data.get("rows", []):
                cells_data = [
                            DataCell(TextField(value=str(JSONvalue))) for JSONvalue in row_data
                ]
                rows.append(DataRow(on_select_changed=lambda e: self.checked_row(e), selected=False,
                    cells=cells_data
                ))

            self.dt_professores.rows.clear()
            self.dt_professores.rows.append(rows)
