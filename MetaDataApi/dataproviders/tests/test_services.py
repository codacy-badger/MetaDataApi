import django
from django.test import TestCase, TransactionTestCase
from urllib import request
from MetaDataApi.metadata.models import Object
from django.core.management import call_command
from datetime import datetime

from MetaDataApi.metadata.services import GetTemporalFloatPairsService
from MetaDataApi.metadata.tests.data import LoadTestData


class TestSomeService(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestSomeService, cls).setUpClass()
        django.setup()

    def test_some(self):

        LoadTestData.init_strava_schema_from_file()
        LoadTestData.init_strava_data_from_file()

        args = {
            "schema_label": "strava",
            "object_label": "activities",
            "attribute_label": "distance",
            "datetime_label": "name",
            "datetime_object_label": "activities",
        }

        data = GetTemporalFloatPairsService.execute(args)

        expected = []

        self.assertListEqual(data, expected)
