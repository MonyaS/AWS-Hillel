import json
from datetime import datetime

from utils import decimalencoder


def deserialize_item(item):
    """

    :param item: {
        "id": str,
        "text": str,
        "checked": bool,
        "createdAt": int,
        "updatedAt": int,
    }
    :return: {
        "id": str,
        "text": str,
        "checked": bool,
        "createdAt": str,
        "updatedAt": str,
    }
    """
    item['createdAt'] = datetime.fromtimestamp(int(item['createdAt']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
    item['updatedAt'] = datetime.fromtimestamp(int(item['updatedAt']) / 1000).strftime('%Y-%m-%d %H:%M:%S')

    return json.dumps(item, cls=decimalencoder.DecimalEncoder)
