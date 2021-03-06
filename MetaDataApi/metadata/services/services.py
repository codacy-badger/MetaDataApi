import json
from django import forms

from service_objects.services import Service

from MetaDataApi.metadata.services import *

from MetaDataApi.metadata.models import *
from django.contrib.auth.models import User

from MetaDataApi.dataproviders.models import ThirdPartyDataProvider

from MetaDataApi.dataproviders.services.data_provider_etl_service import DataProviderEtlService


class DeleteSchemaService(Service):
    schema_label = forms.CharField()

    def process(self):
        schema_label = self.cleaned_data['schema_label']

        if schema_label == "all":
            schemas = Schema.objects.all()
            [schema.delete() for schema in schemas]

            try:
                media_schema_folder = os.path.join(MEDIA_ROOT, "schemas")
                # delete all files in media/schemas folder
                shutil.rmtree(media_schema_folder)
                os.makedirs(media_schema_folder)
            except:
                print("does not work on AWS, and neither needed")
        else:
            schema = Schema.objects.get(label=schema_label)
            schema.delete()


class ExportSchemaService(Service):
    schema_label = forms.CharField()

    def process(self):
        schema_label = self.cleaned_data['schema_label']

        service = RdfSchemaService()

        schema = service._try_get_item(Schema(label=schema_label))

        service.export_schema_from_db(schema)

        schema_file_url = schema.rdfs_file.url
        return schema_file_url


class IdentifySchemaFromFileService(Service):
    file = forms.FileField(required=False)
    schema_label = forms.CharField()
    data_label = forms.CharField(required=False)

    def process(self):
        file = next(self.files.values())
        schema_label = self.cleaned_data['schema_label']
        data_label = self.cleaned_data['data_label']

        identify = SchemaIdentificationV2()

        data = json.loads(file.read())

        data_label = data_label or identify.standardize_string(
            file.name, remove_version=True)

        # here we have no idea about the origin if not specified
        # TODO: consider if its better to do something else
        schema = identify._try_get_item(Schema(label=schema_label))
        if not schema:
            schema = identify.create_new_empty_schema(schema_label)

        objects = identify.identify_schema_from_dataV2(
            data, schema, data_label)

        return objects


class IdentifyDataFromFileService(Service):
    schema_label = forms.CharField()
    file = forms.FileField(required=False)
    data_label = forms.CharField(required=False)
    user_pk = forms.IntegerField()

    def process(self):
        file = next(self.files.values())
        schema_label = self.cleaned_data['schema_label']
        data_label = self.cleaned_data['data_label']
        user_pk = self.cleaned_data['user_pk']
        user = User.objects.get(pk=user_pk)

        identify = SchemaIdentificationV2()

        data = json.loads(file.read())

        data_label = data_label or identify.standardize_string(
            file.name, remove_version=True)

        # here we have no idea about the origin if not specified
        # TODO: consider if its better to do something else
        schema = identify._try_get_item(Schema(label=schema_label))

        objects = identify.map_data_to_native_instances(
            data, schema, data_label)

        return objects


class IdentifySchemaFromProviderService(Service):
    provider_name = forms.CharField()
    endpoint = forms.CharField()
    user_pk = forms.IntegerField()

    def process(self):
        provider_name = self.cleaned_data['provider_name']
        endpoint = self.cleaned_data['endpoint']
        user_pk = self.cleaned_data['user_pk']
        user = User.objects.get(pk=user_pk)

        identify = SchemaIdentificationV2()
        provider_service = DataProviderEtlService(provider_name)

        provider_profile = user.profile.get_data_provider_profile(
            provider_name)

        schema = provider_service.get_related_schema()

        if endpoint == "all" or endpoint is None:
            endpoints = json.loads(
                provider_service.dataprovider.rest_endpoints_list)
        else:
            endpoints = [endpoint, ]
        n_objs = 0
        for endpoint in endpoints:
            data = provider_service.read_data_from_endpoint(
                endpoint, provider_profile.access_token)

            parrent_label = identify.rest_endpoint_to_label(endpoint)

            objects = identify.identify_schema_from_dataV2(
                data, schema, parrent_label)
            n_objs += len(objects)

        return n_objs


class IdentifyDataFromProviderService(Service):
    provider_name = forms.CharField()
    endpoint = forms.CharField()
    user_pk = forms.IntegerField()

    def process(self):
        provider_name = self.cleaned_data['provider_name']
        endpoint = self.cleaned_data['endpoint']
        user_pk = self.cleaned_data['user_pk']
        user = User.objects.get(pk=user_pk)

        identify = SchemaIdentificationV2()
        provider_service = DataProviderEtlService(provider_name)
        rdf_service = RdfInstanceService()

        provider_profile = user.profile.get_data_provider_profile(
            provider_name)

        schema = rdf_service._try_get_item(Schema(label=provider_name))

        # select which endpoints
        if endpoint == "all" or endpoint is None:
            endpoints = json.loads(
                provider_service.dataprovider.rest_endpoints_list)
        else:
            endpoints = [endpoint, ]

        # identify objects for each endpoint
        object_list = []
        for endpoint in endpoints:
            data = provider_service.read_data_from_endpoint(
                endpoint, provider_profile.access_token)

            parrent_label = identify.rest_endpoint_to_label(endpoint)

            objects = identify.map_data_to_native_instances(
                data, schema, parrent_label)
            object_list.extend(objects)

        # generate rdf file from data
        rdf_file = rdf_service.export_instances_to_rdf_file(
            schema, objects)

        return rdf_file, object_list


class IdentifySchemaAndDataFromProviderService(Service):
    provider_name = forms.CharField()
    endpoint = forms.CharField()
    user_pk = forms.IntegerField()

    def process(self):
        provider_name = self.cleaned_data['provider_name']
        endpoint = self.cleaned_data['endpoint']
        user_pk = self.cleaned_data['user_pk']
        user = User.objects.get(pk=user_pk)

        identify = SchemaIdentificationV2()
        provider_service = DataProviderEtlService(provider_name)
        rdf_service = RdfInstanceService()

        provider_profile = user.profile.get_data_provider_profile(
            provider_name)

        schema = rdf_service._try_get_item(Schema(label=provider_name))
        if not schema:
            schema = rdf_service.create_new_empty_schema(provider_name)

        # select which endpoints
        if endpoint == "all" or endpoint is None:
            endpoints = json.loads(
                provider_service.dataprovider.rest_endpoints_list)
        else:
            endpoints = [endpoint, ]

        # identify objects for each endpoint
        object_list = []
        for endpoint in endpoints:
            data = provider_service.read_data_from_endpoint(
                endpoint, provider_profile.access_token)

            parrent_label = identify.rest_endpoint_to_label(endpoint)

            objects = identify.identify_from_json_data(
                data, schema, user, parrent_label)
            object_list.extend(objects)

        # generate rdf file from data
        rdf_file = rdf_service.export_instances_to_rdf_file(
            schema, objects)

        return rdf_file, object_list


class AddJsonSchemaService(Service):
    url = forms.CharField()
    schema_label = forms.CharField()
    user_pk = forms.IntegerField()

    def process(self):
        url = self.cleaned_data['url']
        schema_label = self.cleaned_data['schema_label']
        user_pk = self.cleaned_data['user_pk']
        user = User.objects.get(pk=user_pk)

        service = JsonSchemaService()
        if url == "open_m_health":
            try:
                service.write_to_db_baseschema()
                # import threading

                # task = service.write_to_db_baseschema
                # thr = threading.Thread(target=task)
                # thr.start()  # Will run

            except Exception as e:
                raise GraphQLError(e)
        elif url == "open_m_health_sample":
            service.write_to_db_baseschema(sample=True)
        else:
            try:
                service.write_to_db(url, name)
            except Exception as e:
                raise GraphQLError(str(e))

        return service.touched_meta_items, service._error_list


class AddRdfSchemaService(Service):
    url = forms.CharField()

    def process(self):
        url = self.cleaned_data['url']

        service = RdfSchemaService()
        if url == "baseschema":
            try:
                service.write_to_db_baseschema()
            except Exception as e:
                raise GraphQLError(str(e))
        else:
            try:
                service.write_to_db(url)
            except Exception as e:
                raise GraphQLError(str(e))


class AddPersonReferenceToBaseObjects(Service):
    schema_label = forms.CharField()

    def process(self):
        schema_label = self.cleaned_data['schema_label']

        service = DataCleaningService()

        schema = service._try_get_item(Schema(label=schema_label))

        try:
            objects = service.relate_root_classes_to_foaf(schema)
        except Exception as e:
            raise GraphQLError(str(e))

        return objects


class GetTemporalFloatPairsService(Service):
    schema_label = forms.CharField()
    object_label = forms.CharField()
    attribute_label = forms.CharField()
    datetime_label = forms.CharField(required=False)
    datetime_object_label = forms.CharField(required=False)

    def process(self):
        schema_label = self.cleaned_data['schema_label']
        object_label = self.cleaned_data['object_label']
        attribute_label = self.cleaned_data['attribute_label']
        datetime_label = self.cleaned_data['datetime_label']
        datetime_object_label = self.cleaned_data['datetime_object_label']

        value_att = Attribute.objects.get(
            label=attribute_label,
            object__label=object_label,
            object__schema__label=schema_label)

        Attribute.assert_data_type(value_att, float)

        if datetime_label:
            datetime_att = Attribute.objects.get(
                label=datetime_label,
                object__label=datetime_object_label or object_label,
                object__schema__label=schema_label
            )
            Attribute.assert_data_type(datetime_att, datetime)

        else:
            raise NotImplementedError(
                "identify not implemented, specify a secondary label")
            datetime_att = identify()

        service = BaseMetaDataService()
        data = service.get_connected_attribute_pairs(value_att, datetime_att)

        # data_values = [(att_inst1.value, att_inst2.value)
        #                for att_inst1, att_inst2 in data]

        return data
