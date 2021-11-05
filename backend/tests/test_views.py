from django.test import TestCase
from backend.views import DownloadAnnotations

class TestDownloadAnnotations(TestCase):

    def test_csv_generation(self):
        v = DownloadAnnotations()
        key = ["one", "two", "four"]
        key2 = ["two", "three"]
        key3 = []
        obj = {
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
        }
        output_keys = v.insert_missing_key(key, obj)
        print(key)
        print(output_keys)

        print(v.insert_missing_key(key2, obj))
        print(v.insert_missing_key(key3, obj))
