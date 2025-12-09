import os
from dotenv import load_dotenv
from tethys_sdk.routing import controller
from tethys_sdk.gizmos import Button, MapView, MVLayer

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


    # --------------------------
    # MapView
    # --------------------------
    my_map = MapView(
        height='500px',
        width='100%',
        layers=[map_layer],
        controls=['ZoomSlider', 'FullScreen'],
        attribution='Data: S3 GeoJSON'
    )


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