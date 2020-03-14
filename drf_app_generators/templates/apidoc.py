__all__ = ['APIDOC_VIEW']

APIDOC_VIEW = """# {{ model_meta.verbose_name_plural|capfirst }} APIs
## GET /api/v1/{{ model_meta.verbose_name_plural }}/
-----------------------------------
Get a list of {{ model_meta.verbose_name_plural }}
### Request Parameters
| Fields   | Description            |
|----------|------------------------|
| limit    | How many records should the API return |
| offset   | Which position of the record set should be queried |

#### Example
##### Request
```
curl -X GET \\
    http://localhost:8000/api/v1/{{ model_meta.verbose_name_plural }}/?limit=20&offset=0 \\
    -H 'authorization: Basic YWRtaW46MTIzNDU2' \\
    -H 'cache-control: no-cache'
```

##### Response Body
```
```

#### Response Status Code
| Code  | Description      |
|-------|------------------|
| 200   | OK |

## POST /api/v1/{{ model_meta.verbose_name_plural }}/
-----------------------------------
Create new {{ model_meta.verbose_name_plural }}
### Request Parameters
None

### Request Body
```
```

#### Example
##### Request
```
curl -X POST \\
    http://localhost:8000/api/v1/{{ model_meta.verbose_name_plural }}/?limit=20&offset=0 \\
    -H 'authorization: Basic YWRtaW46MTIzNDU2' \\
    -H 'cache-control: no-cache' \\
    -H 'content-type: application/json' \\
    -d '{}'
```

##### Response Body
```
```

### Response Status Code
| Code  | Description      |
|-------|------------------|
| 201   | Created |

## PUT /api/v1/{{ model_meta.verbose_name_plural }}/:id/
-----------------------------------
Update {{ model_meta.verbose_name_plural }} record by ID
### Request Parameters
None

### Request Body
```
```

#### Example
##### Request
```
curl -X POST \
    http://localhost:8000/api/v1/{{ model_meta.verbose_name_plural }}/1/?limit=20&offset=0 \\
    -H 'authorization: Basic YWRtaW46MTIzNDU2' \\
    -H 'cache-control: no-cache' \\
    -H 'content-type: application/json' \\
    -d '{}'
```

##### Response Body
```
```

### Response Status Code
| Code  | Description      |
|-------|------------------|
| 200   | OK |

## DELETE /api/v1/{{ model_meta.verbose_name_plural }}/:id/
----------------------------------------------
Remove {{ model_meta.verbose_name_plural }} record by ID
### Request Parameters
None

### Request Body
None

#### Example
##### Request
```
curl -X POST \\
    http://localhost:8000/api/v1/{{ model_meta.verbose_name_plural }}/1/?limit=20&offset=0 \\
    -H 'authorization: Basic YWRtaW46MTIzNDU2' \\
    -H 'cache-control: no-cache'
```

##### Response Body
No content

### Response Status Code
| Code  | Description      |
|-------|------------------|
| 204   | DELETED |
"""