from keg_auth import Node, Route


def init_navigation(app):
    # create a main navigation menu for the app. Displayed links will be limited
    # by auth status
    app.auth_manager.add_navigation_menu(
        'main',
        Node(
            Node('Home', Route('public.home')),
            Node(
                'Pages',
                Node('Hello', Route('public.hello')),
                Node('Protected', Route('private.protected_example')),
            ),
            Node(
                'Management',
                Node('Bundles', Route('auth.bundle:list')),
                Node('Groups', Route('auth.group:list')),
                Node('Users', Route('auth.user:list')),
            ),
        )
    )
