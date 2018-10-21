import django
from django.test import TestCase, TransactionTestCase
from urllib import request
from MetaDataApi.metadata.models import Object
from django.core.management import call_command
from MetaDataApi.metadata.services.data_cleaning_service import (
    DataCleaningService
)


class TestSchemaIdentificationService(TransactionTestCase):
    """Tests for the application views."""
    # fixtures = [
    #     'metadata/fixtures/new_load.json',
    # ]

    # Django requires an explicit setup() when running tests in PTVS
    @classmethod
    def setUpClass(cls):
        super(TestSchemaIdentificationService, cls).setUpClass()
        django.setup()

        # call_command(
        #     'loaddata',
        #     'metadata/fixtures/new_load.json',
        #     verbosity=0
        # )
        # call_command('loaddata', 'fixtures/testdb.json', verbosity=1)

        # populate the database
        from MetaDataApi.metadata.services.rdfs_service import RdfService
        from MetaDataApi.metadata.services.json_schema_service import (
            JsonSchemaService
        )

        rdf_service = RdfService()

        # just take foaf
        rdf_service.write_to_db(rdf_url="http://xmlns.com/foaf/0.1/")

        json_service = JsonSchemaService()

        # this takes to long time if doing full
        json_service.write_to_db_baseschema(positive_list=[
            "body-temperature-2.0.json",
            "body-temperature-2.x.json",
        ])

        dc_service = DataCleaningService()

        dc_service.relate_root_classes_to_foaf("open_m_health")

    def test_identify_json_data_sample(self):
        from MetaDataApi.metadata.services.schema_identification import (
            SchemaIdentification)

        from MetaDataApi.metadata.models import Schema, Object

        url = "https://raw.githubusercontent.com/Grusinator/MetaDataApi" + \
            "/master/schemas/json/omh/test_data/body-temperature/2.0/" + \
            "shouldPass/valid-temperature.json"

        Schema.objects.get(label="open_m_health")

        obj_count = Object.objects.all().count()
        # make sure that the number of objects is larger than
        if obj_count < 10:
            raise AssertionError("database not populated")

        with request.urlopen(url) as resp:
            text = resp.read().decode()

        service = SchemaIdentification()

        resp = service.identify_data(url)

        self.assertEqual(1 + 1, 2)
