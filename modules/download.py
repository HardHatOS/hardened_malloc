#!/usr/bin/env python3
from json import loads
from ssl import create_default_context
from urllib.request import urlopen

######################
### CUSTOM MODULES ###
######################
from messages import error,info

###########
### URL ###
###########
# GitHub URL for the hardened_malloc repository
url_github_api = 'https://api.github.com/repos/GrapheneOS/hardened_malloc/releases/latest'

#################
### FUNCTIONS ###
#################
def ssl():
    # Define Python's default SSL context
    context = create_default_context()
    # Enforce the same TLS version for the minimum as the maximum
    context.minimum_version = context.maximum_version
    # Return the SSL context
    return(context)

def dictkey(dct, key):
    try:
        # Return the value for the specified $key within the $dct dictionary
        return(dct[key])
    except KeyError:
        # If the specified key does not work, then display an error message to stdout and exit 1
        error(f"Unable to obtain the value for the following key: '{key}'")

############
### MAIN ###
############
def main():
    # Display informational message to stdout
    info(f"Querying the GitHub API: {url_github_api}")
    # Obtain the information for the hardened_malloc repository 
    request = urlopen(url_github_api, context = ssl())
    # If the return status is anything besides 200, then the query failed
    if request.code != 200: error(f"Unable to query the GitHub API for the hardened_malloc: {url_github_api}")
    # Define the JSON that contains the information for the hardened_malloc repository. Use `decode()` since it will be a bytes object
    github_api_data = request.read().decode()
    # Parse the JSON contents
    github_api_data = loads(github_api_data)
    # URL to the source .tar file. This URL will be set as Source0 within the .spec file
    tarball_url = dictkey(github_api_data, 'tarball_url')
    # The name of the tag is numerical, and will be used as the version number within the .spec file
    tag_name = dictkey(github_api_data, 'tag_name')
    # Return the URL to the latest release and the tag name
    return(tarball_url, tag_name)
