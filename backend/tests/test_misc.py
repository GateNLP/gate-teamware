from django.test import TestCase
from backend.utils.misc import get_value_from_key_path, insert_value_to_key_path

class InsertExtractValuesFromDictWithKeyPath(TestCase):

    def test_get_value_with_key_path(self):

        target_value = "Test value"

        test_dict = {
            "path1": {
                "path2": {
                    "path3": target_value
                }
            },
            "path_array1": [
                {
                    "path2": target_value
                }
            ]
        }

        # Get for normal path, should exist
        self.assertEqual(get_value_from_key_path(test_dict, "path1.path2.path3", "."), target_value)

        # Get for nonexistant path
        self.assertEqual(get_value_from_key_path(test_dict, "path1.dontexist", "."), None)

        # Get for path with array (not supported)
        self.assertEqual(get_value_from_key_path(test_dict, "path_array1.0.path2", "."), None)



    def test_insert_value_with_key_path(self):
        target_value = "Test value"

        test_dict = {
            "path1": {
                "path2": {

                }
            },
            "path_array1": [
                {
                    "path2": target_value
                }
            ]
        }

        # Insert into new path
        self.assertEqual(insert_value_to_key_path(test_dict, "newpath1.newpath2", target_value, "."), True)
        self.assertEqual(test_dict["newpath1"]["newpath2"], target_value)

        # Insert into existing path
        self.assertEqual(insert_value_to_key_path(test_dict, "path1.path2.path3", target_value, "."), True)
        self.assertEqual(test_dict["path1"]["path2"]["path3"], target_value)

        # Insert into path with array (not supported)
        self.assertEqual(insert_value_to_key_path(test_dict, "path_array1.path2.path3", target_value, "."), False)

