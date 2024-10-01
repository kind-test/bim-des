"""Main page for BIM-DES simulation"""

from base64 import b64decode
from io import BytesIO
from pathlib import Path
from tempfile import NamedTemporaryFile
from dash import Dash, callback, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import openpyxl as oxl
from dash_compose import composition

from ..bim import BimModel, runner_times
from ..config.runners import RunnerConfig

app = Dash(
    external_stylesheets=[dbc.themes.UNITED]
)


@composition
def layout():
    """Layout of the page."""
    with html.Div(className='m-3') as ret:
        yield html.H1('BIM-DES histopathology demo', className='mb-4')
        yield html.P('Note: page may appear unresponsive while computations are ongoing.')
        with dbc.Card():
            with dbc.CardBody(class_name='p-3'):
                yield html.H2('Runner time computation')
                with dbc.Stack(class_name='mb-5', gap=2):

                    # IFC GEOMETRY FILE - BUTTON, UPLOAD, STORE
                    with dbc.Stack(direction='horizontal', gap=3):
                        with dcc.Upload(id='upload-ifc-file'):
                            with dbc.Button(id='btn-upload-ifc-file', color='primary'):
                                yield 'Upload .ifc geometry file'
                        with html.Div(id='span-ifc-file-status'):
                            yield 'No file uploaded yet.'
                        yield dcc.Store(id='store-ifc-model')
                    
                    # RUNNER TIME CONFIG FILE - BUTTON, UPLOAD, STORE
                    with dbc.Stack(direction='horizontal', gap=3):
                        with dcc.Upload(id='upload-bim-config', accept='.xlsx'):
                            with dbc.Button(id='btn-upload-bim-config', color='primary'):
                                yield 'Upload configuration file (.xlsx)'
                        with html.Div(id='span-bim-config-status'):
                            yield 'No file uploaded yet.'
                        yield dcc.Store(id='store-bim-config')
                    
                    # DOWNLOAD EXAMPLE CONFIG FILE
                    with dbc.Stack(direction='horizontal', gap=3):
                        with dbc.Button(id='button-bim-template', color='info'):
                            yield 'Download configuration template file'
                            yield dcc.Download(id='download-bim-template')
                
                # COMPUTE RUNNER TIMES
                with dbc.Stack(direction='horizontal', gap=3):
                    with dbc.Button(id='btn-compute-runner-times', color='success', size='lg'):
                        yield 'Compute runner times!'
                
                # RESULTS!
                yield dbc.Stack(id='bim-results')

    return ret


app.layout = layout

# region callbacks
@callback(
    Output('span-ifc-file-status', 'children'),
    Output('store-ifc-model', 'data'),

    Input('upload-ifc-file', 'contents'),
    State('upload-ifc-file', 'filename'),

    running=[
        (Output('span-ifc-file-status', 'children'), 'Uploading/parsing...', 'Complete'),
        (Output('btn-upload-ifc-file', 'disabled'), True, False)
    ],
    prevent_initial_call=True
)
def upload_ifc_file(file_b64: str, file_name: str):
    """Validate an uploaded IFC model file and save it.  Since we can't actually save the model
    in a dcc.Store, we save the content_str (base 64 string) instead."""
    try:
        _, content_str = file_b64.split(',')
        file_bytes = b64decode(content_str)

        with NamedTemporaryFile(mode='wb', suffix='.ifc', delete_on_close=False) as file:
            file.write(file_bytes)
            file.close()
            _ = BimModel.from_ifc(file.name)  # Validation
            return f'Sucessfully parsed {file_name}', content_str  # Save base64 string
    except Exception as e:
        return html.Pre(className='text-danger', children=str(e)), None

@callback(
    Output('download-bim-template', 'data'),
    Input('button-bim-template', 'n_clicks'),
    prevent_initial_call=True
)
def download_runner_template(_):
    """Return the runner times .xlsx template file when the matching button is pressed."""
    path = Path(__file__) / '../../assets/runner_times_template.xlsx'
    path = path.resolve()
    return dcc.send_file(path, filename='runner_times_template.xlsx')

@callback(
    Output('span-bim-config-status', 'children'),
    Output('store-bim-config', 'data'),

    Input('upload-bim-config', 'contents'),
    State('upload-bim-config', 'filename'),

    running=[
        (Output('span-bim-config-status', 'children'), 'Uploading/parsing...', 'Complete'),
        (Output('btn-upload-bim-config', 'disabled'), True, False)
    ],
    prevent_initial_call=True
)
def upload_runner_config(file_b64: str, file_name: str):
    """Validate an uploaded runner config file, parsing it and saving the config as JSON."""
    try:
        _, content_str = file_b64.split(',')
        file_bytes = b64decode(content_str)
        wbook = oxl.load_workbook(BytesIO(file_bytes), data_only=True)
        cfg: RunnerConfig = RunnerConfig.from_excel(wbook)
        return f'Sucessfully parsed {file_name}', cfg.model_dump(mode='json')
    except Exception as e:
        return html.Pre(className='text-danger', children=str(e)), None

@callback(
    Output('btn-compute-runner-times', 'disabled'),
    Input('store-ifc-model', 'data'),
    Input('store-bim-config', 'data')
)
def bim_compute_button_state(ifc_data, config_data):
    """Enable the 'Compute runner times' button if and only if both required files have been
    uploaded."""
    return not (bool(ifc_data) and bool(config_data))
# endregion

# region app.run
if __name__ == '__main__':
    app.run(debug=True)
# endregion
