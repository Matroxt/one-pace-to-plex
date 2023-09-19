import os, sys
import json
import unittest
from unittest.mock import patch, MagicMock, call

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)  # look in parent directory for python files

import rename

class TestRenameFunctions(unittest.TestCase):
    
    def test_load_json_file(self):
        # test episode mapping file
        episode_mapping = json.loads("""{
                                            "Romance Dawn": {
                                                "01": "S00E36",
                                                "02": "E1",
                                                "03": "E2",
                                                "04": "E3"
                                            }
                                        }
                                    """)
        self.assertEqual(rename.load_json_file("./episodes-test.json"), episode_mapping)
        
        # test chapter mapping file
        chapter_mapping = json.loads("""
                                    {
                                        "700-701": "E628-E630",
                                        "702-703": "E631-E633"
                                    }
                                    """)
        self.assertEqual(rename.load_json_file("./chapters-test.json"), chapter_mapping)
        
        
        # test for a file that doesn't exist
        with self.assertRaises(FileNotFoundError):
            rename.load_json_file("./not-a-json-file.txt")
        
        #test with a file that is not valid json
        #with self.assertRaises(ValueError):
        #   rename.load_json_file("./invalid.json")
        
    def test_list_mkv_files_in_directory_invalid_directory(self):
        # test for a directory that doesn't exist
        with self.assertRaises(FileNotFoundError):
            rename.list_mkv_files_in_directory("./not-a-directory")
        
    @patch("rename.abspath")
    @patch("rename.listdir")
    @patch("rename.isfile")
    def test_list_mkv_files_in_directory(self,mock_isfile, mock_listdir, mock_abspath):
        mock_isfile.return_value = True
        mock_listdir.return_value = ["test.mkv", "test2.mkv", "test3.txt"]
        #mock_abspath.return_value = 
        
        files = rename.list_mkv_files_in_directory("./")
        
        assert mock_listdir.called
        assert mock_abspath.called
              
        mock_abspath.assert_has_calls([call("./test.mkv"), call("./test2.mkv")])
        mock_abspath.assert_called_with("./test2.mkv")
        mock_listdir.assert_called_with("./")
        
        assert len(files) == 2
        
        #self.assertEqual(rename.list_mkv_files_in_directory("./"), ["test.mkv", "test2.mkv"])

    @patch("rename.walk")
    @patch("rename.list_mkv_files_in_directory")
    def test_get_files_from_directories(self, mock_list_mkv, mock_walk):
        mock_list_mkv.return_value = ["test.mkv"]
        mock_walk.return_value = [("./Tests", ("tmp",), ("test.mkv",)),("./Tests/tmp", (), ("test2.mk","test3.mkv"))]
        files = rename.get_files_from_directories("./")
        
        assert mock_list_mkv.called_once
        assert mock_walk.called is False
        mock_list_mkv.assert_called_with("./")
        
        files = rename.get_files_from_directories("./", recurse=True)
        
        assert mock_walk.called
        assert len(files) == 2
        
    #unit test for rename.set_mapping()
    def test_set_mapping(self):
        rename.set_mapping("test", "test2")
        self.assertEqual(rename.episode_mapping, "test")
        self.assertEqual(rename.chapter_mapping, "test2")
    
    #unit test for rename.set_ref_file_vars()
    def test_set_ref_file_vars(self):
        rename.set_ref_file_vars("test", "test2")
        self.assertEqual(rename.episodes_ref_file, "test")
        self.assertEqual(rename.chapters_ref_file, "test2")
    
    #unit test for rename.generate_new_name_for_episode()
    def test_generate_new_name_for_episode(self):
        #TODO
        pass

if __name__ == '__main__':
    unittest.main()