OBJECTS = '/objects'
OBJECTS_ITEM = '/objects/{}'


def get_objects(client, *ids):
    return client.get(OBJECTS, params={'id': ids} if ids else None)


def get_object(client, obj_id):
    return client.get(OBJECTS_ITEM.format(obj_id))


def post_object(client, **kwargs):
    return client.post(OBJECTS, **kwargs)


def put_object(client, obj_id, obj):
    return client.put(OBJECTS_ITEM.format(obj_id), json=obj)


def delete_object(client, obj_id):
    return client.delete(OBJECTS_ITEM.format(obj_id))
