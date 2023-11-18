from flet import (UserControl, Container, IconButton, icons, NavigationRail, NavigationRailLabelType,
                  NavigationRailDestination, Icon, padding, border_radius, Text)

class SideMenu(UserControl):
    ext = False
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.cont = Container(            
            padding=padding.all(10),        
            border_radius=border_radius.all(5),
            visible=True,
        )        
        self.nnrail = NavigationRail(
            extended=self.ext,
            label_type=NavigationRailLabelType.NONE,
            min_width=56,                
            min_extended_width=160, 
            bgcolor='transparent',
            leading=IconButton(icon=icons.SWAP_HORIZ_ROUNDED, icon_size=40, tooltip="Mostrar/Ocultar Opções", on_click=self.menu_clicked),
            destinations=[
                NavigationRailDestination(
                icon=icons.SETTINGS, label_content=Text("Configuração")
            ),
                NavigationRailDestination(
                icon_content=Icon(icons.EDIT_CALENDAR_OUTLINED),
                selected_icon_content=Icon(icons.EDIT_CALENDAR),
                label="Calcular",
            ),
                NavigationRailDestination(
                icon=icons.PERM_CONTACT_CALENDAR_OUTLINED, selected_icon=icons.PERM_CONTACT_CALENDAR, label="Horários"
            ),
            ],
            on_change=self.nav_clicked,
        )  
        self.cont.content=self.nnrail

    def build(self):     
        return self.cont

    def menu_clicked(self, e):
        self.nnrail.extended = not self.nnrail.extended        
        self.ext = self.nnrail.extended
        self.update()

    def nav_clicked(self, e):
        if e.control.selected_index == 0:            
            self.page.go("/")
            self.route.page.title='UniTime - Configuração'
            self.route.page.update()
            self.update()
            return
        elif e.control.selected_index == 1:
            self.page.go("/editar")
            self.route.page.title='UniTime - Calcular'
            self.route.page.update()
            self.update()
            return
        elif e.control.selected_index == 2:            
            self.page.go("/horarios")
            self.route.page.title='UniTime - Horários'
            self.route.page.update()
            self.update()
            return

