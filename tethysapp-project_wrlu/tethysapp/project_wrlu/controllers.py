from tethys_sdk.routing import controller
from tethys_sdk.gizmos import Button, MapView, Layer
from .app import App
import boto3
from botocore.exceptions import NoCredentialsError

@controller
def home(request):
    """
    Controller for the app home page.
    """
    # Buttons (your existing code)
    save_button = Button(display_text='', name='save-button', icon='save', style='success')
    edit_button = Button(display_text='', name='edit-button', icon='pen', style='warning')
    remove_button = Button(display_text='', name='remove-button', icon='trash', style='danger')
    previous_button = Button(display_text='Previous', name='previous-button')
    next_button = Button(display_text='Next', name='next-button')

    s3_client = boto3.client('s3')

    try:
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                
            },
            ExpiresIn=3600  # 1 hour
        )
    except NoCredentialsError:
        presigned_url = None

    map_layer = Layer(
        source=presigned_url,
        layer_options={'style': {'color': 'blue', 'weight': 2, 'fillOpacity': 0.5}},
        legend_title='WRLU 1989–1999'
    )

    # Create MapView
    my_map = MapView(
        height='400px',
        width='100%',
        layers=[map_layer],
        controls=['ZoomSlider', 'FullScreen'],
        attribution='Data: S3 GeoJSON'
    )

    context = {
        'save_button': save_button,
        'edit_button': edit_button,
        'remove_button': remove_button,
        'previous_button': previous_button,
        'next_button': next_button,
        'my_map': my_map
    }

    return App.render(request, 'home.html', context)