from flet import Page, app, Theme, ThemeMode, colors

from UniTimeApp import UniTimeApp

def main(page: Page):
    page.title='UniTime'
    page.window_min_height = 700
    page.window_min_width = 1360

    page.theme_mode=ThemeMode.LIGHT
    page.theme = Theme(color_scheme_seed=colors.BLUE_300)

    unitime_app = UniTimeApp(page)
    page.on_route_change = unitime_app.route_change    

    page.add(
        unitime_app.body
    )
    
    page.go("/")
    page.update()

if __name__ == "__main__":
    app(target=main)