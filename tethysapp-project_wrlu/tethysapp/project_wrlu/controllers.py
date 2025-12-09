import os
from dotenv import load_dotenv
from tethys_sdk.routing import controller
from tethys_sdk.gizmos import Button, MapView, MVView, MVDraw, MVLayer, LinePlot

from django.urls import reverse_lazy
from tethys_sdk.layouts import MapLayout
from .app import App
import pandas as pd
import requests
from io import StringIO
import boto3

# --------------------------
# Load .env file
# --------------------------

env_path = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    '.env'
)

load_dotenv(dotenv_path=env_path)

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

BUCKET_NAME = os.getenv('BUCKET_NAME')
GEOJSON_KEY = os.getenv('GEOJSON_KEY')
CSV_KEY = os.getenv('CSV_KEY')

# Build GeoJSON and CSV URLs (public S3)
geojson_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{GEOJSON_KEY}"
csv_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{CSV_KEY}"

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

    ########### Map Portion Start ###########

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

    ########### Map Portion End ###########

    ########### Plot Portion Start ###########

    # --------------------------
    # Load CSV from S3
    # --------------------------

    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    try:
        # Fetch CSV from S3
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=CSV_KEY)
        csv_content = response['Body'].read().decode('utf-8')
        
        # Load into pandas DataFrame
        df = pd.read_csv(StringIO(csv_content))

        # Aggregate total ACRES per SURVEY YEAR
        acres_per_year = df.groupby('SURVEY YEAR')['ACRES'].sum().reset_index()

        # Ensure years are integers
        acres_per_year['SURVEY YEAR'] = acres_per_year['SURVEY YEAR'].astype(int)

        # Include missing years with 0 acres
        all_years = pd.DataFrame({'SURVEY YEAR': range(1989, 2000)})
        acres_per_year = all_years.merge(acres_per_year, on='SURVEY YEAR', how='left').fillna(0)

        # Prepare series for LinePlot
        series_data = [
            {
                'name': 'Total WRLU Acres',
                'color': '#1f77b4',
                'marker': {'enabled': True},
                'data': [[row['SURVEY YEAR'], row['ACRES']] for _, row in acres_per_year.iterrows()]
            }
        ]

        # Create the LinePlot
        wrlu_plot = LinePlot(
            height='400px',
            width='100%',
            engine='highcharts',
            title='Total Water-Related Land Use (WRLU) Area in Utah',
            subtitle='Acres per Year (1989–1999)',
            spline=True,
            x_axis_title='Year',
            y_axis_title='Total Acres',
            x_axis_units='year',
            y_axis_units='acres',
            series=series_data
        )
    except Exception as e:
        print("❌ Error fetching or processing CSV:", e)
        # Fallback dummy plot if something goes wrong
        wrlu_plot = LinePlot(
            height='400px',
            width='100%',
            engine='highcharts',
            title='Total Water-Related Land Use (WRLU) Area in Utah',
            subtitle='Data not available',
            series=[{'name': 'No Data', 'color': '#ff0000', 'data': []}]
        )

    ########### Plot Portion End ###########

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