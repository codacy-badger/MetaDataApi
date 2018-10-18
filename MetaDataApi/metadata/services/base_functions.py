import os
import re
import inflection
# from jsonschema import validate
from urllib import request
from MetaDataApi.metadata.models import (
    Schema, Object, Attribute, ObjectRelation)

from schemas.json.omh.schema_names import schema_names
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist


class BaseMetaDataService():

    def __init__(self):
        self.schema = None
        self.baseurl = None

        self._objects_created_list = []
        self._error_list = []
        self.overwrite_db_objects = False

    def standardize_string(self, string, remove_version=False):
        string = inflection.underscore(str(string))

        string = string.replace(" ", "_")
        # remove any version numbers
        if remove_version:
            string = re.sub(
                "(|_version|_v|_v.)(|_)\d+\.(\d+|x)(|_)", '', string)

        string = re.sub("(|_)vocabulary(|_)", '', string)

        # remove trailing and leading whitespace/underscore
        # string = re.sub('/^[\W_]+|[\W_]+$/', '', string)

        return string

    def _try_get_item(self, item_type, label):
        try:
            # this "with transaction.atomic():"
            # is used to make tests run due to some
            # random error, atomic something.
            # it works fine when runs normally
            with transaction.atomic():
                return_item = item_type.objects.get(label=label)

        except ObjectDoesNotExist as e:
            # try create object

    def _try_create_item(self, item, update=False):

        item_type = type(item)
        remove_version = not isinstance(item_type, Schema)

        # test if exists
        item.label = self.standardize_string(
            item.label, remove_version=remove_version)
        try:
            # this "with transaction.atomic():"
            # is used to make tests run due to some
            # random error, atomic something.
            # it works fine when runs normally
            with transaction.atomic():
                return_item = item_type.objects.get(label=item.label)
                if update or self.overwrite_db_objects:
                    return_item.delete()
                    item.save()
                    # on update add to debug list
                    self._objects_created_list.append(item)
                    return_item = item

            return return_item

        except ObjectDoesNotExist as e:
            # try create object
            try:
                item.save()
                self._objects_created_list.append(item)
                return item
            except Exception as e:
                self._error_list.append(str(e))
                return None

        except (transaction.TransactionManagementError,) as e:
            return None
        except Exception as e:
            return None
