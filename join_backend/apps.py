from django.apps import AppConfig

"""
JoinBackendConfig:

Configures the join_backend application settings, 
specifying the default field type for auto-incrementing primary keys and defining the application’s name within the Django project.
"""


class JoinBackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'join_backend'
