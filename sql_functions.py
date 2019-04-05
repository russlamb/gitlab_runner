from pyodbc import connect

from gitlab_functions import get_file



def run_sql_script(connection_string, sql_script):
    """run a sql script using pyodbc"""
    with connect(connection_string) as conn:
        cursor = conn.cursor()
        sqlQuery = ""
        for line in sql_script.splitlines():
            if line.startswith('GO') and line.endswith('GO'):
                cursor.execute(sqlQuery)
                sqlQuery = ''
            else:
                sqlQuery = sqlQuery + "\n" + line
    if len(sqlQuery.strip())>0:
        cursor.execute(sqlQuery)


def build_connection_string(server, database, app_name='SQL RUNNER'):
    """Build a connection string from template given server and database
    Note: assumes driver is SQL Server.  
    """
    return "Driver={{SQL Server}};Server={0};Database={1};Trusted_Connection=yes;APP={2};".format(server,
                                                                                                  database, app_name)


def run_script_from_gitlab(connection_string, git_file_path, project_id, git_branch):
    """get file from gitlab and run it.  return the file contents."""
    file = get_file(project_id, git_file_path, git_branch)
    run_sql_script(connection_string, file)
    return file
