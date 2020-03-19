# DRF Application Generators
Generate DRF standard apps with a single command.

## Installation
Install with pip

```bash
$ pip install drf-app-generators
```

To use DRF app generators, add it to INSTALLED_APPS.

```code-block:: python
INSTALLED_APPS = (
    ...
    'rest_framework',
    'drf_app_generators',
    ...
)
```

## Usage

### Generate a new Django app.
To use the generators, run the following command.

```bash
$ python manage.py generate {app} {options}
```

| Options                 | Description                                                               |
|-------------------------|---------------------------------------------------------------------------|
|`--models`               | A list of model names.                                                    |
|`--apidoc`               | Generate written API document                                             |
|`--nested`               | Create nested folders for models, apis, factories and serializers         |
|`--force`                | Override existed files                                                    |


Example: Generate a new app with 3 models.
```bash
$ python manage.py generate books --models Book,Author,Label
```

```bash
    src/books/
    ├── __init__.py
    ├── admin.py
    ├── apis.py
    ├── apps.py
    ├── factories.py
    ├── filters.py
    ├── migrations
    │   ├── 0001_initial.py
    │   └── __init__.py
    ├── models.py
    ├── permissions.py
    ├── serializers.py
    └── tests
        ├── __init__.py
        ├── test_books_apis.py
        └── test_books_models.py
```

### Update an existing Django app.
When you finished adding fields to your models, you can update factories & admins by the following commands.

```bash
$ python manage.py app_update {app} {options}
```
| Options | Description             |
|---------|-------------------------|
|`--nested`| If you app is nested   |
| `--factory`| Update your factories. |
| `--api`| Update your APIs. |
| `--admin`| Update your admin. |
| `--serializer`| Update your serializers. |
| `--unittest`| Update your unittest. |
| `--filter`| Update your filters. |
| `--all`| Update all components. |
| `--add-models`| Add more models to your app. |

Example: Update books app we just generated.
```bash
python manage.py app_update books \
    --factory \
    --admin \
    --api \
    --serializer \
    --unittest \
    --filter \
    --add-models Label,Category
```

## Tests
A full application built with drf-generators can be found in the tests directory.

## License
MIT License. See [LICENSE](https://github.com/drf-tools/drf-app-generators/blob/master/LICENSE).
