from flet import AlertDialog, TextButton, RoundedRectangleBorder, MainAxisAlignment, Text

class ConfirmDialog(AlertDialog):
    
    def __init__(self, function, title="", content=""):
        super().__init__()
        self.function = function

        self.modal=True
        self.title=Text(title)
        self.content=Text(content)
        self.actions=[
            TextButton("Não", on_click=self.canceled),
            TextButton(content=Text("Sim", color="red"), on_click=self.confirmed),
        ]
        self.actions_alignment=MainAxisAlignment.END
        self.shape=RoundedRectangleBorder(radius=10)

    def build(self):
        return self
    
    def confirmed(self, e):
        self.open = False
        self.update()
        self.function(self.data)
    
    def canceled(self, e):
        self.open = False
        self.update()
