from keg_auth import NavItem, NavURL


def init_navigation(app):
    # create a main navigation menu for the app. Displayed links will be limited
    # by auth status
    app.auth_manager.add_navigation_menu(
        'main',
        NavItem(
            NavItem(
                'Auth',
                NavItem('Logout', NavURL('auth.logout')),
                NavItem('Bundles', NavURL('auth.bundle:list')),
                NavItem('Groups', NavURL('auth.group:list')),
                NavItem('Users', NavURL('auth.user:list')),
            ),
        )
    )
