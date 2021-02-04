## BU Python Login ##

This is a script to login to any BU site that uses Shibboleth. To use:  

1. Create User object, passing in username and password.
2. Call login method, passing in url you want to log in to.
3. The login method will return a session object that contains the cookes n stuff.

The accommodate class is used to download accommodation letters. To use:  

1. Create Accommodate object passing in previously created session
2. Call download_letters method. 
Options: (bool, string year):
    - bool(True/False): True will generate a letter to copy and paste to professors
    - string("all"/"year"): "all" will download all letters. "2020" will download letters generated in the year 2020.