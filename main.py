import json
import logging

from gitlab_functions import get_file, is_api_key_set
from sql_functions import run_script_from_gitlab, build_connection_string

# Get logger object for error and debug logging
logger = logging.getLogger('SQL_Runner.Load')
logger.setLevel(logging.INFO)  # capture all informational level output

# create file handler which logs debug messages (INFO level)
fh = logging.FileHandler('runner.log')  # output file handler
fh.setLevel(logging.INFO)  # capture all informational level output

# create console handler
ch = logging.StreamHandler()  # command line (stdout) stream handler
ch.setLevel(logging.ERROR)  # capture ERROR level output only

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # format of each line
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# logger.addHandler(ch)   #handler for command line output removed for now 
logger.addHandler(fh)  # handler for log file output


def get_files_to_run(project_id, configuration_file_path,
                     branch="master"):
    """Go to gitlab to get the configuration file, then fetch and run each file specified within it on the DB server.

    Currently the function is hardcoded to look for the configuration file in a specific path.  This could
    be changed to command line args if needed."""
    try:
        logger.info("Get configuration from gitlab.  project: {}, file path: {}, branch: {}".format(project_id,
                                                                                                    configuration_file_path,
                                                                                                    branch))
        file = get_file(project_id,  # POC project is where we store the configuration
                        configuration_file_path,  # git path to configuration file
                        branch)  # branch where the config file lives

        logger.info("# of Lines in configuration file: {}".format(len(file.split('\n'))))
        config = json.loads(file)  # parse the config file JSON into a nested dictionary object

        logger.info("Start Processing contents")
    except Exception as e:
        logger.error(
            "There was an error retrieving the configuration file." +
            "  project:{}, path:{}, branch:{}".format(project_id,
                                                      configuration_file_path,
                                                      branch)
        )
        exit(1)  # exit the program with error code 1.  Can't function without config.

    for server in config:  # first level of JSON is server
        for database in config[server]:  # second level is database
            connection_string = build_connection_string(server, database)  # build conn str from server and db
            logger.info("connection string: {}".format(connection_string))
            for item in config[server][database]:  # item is a dictionary object.
                try:
                    branch = item["branch"]  # branch of project
                    git_file_path = item["git_file_path"]  # git path in repo
                    project = item["project"]  # id of project

                    run_script_from_gitlab(connection_string, git_file_path, project,
                                           branch)  # fetch and run the script
                    logger.info("completed item: {}".format(item))

                except Exception as e:
                    logger.error(
                        "An error occurred while running config item.  server: {}, db: {}, error: {}, item = {}".format(
                            server, database, e, item))


if __name__ == "__main__":
    is_api_key_set()  # print a message if the API key is set or not
    get_files_to_run()  # fetch configuration file from gitlab, then run all files specified in the config.
