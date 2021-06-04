from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.utils import timezone

from backend.models import Project, Document
from backend.utils.serialize import ModelSerializer


class TestProjectModel(TestCase):
    def test_saving_and_loading(self):

        name = "Test name"
        created_at = timezone.now()
        data = {
            "entry1": "val1",
            "entry2": "val2"
        }

        proj = Project(name=name, created_at=created_at, configuration=data)
        proj.save()

        loaded_proj = Project.objects.get(pk=1)
        self.assertEqual(loaded_proj.name, name)
        self.assertEqual(loaded_proj.created, created_at)
        proj_data = loaded_proj.configuration
        self.assertEqual(proj_data["entry1"], data["entry1"])
        self.assertEqual(proj_data["entry2"], data["entry2"])

    def test_serializing(self):

        user1 = get_user_model().objects.create(username="user1")
        user2 = get_user_model().objects.create(username="user2")

        name = "Test name"
        created_at = timezone.now()
        data = {
            "entry1": "val1",
            "entry2": "val2"
        }
        proj = Project(name=name, created_at=created_at, configuration=data)
        proj.save()

        # One document
        document = Document.objects.create(project=proj)
        document.project = proj
        document.save()

        # Two document
        document2 = Document.objects.create(project=proj)

        # User 1 as owner
        user1.owns.add(proj)
        user1.save()

        # User 2 as manager
        user2.manages.add(proj)

        # Load a fresh project model to serialize
        proj = Project.objects.get(pk=1)

        serializer = ModelSerializer()
        serialized_proj = serializer.serialize(proj)

        self.assertEqual(serialized_proj["name"], proj.name)
        self.assertEqual(serialized_proj["configuration"], proj.configuration)
        self.assertEqual(serialized_proj["owner"], user1.id)
        self.assertEqual(serialized_proj["managers"], [user2.id])
        self.assertEqual(serialized_proj["documents"], [document.id, document2.id])




    def test_deserialize(self):
        name = "Test name"
        created_at = timezone.now()
        data = {
            "entry1": "val1",
            "entry2": "val2"
        }


        user1 = get_user_model().objects.create(username="user1")
        user2 = get_user_model().objects.create(username="user2")
        proj = Project()
        proj.save()

        input_dict = {
            "id": proj.id,
            "name": name,
            "created_at": created_at,
            "data": data,
            "owner": user1.id
        }

        serializer = ModelSerializer()
        deserialized_obj = serializer.deserialize(Project, input_dict)

        self.assertEqual(input_dict["name"], deserialized_obj.name)
        self.assertEqual(input_dict["owner"], deserialized_obj.owner.id)











