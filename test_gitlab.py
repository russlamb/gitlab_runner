import unittest

from gitlab_functions import get_file, print_projects, print_project_branches
from sql_functions import run_sql_script, build_connection_string, run_script_from_gitlab

TEST_PROJECT = 806
TEST_GROUP = 434
TEST_FILE = "test_file.txt"
TEST_CONNECTION_STRING = "Driver={{SQL Server}};Server=Localdb;database=Test"
TEST_SERVER="LocalDB"
TEST_DB = "Test"

class TestApiManagers(unittest.TestCase):
    """Tests for checking connectivity to gitlab"""
    def test_project_branches(self):
        """get list of branches for nvision project"""
        
        branches = print_project_branches(TEST_PROJECT) #checking the TEST project
        self.assertGreaterEqual(len(branches), 1) # at least one branch makes sense.

    def test_projects(self):
        """get list of projects for group"""
        
        projects = print_projects(TEST_GROUP)
        self.assertGreaterEqual(len(projects), 40)  # GROUP has 40 projects as of 9/11/2018.  Test asserts at least 40

    def test_file(self):
        
        file = get_file(TEST_PROJECT, TEST_FILE,
                        'master')
        print(file)

class TestApiAndPyodbc(unittest.TestCase):
    """Test combination of gitlab and sql script"""
    def test_run_file(self):
        """run test script that creates tables and inserts data with separate function calls"""
        file = get_file(TEST_PROJECT,TEST_FILE,
                        'master')

        run_sql_script(TEST_CONNECTION_STRING, file)

    def test_get_and_run(self):
        """run test script that creates tables and inserts data with one function call"""
        run_script_from_gitlab(build_connection_string(TEST_SERVER,TEST_DB),
                     TEST_FILE, TEST_PROJECT,"master"
                               )

class TestSqlRun(unittest.TestCase):
    """Test sql functions"""
    def test_connection_string_builder(self):
        self.assertEqual( build_connection_string(TEST_SERVER,TEST_DB),
        TEST_CONNECTION_STRING
        ,"connection string builder not working")

