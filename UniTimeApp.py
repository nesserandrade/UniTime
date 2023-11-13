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
    
        """
        creates instances of views and passes the class itself as a parameter
        for all of them, facilitating communication between all classes
        """
        self.config = Configuracao(self)
        self.edit = EditarPreferencias(self)
        self.horarios = Horarios(self)

        # Creates instances of dialogs
        self.save_file_dialog = FilePicker()
        # hide all dialogs in overlay
        self.page.overlay.extend([self.save_file_dialog])

        # Creates dict of routes:
        self.routes = {
            "/": self.config,
            "/editar": self.edit,
            "/horarios": self.horarios,
        }
        
        # Creates dict of method to initialize the Views:
        self.calls = {
            "/": self.config.initialize,
            "/editar": self.edit.initialize,
            "/horarios": self.horarios.initialize,
        }

        # App's body:
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
        # Change View:
        self.container.content = self.routes[e.route] 
        #self.body.update()
        self.page.update()

        # Initialize the View
        self.calls[e.route]()
        
        self.page.update()
