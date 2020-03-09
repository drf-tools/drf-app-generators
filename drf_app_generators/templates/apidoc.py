__all__ = ['APIDOC_VIEW']

APIDOC_VIEW = """# {{ resource.name|capfirst }} APIs
## GET /api/v1/{{ resource.name }}/
-----------------------------------
Get a list of {{ resource.name }}
### Request Parameters
| Fields   | Description            |
|----------|------------------------|
| limit    | How many records should the API return |
| offset   | Which position of the record set should be queried |

#### Example
##### Request
```
curl -X GET \\
    http://localhost:8000/api/v1/{{ resource.name }}/?limit=20&offset=0 \\
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

## POST /api/v1/{{ resource.name }}/
-----------------------------------
Create new {{ resource.name }}
### Request Parameters
None

### Request Body
```
```

#### Example
##### Request
```
curl -X POST \\
    http://localhost:8000/api/v1/{{ resource.name }}/?limit=20&offset=0 \\
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

## PUT /api/v1/{{ resource.name }}/:id/
-----------------------------------
Update {{ resource.name }} record by ID
### Request Parameters
None

### Request Body
```
```

#### Example
##### Request
```
curl -X POST \
    http://localhost:8000/api/v1/{{ resource.name }}/1/?limit=20&offset=0 \\
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

## DELETE /api/v1/{{ resource.name }}/:id/
----------------------------------------------
Remove {{ resource.name }} record by ID
### Request Parameters
None

### Request Body
None

#### Example
##### Request
```
curl -X POST \\
    http://localhost:8000/api/v1/{{ resource.name }}/1/?limit=20&offset=0 \\
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