"""Main page for BIM-DES simulation"""

from dash import Dash, html
import dash_bootstrap_components as dbc
from dash_compose import composition

app = Dash(
    external_stylesheets=[dbc.themes.UNITED]
)

@composition
def layout():
    """Layout of the page."""
    with html.Div(className='m-3') as ret:
        yield html.H1('BIM-DES histopathology demo', className='mb-4')
        with dbc.Card():
            with dbc.CardBody(class_name='p-3'):
                yield html.H2('Runner time computation')
                with dbc.Stack(class_name='mb-5', gap=2):
                    with dbc.Stack(direction='horizontal', gap=3):
                        with dbc.Button(color='primary'):
                            yield 'Upload .ifc geometry file'
                        with html.Span():
                            yield 'No file uploaded yet.'
                    with dbc.Stack(direction='horizontal', gap=3):
                        with dbc.Button(color='primary'):
                            yield 'Upload .xlsx configuration file'
                        with html.Span():
                            yield 'No file uploaded yet.'
                    with dbc.Stack(direction='horizontal', gap=3):
                        with dbc.Button(color='info'):
                            yield 'Download .xlsx configuration template file'
                with dbc.Stack(direction='horizontal', gap=3):
                    with dbc.Button(color='success', size='lg'):
                        yield 'Compute runner times!'
                yield dbc.Stack(id='bim-results')

    return ret

app.layout = layout

if __name__ == '__main__':
    app.run(debug=True)
