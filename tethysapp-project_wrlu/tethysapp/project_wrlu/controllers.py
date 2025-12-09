import os
from dotenv import load_dotenv
from tethys_sdk.routing import controller
from tethys_sdk.gizmos import Button, MapView, MVView, MVDraw, MVLayer

from django.urls import reverse_lazy
from tethys_sdk.layouts import MapLayout
from .app import App

from tethys_sdk.gizmos import LinePlot


# --------------------------
# Load .env file
# --------------------------
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

BUCKET_NAME = os.getenv('BUCKET_NAME')
BUCKET_KEY = os.getenv('BUCKET_KEY')

# Build GeoJSON URL (public S3)
geojson_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{BUCKET_KEY}"


@controller
def home(request):
    """
    Controller for the app home page with buttons and a map.
    """

    # --------------------------
    # Buttons
    # --------------------------
    save_button = Button(
        display_text='',
        name='save-button',
        icon='save',
        style='success',
        attributes={
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'Save'
        }
    )

    edit_button = Button(
        display_text='',
        name='edit-button',
        icon='pen',
        style='warning',
        attributes={
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'Edit'
        }
    )

    remove_button = Button(
        display_text='',
        name='remove-button',
        icon='trash',
        style='danger',
        attributes={
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'Remove'
        }
    )

    previous_button = Button(
        display_text='Previous',
        name='previous-button',
        attributes={
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'Previous'
        }
    )

    next_button = Button(
        display_text='Next',
        name='next-button',
        attributes={
            'data-bs-toggle': 'tooltip',
            'data-bs-placement': 'top',
            'title': 'Next'
        }
    )

    # --------------------------
    # Map View Layer
    # --------------------------
    map_layer = MVLayer(
        source='GeoJSON',
        options={
            'url': geojson_url
        },
        layer_options={
            'style': {
                'ol.style.Style': {
                    'stroke': {'ol.style.Stroke': {'color': 'blue', 'width': 2}},
                    'fill': {'ol.style.Fill': {'color': 'blue', 'fillOpacity': 0.5}},
                }
            }
        },
        legend_title='WRLU 1989–1999'
    )

    basemaps = ['OpenStreetMap']

    # --------------------------
    # View Options
    # --------------------------

    view_options = MVView(
        projection='EPSG:4326',
        center=[-112.0, 40.7],
        zoom=8,
        maxZoom=18,
        minZoom=5
    )

    # --------------------------
    # Define drawing options
    # --------------------------
    drawing_options = MVDraw(
        controls=['Modify', 'Delete', 'Move', 'Point', 'LineString', 'Polygon', 'Box'],
        initial='Point',
        output_format='WKT'
    )

    # --------------------------
    # Define controls
    # --------------------------
    controls_settings=[
            'ZoomSlider', 'Rotate', 'FullScreen',
            {'ZoomToExtent': {
                'projection': 'EPSG:4326',
                'extent': [-112.026062, 41.088677, -111.82315, 41.76016]  #: Utah
            }}
            ]

    # --------------------------
    # MapView
    # --------------------------
    my_map = MapView(
        height='500px',
        width='100%',
        controls=controls_settings,
        layers=map_layer,
        view=view_options,
        basemap=basemaps,
        draw=drawing_options,
        legend=True
    )

    # WRLU entries per year
    wrlu_data = {
        1989: 6251,
        1991: 4397,
        1992: 18048,
        1994: 8668,
        1995: 45882,
        1996: 21634,
        1997: 6183,
        1998: 6623,
        1999: 19457
    }

    # Convert to list of [year, count] for the plot
    series_data = [[year, count] for year, count in sorted(wrlu_data.items())]

    # Create LinePlot
    wrlu_plot = LinePlot(
        height='350px',
        width='700px',
        engine='highcharts',
        title='WRLU Data Collection Trend in Utah',
        subtitle='1989–1999 (missing 1990, 1993)',
        spline=True,                  # smooth line
        x_axis_title='Year',
        y_axis_title='Number of Entries',
        x_axis_units='year',
        y_axis_units='entries',
        series=[
            {
                'name': 'WRLU Entries',
                'color': '#1f77b4',
                'marker': {'enabled': True},  # show points for each year
                'data': series_data
            }
        ]
    )

    # --------------------------
    # Dummy LinePlot
    # --------------------------
    # line_plot_view = LinePlot(
    #     height='400px',
    #     width='100%',
    #     engine='highcharts',
    #     title='Dummy Plot',
    #     series=[{'name':'Test', 'color':'#0066ff','data':[[1989,1],[1991,2],[1992,3],[1994,4],[1995,5]]}]
    # )


    # --------------------------
    # Context
    # --------------------------
    context = {
        'save_button': save_button,
        'edit_button': edit_button,
        'remove_button': remove_button,
        'previous_button': previous_button,
        'next_button': next_button,
        'my_map': my_map,
        'wrlu_plot': wrlu_plot
    }

    return App.render(request, 'home.html', context)