#!/usr/bin/env python

import dash
import dash_bootstrap_components as dbc
from dash import (
    dcc,
    html,
    Input,
    Output,
    State,
    callback,
    ALL
)
from dash.exceptions import PreventUpdate

# Barcode SVG generation
from io import BytesIO
import barcode
from barcode.writer import SVGWriter

import datetime

# Data wrangling
import pandas as pd

dash.register_page(__name__, path="/")

# TODO: might replace this by a json file if it grows too large
phase_map = {
        "Assay Transfer": {
            "abbreviation": "AsT",
            "definition": "",
            "description": "",
        },
        "Pilot Screen": {
            "abbreviation": "PiS",
            "definition": "",
            "description": "",
        },
        "Primary Screen": {
            "abbreviation": "PrS",
            "definition": "",
            "description": "A primary screen refers to an initial step in the drug development process where a large number of chemical compounds or substances are tested to identify potential candidates for further evaluation. The primary screen is designed to quickly assess the biological activity of these compounds."
        },
        "Hit Confirmation": {
            "abbreviation": "HiC",
            "definition": "",
            "description": "",
        },
        "Activity Determination": {
            "abbreviation": "AcD",
            "definition": "",
            "description": "",
        },
        "Reference": {
            "abbreviation": "Ref",
            "definition": "",
            "description": "",
        },
        "Motherplate": {
            "abbreviation": "MP",
            "definition": "",
            "description": "The 'motherplate' refers to a source plate or master plate that contains a large number of samples, compounds, or substances that are typically used for creating multiple copies, or 'daughter plates,' for various experiments, assays, or screening processes.",
        },
}


def generate_info():
    """Generates a 2D grid with cards in a Div"""
    contents = [
            # html.H2("Phase Glossary", style={"textAlign": "center"})
    ]
    cards = []
    for phase, properties in phase_map.items():
        cards.append(
            dbc.Card([
                dcc.Markdown(
                    f"""
                    ### {phase} ({properties["abbreviation"]})
                    **Definition:**
                    {properties["definition"]}

                    **Description:**
                    {properties["description"]}
                    """
                )
            ])
        )
    # if number of cards is uneven, make them even by adding None
    # this is necessary as otherwise the last card is swallowed
    if len(cards) % 2 == 1:
        cards.append(None)
    tandem_list = list(zip(cards, cards[1:]))[::2]
    for card_a, card_b in tandem_list:
        contents.append(
            dbc.Row([
                dbc.Col([
                    card_a
                ]),
                dbc.Col([
                    card_b
                ])
            ])
        )
    return html.Div(contents)


layout = dbc.Container(id="barcodes-container", children = [
    dcc.Store(id="barcodes-child-storage"),
    dcc.Store(id="barcodes-platetypes-storage"),
    html.P(id="barcodes-placeholder"),
    html.H1("Barcode Generator", style={"textAlign": "center"}),
    dcc.Tabs(id="barcodes-tabs_cards", children=[
        dcc.Tab(label="Assay Plates", children=[
            dbc.Card([
                dbc.Row([
                    dbc.Col([
                        # Outer row col end
                        dbc.Row([
                            dbc.Col([
                                html.Label(
                                    "Project Nr.",
                                )
                            ], width=2),
                            dbc.Col([
                                dcc.Input(
                                    id="barcodes-input-project_nr",
                                    type="number",
                                    min=1,
                                    max=999,
                                    autoFocus=True,
                                    # required=True,
                                    # placeholder="1"
                                ),
                            ], width=2)
                        ], justify="center"),
                        # Next row
                        dbc.Row([
                            dbc.Col([
                                html.Label(
                                    "Run Nr.",
                                )
                            ], width=2),
                            dbc.Col([
                                dcc.Input(
                                    id="barcodes-input-run_nr",
                                    type="number",
                                    min=1,
                                    max=99,
                                    # placeholder="1"
                                ),
                            ], width=2)
                        ], justify="center"),
                        dbc.Row([
                            dbc.Col([
                                html.Label(
                                    "Start at",
                                )
                            ], width=2),
                            dbc.Col([
                                dcc.Input(
                                    id="barcodes-input-startat",
                                    type="number",
                                    min=1,
                                    value=1,
                                    # placeholder="1"
                                ),
                            ], width=2)
                        ], justify="center"),
                        dbc.Row([
                            dbc.Col([
                                dcc.Dropdown(
                                    options=list(phase_map.keys()),
                                    id="barcodes-input-phase",
                                    placeholder="Phase",
                                ),
                                ], width={"size": 2, "offset": 2}),
                        ], justify="center"),
                        dbc.Row([
                            dbc.Col([
                                html.Label("Platetype"),
                                ], width={"size": 2, "offset": 6}
                            ),
                            dbc.Col([
                                html.Label("Amount"),
                                ], width={"size": 2}
                            ),
                            dbc.Col([
                                html.Label("Date of Experiment")
                                ], width={"size": 2})
                        ], justify="center"),
                        dbc.Row([
                            dbc.Col([
                                html.Button(
                                    "Add Plate Type",
                                    id="barcodes-additional_plate_type",
                                    n_clicks=0,
                                    # disabled=True,
                                    # TODO: make additional css button in green :)
                                    className="button-add",
                                    # style={"margin-top": "15px"}
                                )
                                    ], width={"size": 2, "offset": 4}),
                            dbc.Col([
                                html.Div(id="barcodes-platetype_div"),
                            ])
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.Button(
                                    "Write Barcodes File",
                                    id="barcodes-write_button",
                                    n_clicks=0,
                                    disabled=True,
                                    className="button-22",
                                    style={"margin-top": "15px"}
                                    ),
                                dcc.Download(id="barcodes-download_dataframe"),
                                dcc.Download(id="barcodes-download_cybio_df"),
                            ], width=2)
                        ], justify="center")
                    ]),
                ]),
            ], body=True),
            html.Div(id="barcodes-generator_div"),
        ]),
        dcc.Tab(label="Phase Glossary", children=[
            dbc.Card([
                generate_info()
            ], body=True),
        ]),
    ]),
])


"""
Generates a new platetype-row.
"""
def get_platetyperow(
        index,
        info=None,
        amount=None,
        date=datetime.date.today() # use todays date as starting default
        ):
    """
    info: barcodes-platetype_info
    amount: barcodes-platetype_amount
    """
    row = dbc.Row([
        dbc.Col([
            dcc.Input(
                id={
                    'type': "barcodes-platetype_info",
                    'index': index
                },
                type="text",
                value=info,
                placeholder="e.g. Strain"
            ),
            ], width=4),
        dbc.Col([
            dcc.Input(
                id={
                    'type': "barcodes-platetype_amount",
                    'index': index
                },
                type="number",
                min=1,
                value=amount,
                placeholder=""
            ),
        ], width=4),
        dbc.Col([
            dcc.DatePickerSingle(
                id={
                    'type': "barcodes-platetype_date",
                    'index': index
                },
                date=date,
                display_format='DD.MM.YYYY'
                )
            ])
    ], justify="start")
    return row


@callback(
    Output("barcodes-platetype_div", "children"),
    Input("barcodes-additional_plate_type", "n_clicks"),
    State({'type': "barcodes-platetype_info", 'index': ALL}, 'value'),
    State({'type': "barcodes-platetype_amount", 'index': ALL}, 'value'),
    State({'type': "barcodes-platetype_date", 'index': ALL}, 'date'),
)
def generate_platetypes(
        n_clicks,
        platetype_infos,
        platetype_amounts,
        platetype_dates,
        ):
    # TODO: add button to delete the last platetype
    platetypes = []
    if n_clicks > 0:
        # Initialize new empty platetype row:
        platetype_infos.append(None)
        platetype_amounts.append(None)
        # Use the last date from the previous row for the new row:
        year, month, day = [int(i) for i in platetype_dates[-1:][0].split("-")]
        platetype_dates.append(datetime.date(year, month, day))
        # Reconstruct the already known platetype rows:
        for i, (info, amount, date) in enumerate(
                zip(platetype_infos, platetype_amounts, platetype_dates),
                start=1
        ):
            platetypes.append(
                get_platetyperow(i, info, amount, date)
            )
    else:  # Initialize with index 1
        print(datetime.date.today())
        platetypes = [
            get_platetyperow(1, date=datetime.date.today())
        ]
    return platetypes


@callback(
    Output("barcodes-child-storage", "data"),
    Output("barcodes-generator_div", "children"),
    Output("barcodes-write_button", "disabled"),
    Input("barcodes-input-project_nr", "value"),
    Input("barcodes-input-run_nr", "value"),
    Input("barcodes-input-phase", "value"),
    Input("barcodes-input-startat", "value"),
    Input({'type': "barcodes-platetype_info", 'index': ALL}, 'value'),
    Input({'type': "barcodes-platetype_amount", 'index': ALL}, 'value'),
    Input({'type': "barcodes-platetype_date", 'index': ALL}, 'date'),
)
def generate_assay_barcodes(
    project_nr: str,
    run_nr: str,
    phase: str,
    startat: int,
    platetype_infos,
    platetype_amounts,
    platetype_dates,
):
    # Take the first two letters of the first word and the first letter of the
    # second word for phase abbreviation
    barcode_objects = []
    input_info_dict = {
        "Barcode": [],
        "ProjectNr": [],
        "PlateNr": [],
        "Phase": [],
        "PhaseID": [],
        "RunNr": [],
        "Date": [],
        "Info": [],
    }
    if any(map(lambda x: x == None, [
        project_nr,
        run_nr,
        phase,
        *platetype_infos,
        *platetype_amounts
        # *platetype_dates,
        ])):
        raise PreventUpdate
    else:
        code128 = barcode.get_barcode_class("code128")

        # we need the platenumbers from start to end with corresponding infos
        """
            Small utility function to repeat a single entry like platetype
            or date for x amount of plates
        """
        def string_repeats(strings: list[str], repeats: list[int]) -> list[str]:
            return sum([[x] *y for x, y in zip(strings, repeats)], [])
        plates_infos_rep = string_repeats(platetype_infos, platetype_amounts)
        plates_dates_rep = string_repeats(platetype_dates, platetype_amounts)
        amount = sum(platetype_amounts)

        for plate_nr in range(amount):
            phase_id = phase_map[phase]["abbreviation"]
            bar = "".join([
                str(project_nr).zfill(3),
                phase_id,
                str(run_nr).zfill(2),
                str(startat + plate_nr).zfill(3)
            ])
            input_info_dict["Barcode"].append(bar)
            input_info_dict["ProjectNr"].append(project_nr)
            input_info_dict["PlateNr"].append(startat + plate_nr)
            input_info_dict["Phase"].append(phase)
            input_info_dict["PhaseID"].append(phase_id)
            input_info_dict["RunNr"].append(run_nr)
            input_info_dict["Date"].append(plates_dates_rep[plate_nr])
            input_info_dict["Info"].append(plates_infos_rep[plate_nr])
            barcode_buffer = BytesIO()
            code128(bar, writer=SVGWriter()).write(barcode_buffer)
            barcode_buffer = barcode_buffer.getvalue().decode()
            barcode_objects.extend([
                dbc.Card(
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Img(src=f"data:image/svg+xml;utf8,{barcode_buffer}")
                            ], width=2),
                            dbc.Col([
                                html.Label(plates_infos_rep[plate_nr])
                            ], width=2)
                        ], justify="center"),
                    ])
                )
            ])
        return input_info_dict, barcode_objects, False


@callback(
    Output("barcodes-download_dataframe", "data"),
    Output("barcodes-download_cybio_df", "data"),
    Input("barcodes-write_button", "n_clicks"),
    Input("barcodes-child-storage", "data"),
)
def write_barcodes(
    button_clicks,
    input_info_dict,
):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    # dash.callback_context.triggered captures the properties that have changed
    # since last call back. That means even after n_clicks becomes positive,
    # it may not be part of dash.callback_context.triggered.
    # Thus, use of the latter prevents unwanted firing of callbacks based on n_clicks
    # https://stackoverflow.com/questions/62671226/plotly-dash-how-to-reset-the-n-clicks-attribute-of-a-dash-html-button
    if "barcodes-write_button" in changed_id:
        # column_headers = [
        #     "Barcode",                                # Barcode
        #     *[f"value{i}" for i in range(1, 9+1, 1)]  # value1, ..., value9
        # ]

        barcode_df = pd.DataFrame(input_info_dict)  #, columns=column_headers)
        # TODO: change csv filename
        # project_nr, plate_nr, plate_nr_str, phase, phase_id, run_nr, strain
        # print(input_info)
        # print(barcode_df)
        # rename columns so cybio quadprint AJ software wont bitch
        # format date
        barcode_df["Date"] = barcode_df["Date"].apply(lambda x: x.replace("-", ""))
        cybio_print_df = barcode_df.rename(columns={
            "ProjectNr": "value1",
            "PlateNr": "value2",
            "Phase": "value3",
            "PhaseID": "value4",
            "RunNr": "value5",
            "Info": "value6",
            "Date": "value7",
        })
        # Do some formatting so the information can be printed pretty
        cybio_print_df["value1"] = cybio_print_df["value1"].apply(lambda x: str(x).zfill(3))
        cybio_print_df["value2"] = cybio_print_df["value2"].apply(lambda x: str(x).zfill(3))
        cybio_print_df["value5"] = cybio_print_df["value5"].apply(lambda x: str(x).zfill(2))
        cybio_print_df["value7"] = cybio_print_df["value7"].apply(lambda x: x[2:])
        fill_df = pd.DataFrame({
            f"value{i}": [""] * (10 - len(cybio_print_df))\
            for i in range(cybio_print_df.shape[1], 10, 1)
        })
        cybio_print_df = pd.concat([cybio_print_df, fill_df], axis=1)

        # Sort by column
        cybio_print_df = cybio_print_df.sort_index(axis=1)
        cybio_print_df = cybio_print_df.dropna(subset="Barcode")

        # TODO: send both dataframes as csv files over scp to lab pc
        return \
            dcc.send_data_frame(
                cybio_print_df.to_csv,
                f'{str(barcode_df["ProjectNr"][0]).zfill(3)}_'
                f'{barcode_df["PhaseID"][0]}_'
                f'{str(barcode_df["RunNr"][0]).zfill(2)}_'
                f'cybio_barcodes_'
                f'{barcode_df["Date"][0]}'
                f'.csv',
                sep=";",
                index=False
            ), dcc.send_data_frame(
                barcode_df.to_csv,
                f'{str(barcode_df["ProjectNr"][0]).zfill(3)}_'
                f'{barcode_df["PhaseID"][0]}_'
                f'{str(barcode_df["RunNr"][0]).zfill(2)}_'
                f'barcodes_'
                f'{barcode_df["Date"][0]}'
                f'.csv',
                sep=";",
                index=False
            )
    else:
        raise PreventUpdate
