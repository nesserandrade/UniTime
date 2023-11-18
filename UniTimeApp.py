from flet import Page, Container, Row, VerticalDivider, FilePicker

from Configuracao import Configuracao
from SideMenu import SideMenu
from EditarPreferencias import EditarPreferencias
from Horarios import Horarios

class UniTimeApp:
    def __init__(self, page: Page):
        self.page = page
        
        # Creates the side menu
        self.menu = SideMenu(self)
    
        self.config = Configuracao(self)
        self.edit = EditarPreferencias(self)
        self.horarios = Horarios(self)

        self.save_file_dialog = FilePicker()

        self.page.overlay.extend([self.save_file_dialog])

        self.routes = {
            "/": self.config,
            "/editar": self.edit,
            "/horarios": self.horarios,
        }
        
        self.calls = {
            "/": self.config.initialize,
            "/editar": self.edit.initialize,
            "/horarios": self.horarios.initialize,
        }

        self.container = Container(expand=True, content=self.routes["/"])
        self.body = Row(
            expand=True,
            alignment="start",
            controls=[
                self.menu,
                VerticalDivider(width=1),
                self.container,
            ]
        )

    def route_change(self, e):

        self.container.content = self.routes[e.route] 
        self.page.update()

        self.calls[e.route]()
        
        self.page.update()
