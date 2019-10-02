from keg_auth import NavItem, NavURL


def init_navigation(app):
    # create a main navigation menu for the app. Displayed links will be limited
    # by auth status
    app.auth_manager.add_navigation_menu(
        'main',
        NavItem(
            NavItem('Home', NavURL('public.home'), icon_class='fas fa-home'),
            NavItem('Blog', NavURL('private.blog:list'), icon_class='fas fa-blog'),
            NavItem(
                'Pages',
                NavItem('Hello', NavURL('public.hello')),
                NavItem('Protected', NavURL('private.protected_example'),
                        icon_class='fas fa-lock'),
                NavItem('Alerts Demo', NavURL('public.alerts-demo')),
                icon_class='fas fa-file',
            ),
            NavItem(
                'Management',
                NavItem('Bundles', NavURL('auth.bundle:list'), icon_class='fas fa-briefcase'),
                NavItem('Groups', NavURL('auth.group:list'), icon_class='fas fa-users'),
                NavItem('Users', NavURL('auth.user:list'), icon_class='fas fa-user'),
                icon_class='fas fa-cog',
            ),
        )
    )
