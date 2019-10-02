import webgrid
import webgrid.flask


class Grid(webgrid.BaseGrid):
    manager = webgrid.flask.WebGrid()
    session_on = True
