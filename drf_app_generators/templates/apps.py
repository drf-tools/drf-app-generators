__all__ = ['APP_VIEW']

APP_VIEW = """from core import apps


class {{ app|capfirst }}Config(apps.BaseConfig):
    name = '{{ app }}'
"""
