# import the library to parse the parameters input and the Github JSON
import argparse, json

# import the library to make requests to API
import requests

# import library to send git clone command
from subprocess import call

# print the name of the program
print ("""
 _____ _ _   _           _      ______                   _____                    _
|  __ (_) | | |         | |     | ___ \                 /  __ \                  | |
| |  \/_| |_| |__  _   _| |__   | |_/ /___ _ __   ___   | /  \/_ __ __ ___      _| | ___ _ __
| | __| | __| '_ \| | | | '_ \  |    // _ \ '_ \ / _ \  | |   | '__/ _` \ \ /\ / / |/ _ \ '__|
| |_\ \ | |_| | | | |_| | |_) | | |\ \  __/ |_) | (_) | | \__/\ | | (_| |\ V  V /| |  __/ |
 \____/_|\__|_| |_|\__,_|_.__/  \_| \_\___| .__/ \___/   \____/_|  \__,_| \_/\_/ |_|\___|_|
                                          | |
                                          |_|
""")

# ===== PARAMETERS =====
# the code to be searched
code_to_search = None

# the keyword to identify the repo
keyword = None

# the file in which the code is searched in
file_that_contains_code = None

# username and passowrd
username = None
password = None

# how many results per page? 100 is the maximum
results_per_page = 5

# the limit of repo to download
results_limit = 500;
# ===== PARAMETERS =====



# this variable will hold the number of repositories retrieved with the search_repo API invocation
total_count = 0

# is this the first loop? (this for emulating a do-while loop)
first_loop = True

# we start from page 1
current_result_page = 1

# the currently number of downloaded repo
current_found_repo = 0;

# github base URL
github_base_url = 'https://github.com/'
api_base_url = 'https://api.github.com/'
search_repo = 'search/repositories'
search_code = 'search/code'

# add the description for the arguments usage
parser = argparse.ArgumentParser(description="crawl python repositories by keywords, file name and code")

# parameters
parser.add_argument("code", help='Code to be searched in Github repositories')
parser.add_argument("-u", "--username", help='Github username for authentication')
parser.add_argument("-p", "--password", help='Github password for authentication')
parser.add_argument("-k", "--keywords", help='Keywords for repository lookup (concatenated with +)')
parser.add_argument("-f", "--filename", help='File name in which to search for the code')
parser.add_argument("-r", "--resultPerPage"    , help='Number of results per page. 100 is the maximum and 50 the default')
parser.add_argument("-l", "--resultLimit"    , help='Limit of the number of repo to download. 500 is the default, there is no maximum')


# parse the parameters
args = parser.parse_args()

# acquire the parameters
if (args.code):
    code_to_search = args.code
if (args.keywords):
    keyword = args.keywords
if (args.filename):
    file_that_contains_code = args.filename
if (args.password):
    password = args.password
if (args.username):
    username = args.username
if (args.resultPerPage):
    results_per_page = args.resultPerPage
if (args.resultLimit):
    results_limit = args.resultLimit
    if (resultLimit > 100):
        resultLimit = 100



# logical flow:
#   for each keyword, do a repository search (parameter q = keyword, page = page_number)
#       for each repository, do a code search specifying (parameter q = code, repo = repositoryName, filename = filename)


# the final result
android_opensource_app_repositories = []

# while there are still repo to analyze OR this is the first loop
while (total_count > 0 or first_loop):

    # start a new loop
    print("starting a new loop, page: " + str(current_result_page))

    # build the url with the keyword and the current result page
    url_repo = api_base_url + search_repo
    url_repo = (url_repo + "?q=" + keyword + "&") if (keyword != None) else (url_repo)
    url_repo = url_repo + "page=" + str(current_result_page) + "&per_page=" + str(results_per_page)

    # the request made to github to download the repos
    r_repo = None

    # send the request with or without credentials
    if (username != None and password != None):
        r_repo = requests.get(url_repo, auth=(username, password))
    else:
        r_repo = requests.get(url_repo)

    # if the request was not successful
    if (r_repo.status_code != 200):
        # print error
        print ("    error while searching repositories: " + str(r_repo.status_code))

    # if the request was successful
    else:
        # acquire the JSON
        parsed_json_repo = json.dumps(r_repo.json(), ensure_ascii=False)
        j_repo = json.loads(parsed_json_repo)

        # if this is the first loop, set the total_count value
        if (first_loop):
            total_count = j_repo['total_count']
            first_loop = False

        # now, for each result repo in the json (thus <param['per_page']> repositories)
        for i in range(results_per_page):
            # get the repository name
            repo_name = j_repo['items'][i]['full_name']

            # print it
            print ("    analyzing repository: " + repo_name)

            # build the query
            url_code = api_base_url + search_code + "?q=" + code_to_search
            url_code = (url_code + "+filename:" + file_that_contains_code) if (file_that_contains_code != None) else (url_code)
            url_code = (url_code + "+repo:" + repo_name) if (repo_name != None) else (url_code)
            url_code = (url_code + "+in:file")

            # the request made to github to download the file in the repo
            r_code = None

            # send the request with or without credentials
            if (username != None and password != None):
                r_code = requests.get(url_code, auth=(username, password))
            else:
                r_code = requests.get(url_code)

            # if the request was not successful
            if (r_code.status_code != 200):
                # print error
                print ("    error while searching file in repo: " + str(r_code.status_code))

            # if the request was successful
            else:
                # acquire the JSON
                parsed_json_code = json.dumps(r_code.json(), ensure_ascii=False)
                j_code = json.loads(parsed_json_code)

                # for each file containing the code (there should be just one but )
                for item in j_code['items']:

                    # if the file is a 'build.gradle' file and it is at root level
                    if (item['name'] == file_that_contains_code and item['path'] == file_that_contains_code):

                        # save the name of the repo
                        android_opensource_app_repositories.append(github_base_url + repo_name)

                        # clone the repo as <repo_name>
                        call(["git", "clone", github_base_url + repo_name, "-".join(repo_name.split("/"))] )

                        # increment the current found repo
                        current_found_repo = current_found_repo + 1;

        # print that the loop (thus the oage) is ended
        print("end of loop. total_count = " + str(total_count) + ", page = " + str(current_result_page) +
              ". Have to analyze other " + str(total_count -current_result_page*results_per_page) + " repositories")

        # increment the page number
        current_result_page = current_result_page + 1

        # decrement the total count of repo to crawl
        total_count = total_count - results_per_page

        # print the partial results
        print (android_opensource_app_repositories)

# finally print the results
print (android_opensource_app_repositories)
