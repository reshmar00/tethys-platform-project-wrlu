import os
from dotenv import load_dotenv
from tethys_sdk.routing import controller
from tethys_sdk.gizmos import Button, MapView, MVView, MVDraw, MVLayer

from django.urls import reverse_lazy
from tethys_sdk.layouts import MapLayout
from .app import App

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
    # view_options = MVView(
    #     projection='EPSG:4326',
    #     center=[41.1, -111.5],   # <-- Utah center (latitude, longitude)
    #     zoom=10,
    #     maxZoom=18,
    #     minZoom=5
    # )

    view_options = MVView(
        projection='EPSG:4326',
        center=[-111.924606, 41.4244185],
        zoom=10,
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
        layers=[map_layer],
        view=view_options,
        basemap=basemaps,
        draw=drawing_options,
        legend=True
    )

    # my_map = MapView(
    #     height='100%',
    #     width='100%',
    #     controls=[
    #         'ZoomSlider', 'Rotate', 'FullScreen',
    #         {'ZoomToExtent': {
    #             'projection': 'EPSG:4326',
    #             'extent': [-112.026062, 41.088677, -111.82315, 41.76016]  #: Utah
    #         }}
    #         ],

    #         basemap='OpenStreetMap',
    #         view=MVView(
    #             projection='EPSG:4326',
    #             center=[-111.924606, 41.4244185],
    #             zoom=7,
    #             maxZoom=18,
    #             minZoom=2
    #         )
    #     )


    # --------------------------
    # Context
    # --------------------------
    context = {
        'save_button': save_button,
        'edit_button': edit_button,
        'remove_button': remove_button,
        'previous_button': previous_button,
        'next_button': next_button,
        'my_map': my_map
    }

    return App.render(request, 'home.html', context)