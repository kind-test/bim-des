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
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

    with dbc.Stack() as ret:
        yield table
    return ret
