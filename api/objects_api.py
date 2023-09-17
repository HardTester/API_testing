from api import routes


def get_objects(client, *ids):
    return client.get(routes.Routes.OBJECTS, params={'id': ids} if ids else None)


def get_object(client, obj_id):
    return client.get(routes.Routes.OBJECTS_ITEM.format(obj_id))


def post_object(client, **kwargs):
    return client.post(routes.Routes.OBJECTS, **kwargs)


def put_object(client, obj_id, **kwargs):
    return client.put(routes.Routes.OBJECTS_ITEM.format(obj_id), **kwargs)


def delete_object(client, obj_id):
    return client.delete(routes.Routes.OBJECTS_ITEM.format(obj_id))
