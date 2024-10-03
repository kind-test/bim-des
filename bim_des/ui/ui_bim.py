"""Functions for calling the main BIM module and displaying the results on the Dash app."""

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_compose import composition
import pandas as pd

from ..bim import BimModel, runner_times
from ..config.runners import RunnerConfig


@composition
def compute_runner_times(model: BimModel, config: RunnerConfig):
    """Compute the runner times and display the results."""

    print('Computing runner times...')
    rt = runner_times(model, config)
    print('Done!')

    df = pd.DataFrame(
        [[str(k).replace("'", ''), v] for k, v in rt.items()],
        columns=['runner_journey', 'runner_time']
    )
    df2 = df.copy().round({'runner_time': 3})
    table: dbc.Table = dbc.Table.from_dataframe(
        df2, striped=True, bordered=True, hover=True, class_name='w-auto')

    with dbc.Stack() as ret:
        yield html.H2('Runner times')
        with dbc.Stack(direction='horizontal'):
            yield table
        yield dcc.Store(id='store-bim-results', data={
            'runner_times': df.to_dict()
        })
    return ret
