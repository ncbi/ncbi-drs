import connexion
import six

from swagger_server.models.access_url import AccessURL  # noqa: E501
from swagger_server.models.drs_object import DrsObject  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server import util


def get_access_url(object_id, access_id):  # noqa: E501
    """Get a URL for fetching bytes.

    Returns a URL that can be used to fetch the bytes of a &#x60;DrsObject&#x60;.  This method only needs to be called when using an &#x60;AccessMethod&#x60; that contains an &#x60;access_id&#x60; (e.g., for servers that use signed URLs for fetching object bytes). # noqa: E501

    :param object_id: An &#x60;id&#x60; of a &#x60;DrsObject&#x60;
    :type object_id: str
    :param access_id: An &#x60;access_id&#x60; from the &#x60;access_methods&#x60; list of a &#x60;DrsObject&#x60;
    :type access_id: str

    :rtype: AccessURL
    """
    return 'do some magic!'


def get_object(object_id, expand=None):  # noqa: E501
    """Get info about a &#x60;DrsObject&#x60;.

    Returns object metadata, and a list of access methods that can be used to fetch object bytes. # noqa: E501

    :param object_id: 
    :type object_id: str
    :param expand: If false and the object_id refers to a bundle, then the ContentsObject array contains only those objects directly contained in the bundle. That is, if the bundle contains other bundles, those other bundles are not recursively included in the result. If true and the object_id refers to a bundle, then the entire set of objects in the bundle is expanded. That is, if the bundle contains aother bundles, then those other bundles are recursively expanded and included in the result. Recursion continues through the entire sub-tree of the bundle. If the object_id refers to a blob, then the query parameter is ignored.
    :type expand: bool

    :rtype: DrsObject
    """
    return 'do some magic!'
