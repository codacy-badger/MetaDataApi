from MetaDataApi.metadata.tests.data import LoadTestData
from django.test import TestCase, TransactionTestCase
import django

from MetaDataApi.metadata.tests import UtilsForTesting
from MetaDataApi.metadata.utils.django_model_utils import BuildSearchArgsFromJson


class TestBuildSearchArgsFromJson(TransactionTestCase):

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestBuildSearchArgsFromJson, cls).setUpClass()
        # django.setup()

    def test_build_search_args_from_json(self):

        #data = UtilsForTesting.loadStravaActivities()

        data = {
            "object1": {
                "Attribute1": 3,
                "Attribute2": {"value": "att2value"},
                "object2": {
                    "attribute3": True,
                    "attribute4": 5.04
                }
            }
        }

        builder = BuildSearchArgsFromJson()
        args = builder.build(data)

        expected = {
            'from_relations__from_object__label': 'object1',
            'from_relations__from_object__from_relations__from_object__label__in':
                ['Attribute1',
                 'Attribute2',
                 'object2'],
            'from_relations__from_object__from_relations__from_object__from_relations__from_object__label__in':
                ['attribute3',
                 'attribute4']
        }

        self.assertEqual(args, expected)
