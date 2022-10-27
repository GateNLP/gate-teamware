import logging
import json
from datetime import datetime
from django.db import models
from django.db.models import Model, ManyToOneRel, ManyToManyRel, ForeignKey

from django.utils import timezone

from backend.models import Project

log = logging.getLogger(__name__)


def dsl_val(attr_name, obj, data):
    """
    Insert value of `data` with key `attr_name` into the object `obj` with attribute name `attr_name`
    """
    if attr_name in data:
        setattr(obj, attr_name, data[attr_name])


def dsl_json(attr_name, obj, data):
    """
    Convert value of `data` with key `attr_name` into a JSON string and insert into the
    object `obj` with attribute name `attr_name`
    """
    if attr_name in data:
        setattr(obj, attr_name, json.dumps(data[attr_name]))


def dsl_date(attr_name, obj, data):
    """
    Convert value of `data` with key `attr_name` into a datetime object and insert into the
    object `obj` with attribute name `attr_name`
    """
    if attr_name in data:
        if data[attr_name] is None:
            setattr(obj, attr_name, None)
        elif isinstance(data[attr_name], str):
            setattr(obj, attr_name, datetime.fromisoformat(data[attr_name]))
        elif isinstance(data[attr_name], datetime):
            setattr(obj, attr_name, data[attr_name])
        else:
            raise ValueError("Date must be None, str or datetime object")


class FieldSerializer:

    def serialize(self, model_obj, field):
        return getattr(model_obj, field.name)

    def deserialize(self, model_obj, val_input, field):
        setattr(model_obj, field.name, val_input)


class ForeignKeySerializer(FieldSerializer):

    def serialize(self, model_obj, field):
        related_obj = getattr(model_obj, field.name)
        if not related_obj:
            return None

        return related_obj.id

    def deserialize(self, model_obj, val_input, field):
        rel_obj = None
        if val_input:
            rel_obj = field.related_model.objects.get(pk=val_input)
        setattr(model_obj, field.name, rel_obj)


class RelationSerializer(FieldSerializer):

    def serialize(self, model_obj, field):
        relation_objs = getattr(model_obj, field.name).all().values_list('id', flat=True)
        return [rel_obj for rel_obj in relation_objs]

    def deserialize(self, model_obj, val_input, field):
        pass # TODO ? Might be better to manage these relations in a separate field


class ModelSerializer:

    def __init__(self):
        """
        field_serializer:dict Use special serializer (subclass of FieldSerializer) for the specified field name e.g. {"my_json_field": JSONFieldSerializer}
        field_relation_spec:dict Serialize one-to-many or many-to-many relations. The spec allows declarations of
        fields in the related object to serialize e.g.
        {
            "my_relation_field": {
                                    "field": {"id", "name", ...}
                                }
        }

        """
        self._field_serializer = FieldSerializer()
        self._relation_serializer = RelationSerializer()
        self._foreign_key_serializer = ForeignKeySerializer()
        self.field_serializers = {}
        self.field_relation_spec = {}
        self.serializer_dict = {
            ManyToManyRel: self._relation_serializer,
            ManyToOneRel: self._relation_serializer,
            ForeignKey: self._foreign_key_serializer
        }

    def serialize(self, model_obj: Model, select_fields: set = None, exclude_fields: set = None):

        if not model_obj or not isinstance(model_obj, Model):
            raise ValueError("Must provide an instance of a Model to serialize")

        output = {}

        fields_to_serialize = self.get_field_names_to_serialize(model_obj, select_fields, exclude_fields)

        # Value fields, foreign keys and fields with serializers
        for field in model_obj.__class__._meta.get_fields():
            if field.name in fields_to_serialize:
                output[field.name] = self.serialize_field(model_obj, field)

        return output

    def get_field_names_to_serialize(self, model_obj: Model, select_fields: set, exclude_fields: set):
        fields_to_serialize = select_fields
        if not fields_to_serialize or len(fields_to_serialize) < 1:
            fields_to_serialize = set()
            for field in model_obj.__class__._meta.get_fields():
                fields_to_serialize.add(field.name)
        if exclude_fields:
            for exclude_name in exclude_fields:
                fields_to_serialize.remove(exclude_name)

        return fields_to_serialize

    def serialize_field(self, model_obj: Model, field):
        field_serializer = self.get_field_serializer(field)
        return field_serializer.serialize(model_obj, field)

    def get_field_serializer(self, django_field):
        if django_field.__class__ in self.serializer_dict:
            return self.serializer_dict[django_field.__class__]
        else:
            return FieldSerializer()

    def deserialize(self, model_class, input_dict, select_fields: set = None, exclude_fields: set = None):

        if not issubclass(model_class, Model):
            raise ValueError(f"{model_class} must be subclass of django Model")

        model_obj = model_class.objects.get(pk=input_dict["id"])
        if not model_obj:
            raise ValueError(f"No object with id {input_dict['id']}")

        fields_to_serialize = self.get_field_names_to_serialize(model_obj, select_fields, exclude_fields)

        # Value fields, foreign keys and fields with serializers
        for field in model_obj.__class__._meta.get_fields():
            if field.name in fields_to_serialize and field.name in input_dict:
                self.deserialize_field(model_obj, input_dict[field.name], field)

        model_obj.save()
        return model_obj

    def deserialize_field(self, model_obj, input_field, field):
        field_serializer = self.get_field_serializer(field)
        return field_serializer.deserialize(model_obj, input_field, field)

