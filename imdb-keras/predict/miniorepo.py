from minio import Minio


client = Minio('localhost:9000',
                  access_key='fedn_admin',
                  secret_key='password',
                  secure=False )


def get_global_model(model_id, bucket=''):

    if bucket == '':
        bucket = 'fedn-models'

    try:
        data = client.get_object(bucket, model_id)
        return data.read()
    except Exception as e:
        raise Exception("Could not fetch data from bucket, {}".format(e))


def get_global_model_list(bucket=''):
    objects_list = []
    if bucket == '':
        bucket = 'fedn-models'

    try:
        objects = client.list_objects(bucket)
        for obj in objects:
            objects_list.append(obj.object_name)
        return objects_list

    except Exception as e:
        raise Exception("Could not fetch object list from bucket, {}".format(e))