OBJECTS = '/objects'
OBJECTS_ITEM = '/objects/{}'


def get_objects(client, ids=None):
    return client.get(OBJECTS, params=ids)


def post_object(client, obj):
    return client.post(OBJECTS, json=obj)


def put_object(client, obj_id, obj):
    return client.put(OBJECTS_ITEM.format(obj_id), json=obj)


def delete_object(client, obj_id):
    return client.delete(OBJECTS_ITEM.format(obj_id))
