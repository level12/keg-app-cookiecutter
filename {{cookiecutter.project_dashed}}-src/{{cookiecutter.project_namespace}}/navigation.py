from keg_auth import NavItem, NavURL


def init_navigation(app):
    # create a main navigation menu for the app. Displayed links will be limited
    # by auth status
    app.auth_manager.add_navigation_menu(
        'main',
        NavItem(
            NavItem(
                'Management',
                NavItem('Bundles', NavURL('auth.bundle:list'), icon_class='fas fa-briefcase'),
                NavItem('Groups', NavURL('auth.group:list'), icon_class='fas fa-users'),
                NavItem('Users', NavURL('auth.user:list'), icon_class='fas fa-user'),
                icon_class='fas fa-cog',
            ),
        )
    )
