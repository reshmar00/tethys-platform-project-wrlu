from tethys_sdk.base import TethysAppBase
from tethys_sdk.app_settings import CustomSetting

class App(TethysAppBase):
    """
    Tethys app class for WRLU.
    """
    name = 'WRLU'
    description = 'Water Related Land Use in Utah'
    package = 'project_wrlu'  # WARNING: Do not change this value
    index = 'home'
    icon = f'{package}/images/icon.gif'
    root_url = 'project-wrlu'
    color = '#00e6e6'
    tags = '"app","hydrology","water use"'
    enable_feedback = False
    feedback_emails = []

    def custom_settings(self):
            """
            Example custom_settings method.
            """
            custom_settings = (
                CustomSetting(
                    name='max_dams',
                    type=CustomSetting.TYPE_INTEGER,
                    description='Maximum number of dams that can be created in the app.',
                    required=False
                ),
            )
            return custom_settings