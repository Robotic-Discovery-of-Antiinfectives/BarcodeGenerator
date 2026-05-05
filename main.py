import dash
from dash import Dash, html

# # use waitress as a wsgi server (windows...)
from waitress import serve
from socket import gethostname

# from numba.core.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings

# warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
# warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    title="Toolbox",
    use_pages=True
)

app.layout = html.Div([
    dash.page_container
])

# provide some information:
print("Dash version: ", dash.__version__)
print("Page registry: ", *dash.page_registry.keys(), sep="\n\t")


if __name__ == '__main__':
    # if gethostname() == "Ogygia":
    #     serve(app.server, listen='*:8000')
    # else:
    app.run(debug=True)
