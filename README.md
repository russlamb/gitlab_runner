# 	SQL Runner
This project will run select files from gitlab in the specified database(s).  

# Configuration
The file used for configuration is stored as JSON on the gitlab server itself.

JSON specifies the server and database in which to run the sql as nested objects.  The Database key corresponds with a list
of objects specifying the file / branch / project id that should be run.  Assumes Integrated authentication for database.

"git_file_path" should be the path for your file.  The path can be copied from the url of the file.  It is everything after the branch name.  

For example, we will get the file path for this file url in the POC project, master branch:

http://SERVER/GROUP/REPO/blob/master/FOLDERPATH/runner_config_qb.json

The file path is:

/FOLDERPATH/runner_config_qb.json

This is everything after the branch part of the url ("master").

To find the id for your project.  Use this API url http://SERVER/api/v4/groups/434/projects


