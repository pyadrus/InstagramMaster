import flet as ft

program_version, date_of_program_change = "0.0.1", "07.04.2024"  # Версия программы, дата изменения


def run():
    def main(page: ft.Page):
        page.title = f"InstagramMaster: {program_version} (Дата изменения {date_of_program_change})"
        page.window_width = 520  # window's width is 200 px
        page.window_height = 650  # window's height is 200 px
        page.window_resizable = False  # window is not resizable

        # width - ширина,  # height - высота
        def route_change(route):
            page.views.clear()
            page.views.append(
                ft.View("/", [ft.AppBar(title=ft.Text("Главное меню"),
                                        bgcolor=ft.colors.SURFACE_VARIANT),
                              ft.Text(spans=[ft.TextSpan(
                                  "InstagramMaster",
                                  ft.TextStyle(
                                      size=40,
                                      weight=ft.FontWeight.BOLD,
                                      foreground=ft.Paint(
                                          gradient=ft.PaintLinearGradient((0, 20), (150, 20), [ft.colors.PINK,
                                                                                               ft.colors.PURPLE])), ), ), ], ),
                              ft.Text(disabled=False,
                                      spans=[ft.TextSpan("Аккаунт  Telegram: "),
                                             ft.TextSpan("https://t.me/PyAdminRU",
                                                         ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
                                                         url="https://t.me/PyAdminRU", ), ], ),
                              ft.Text(disabled=False,
                                      spans=[ft.TextSpan("Канал Telegram: "),
                                             ft.TextSpan("https://t.me/master_tg_d",
                                                         ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
                                                         url="https://t.me/master_tg_d", ), ], ),
                              # Кнопки в меню "Главное меню"
                              ft.ElevatedButton(width=500, height=30, text="Парсинг постов со страницы",
                                                on_click=lambda _: page.go("/parsing_posts_from_page")),
                              ft.ElevatedButton(width=500, height=30, text="Парсинг reels со страницы",
                                                on_click=lambda _: page.go("/parsing")),
                              ft.ElevatedButton(width=500, height=30, text="Скачать посты instagram со страницы",
                                                on_click=lambda _: page.go("/contacts")),
                              ft.ElevatedButton(width=500, height=30, text="Скачать reels instagram со страницы",
                                                on_click=lambda _: page.go("/subscribe_unsubscribe")),
                              ft.ElevatedButton(width=500, height=30, text="Запись в google",
                                                on_click=lambda _: page.go("/store")),
                              ft.ElevatedButton(width=500, height=30, text="Работа с Яндекс диском",
                                                on_click=lambda _: page.go("/sending_messages")),
                              ft.ElevatedButton(width=500, height=30, text="Настройки",
                                                on_click=lambda _: page.go("/reaction")),
                              ], ))
            if page.route == "/parsing_posts_from_page":
                page.views.append(
                    ft.View("/parsing_posts_from_page", [ft.AppBar(title=ft.Text("Главное меню"),
                                                                   bgcolor=ft.colors.SURFACE_VARIANT),
                                                         ft.Text(disabled=False,
                                                                 spans=[ft.TextSpan("Аккаунт  Telegram: "),
                                                                        ft.TextSpan("https://t.me/PyAdminRU",
                                                                                    ft.TextStyle(
                                                                                        decoration=ft.TextDecoration.UNDERLINE),
                                                                                    url="https://t.me/PyAdminRU", ), ], ),
                                                         ft.Text(disabled=False,
                                                                 spans=[ft.TextSpan("Канал Telegram: "),
                                                                        ft.TextSpan("https://t.me/master_tg_d",
                                                                                    ft.TextStyle(
                                                                                        decoration=ft.TextDecoration.UNDERLINE),
                                                                                    url="https://t.me/master_tg_d", ), ], ),
                                                         ft.ElevatedButton(width=500, height=30, text="Go Home",
                                                                           on_click=lambda _: page.go("/")), ], ))
            elif page.route == "/parsing":
                page.views.append(
                    ft.View("/parsing", [ft.AppBar(title=ft.Text("Главное меню"),
                                                   bgcolor=ft.colors.SURFACE_VARIANT),
                                         ft.Text(disabled=False,
                                                 spans=[ft.TextSpan("Аккаунт  Telegram: "),
                                                        ft.TextSpan("https://t.me/PyAdminRU",
                                                                    ft.TextStyle(
                                                                        decoration=ft.TextDecoration.UNDERLINE),
                                                                    url="https://t.me/PyAdminRU", ), ], ),
                                         ft.Text(disabled=False,
                                                 spans=[ft.TextSpan("Канал Telegram: "),
                                                        ft.TextSpan("https://t.me/master_tg_d",
                                                                    ft.TextStyle(
                                                                        decoration=ft.TextDecoration.UNDERLINE),
                                                                    url="https://t.me/master_tg_d", ), ], ),
                                         ft.ElevatedButton(width=500, height=30, text="Go Home",
                                                           on_click=lambda _: page.go("/")), ], ))
            elif page.route == "/contacts":
                page.views.append(
                    ft.View("/contacts", [ft.AppBar(title=ft.Text("Главное меню"),
                                                    bgcolor=ft.colors.SURFACE_VARIANT),
                                          ft.Text(disabled=False,
                                                  spans=[ft.TextSpan("Аккаунт  Telegram: "),
                                                         ft.TextSpan("https://t.me/PyAdminRU",
                                                                     ft.TextStyle(
                                                                         decoration=ft.TextDecoration.UNDERLINE),
                                                                     url="https://t.me/PyAdminRU", ), ], ),
                                          ft.Text(disabled=False,
                                                  spans=[ft.TextSpan("Канал Telegram: "),
                                                         ft.TextSpan("https://t.me/master_tg_d",
                                                                     ft.TextStyle(
                                                                         decoration=ft.TextDecoration.UNDERLINE),
                                                                     url="https://t.me/master_tg_d", ), ], ),
                                          ft.ElevatedButton(width=500, height=30, text="Go Home",
                                                            on_click=lambda _: page.go("/")), ], ))
            elif page.route == "/subscribe_unsubscribe":
                page.views.append(
                    ft.View("/subscribe_unsubscribe", [ft.AppBar(title=ft.Text("Главное меню"),
                                                                 bgcolor=ft.colors.SURFACE_VARIANT),
                                                       ft.Text(disabled=False,
                                                               spans=[ft.TextSpan("Аккаунт  Telegram: "),
                                                                      ft.TextSpan("https://t.me/PyAdminRU",
                                                                                  ft.TextStyle(
                                                                                      decoration=ft.TextDecoration.UNDERLINE),
                                                                                  url="https://t.me/PyAdminRU", ), ], ),
                                                       ft.Text(disabled=False,
                                                               spans=[ft.TextSpan("Канал Telegram: "),
                                                                      ft.TextSpan("https://t.me/master_tg_d",
                                                                                  ft.TextStyle(
                                                                                      decoration=ft.TextDecoration.UNDERLINE),
                                                                                  url="https://t.me/master_tg_d", ), ], ),
                                                       ft.ElevatedButton(width=500, height=30, text="Go Home",
                                                                         on_click=lambda _: page.go("/")), ], ))
            elif page.route == "/sending_messages":
                page.views.append(
                    ft.View("/sending_messages", [ft.AppBar(title=ft.Text("Главное меню"),
                                                            bgcolor=ft.colors.SURFACE_VARIANT),
                                                  ft.Text(disabled=False,
                                                          spans=[ft.TextSpan("Аккаунт  Telegram: "),
                                                                 ft.TextSpan("https://t.me/PyAdminRU",
                                                                             ft.TextStyle(
                                                                                 decoration=ft.TextDecoration.UNDERLINE),
                                                                             url="https://t.me/PyAdminRU", ), ], ),
                                                  ft.Text(disabled=False,
                                                          spans=[ft.TextSpan("Канал Telegram: "),
                                                                 ft.TextSpan("https://t.me/master_tg_d",
                                                                             ft.TextStyle(
                                                                                 decoration=ft.TextDecoration.UNDERLINE),
                                                                             url="https://t.me/master_tg_d", ), ], ),
                                                  ft.ElevatedButton(width=500, height=30, text="Go Home",
                                                                    on_click=lambda _: page.go("/")), ], ))
            elif page.route == "/reaction":
                page.views.append(
                    ft.View("/reaction", [ft.AppBar(title=ft.Text("Главное меню"),
                                                    bgcolor=ft.colors.SURFACE_VARIANT),
                                          ft.Text(disabled=False,
                                                  spans=[ft.TextSpan("Аккаунт  Telegram: "),
                                                         ft.TextSpan("https://t.me/PyAdminRU",
                                                                     ft.TextStyle(
                                                                         decoration=ft.TextDecoration.UNDERLINE),
                                                                     url="https://t.me/PyAdminRU", ), ], ),
                                          ft.Text(disabled=False,
                                                  spans=[ft.TextSpan("Канал Telegram: "),
                                                         ft.TextSpan("https://t.me/master_tg_d",
                                                                     ft.TextStyle(
                                                                         decoration=ft.TextDecoration.UNDERLINE),
                                                                     url="https://t.me/master_tg_d", ), ], ),
                                          ft.ElevatedButton(width=500, height=30, text="Go Home",
                                                            on_click=lambda _: page.go("/")), ], ))
            elif page.route == "/settings":
                page.views.append(
                    ft.View("/settings", [ft.AppBar(title=ft.Text("Главное меню"),
                                                    bgcolor=ft.colors.SURFACE_VARIANT),
                                          ft.Text(disabled=False,
                                                  spans=[ft.TextSpan("Аккаунт  Telegram: "),
                                                         ft.TextSpan("https://t.me/PyAdminRU",
                                                                     ft.TextStyle(
                                                                         decoration=ft.TextDecoration.UNDERLINE),
                                                                     url="https://t.me/PyAdminRU", ), ], ),
                                          ft.Text(disabled=False,
                                                  spans=[ft.TextSpan("Канал Telegram: "),
                                                         ft.TextSpan("https://t.me/master_tg_d",
                                                                     ft.TextStyle(
                                                                         decoration=ft.TextDecoration.UNDERLINE),
                                                                     url="https://t.me/master_tg_d", ), ], ),
                                          ft.ElevatedButton(width=500, height=30, text="Go Home",
                                                            on_click=lambda _: page.go("/")), ], ))
                if page.route == "/link_entry":
                    print("Запись ссылки")

            page.update()

        def view_pop(view):
            page.views.pop()
            top_view = page.views[-1]
            page.go(top_view.route)

        page.on_route_change = route_change
        page.on_view_pop = view_pop
        page.go(page.route)

    # ft.app(target=main, view=ft.AppView.WEB_BROWSER)
    ft.app(target=main)


if __name__ == "__main__":
    run()
