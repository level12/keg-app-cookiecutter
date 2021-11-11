import webgrid
import webgrid.flask


class GridManager(webgrid.flask.WebGrid):
    args_loaders = (
        webgrid.extensions.RequestArgsLoader,
        webgrid.extensions.WebSessionArgsLoader,
        webgrid.extensions.RequestFormLoader,
    )


class Grid(webgrid.BaseGrid):
    manager = GridManager()
