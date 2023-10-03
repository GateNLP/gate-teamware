# Utility commands
Django provides various [built-in utility functions](https://docs.djangoproject.com/en/4.2/ref/django-admin/) that can 
be accessed from `manage.py` script at the root of the project. A few teamware-specific utility commands have been added
in order to assist with management and development of the application.

To use the custom utility commands, navigate to the app's root folder (with the file `manage.py`) and 
run `./manage.py command_name` where `command_name` is the command that you'd like to run. Adding a `-h` argument
prints out the description and all possible options for the command e.g.:

```
./manage.py export_annotations -h
```

## Available commands

### General Usage
- **export_annotations** - Manually export annotations belonging to a project and save it to a zipped file.
  
### Development
<span style="color:red">**Warning, use of the following functions will modify or reset your database! Ensure your database is backed up
before using them outside of development.**</span> 

- **load_test_fixture** -  The command loads a pre-defined test fixture. Use without any arguments to see all 
  available fixtures.
- **check_create_superuser** - Checks whether there's a superuser in the database and creates one if none exists. The 
  username, password and email are obtained from environment variables `SUPERUSER_USERNAME`, `SUPERUSER_PASSWORD` and
  `SUPERUSER_EMAIL` respectively.

