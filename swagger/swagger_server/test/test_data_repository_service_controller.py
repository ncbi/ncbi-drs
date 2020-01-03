# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.access_url import AccessURL  # noqa: E501
from swagger_server.models.drs_object import DrsObject  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDataRepositoryServiceController(BaseTestCase):
    """DataRepositoryServiceController integration test stubs"""

    def test_get_access_url(self):
        """Test case for get_access_url

        Get a URL for fetching bytes.
        """
        response = self.client.open(
            '/ga4gh/drs/v1/objects/{object_id}/access/{access_id}'.format(object_id='object_id_example', access_id='access_id_example'),
            method='GET',
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_object(self):
        """Test case for get_object

        Get info about a `DrsObject`.
        """
        query_string = [('expand', false)]
        response = self.client.open(
            '/ga4gh/drs/v1/objects/{object_id}'.format(object_id='object_id_example'),
            method='GET',
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
