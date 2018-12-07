# GithubRepositoryCrawler
Simple Python tool that wraps Github APIs to download repositories searched by keywords, file and code:
1. First, it makes a repository search (parameters k = keywords, r = results_per_page, l = result_limit)
2. Then, for each repository, it performs a code search (parameters code (required), f = file_that_contains_code)
3. Eventually, it downloads (through `git clone`) the repositories that matches the specified parameters

Rememeber that Github limits the number of requests you can do: to increment this number, specify username (-u) and password (-p)

# Help
```
_____ _ _   _           _      ______                   _____                    _
|  __ (_) | | |         | |     | ___ \                 /  __ \                  | |
| |  \/_| |_| |__  _   _| |__   | |_/ /___ _ __   ___   | /  \/_ __ __ ___      _| | ___ _ __
| | __| | __| '_ \| | | | '_ \  |    // _ \ '_ \ / _ \  | |   | '__/ _` \ \ /\ / / |/ _ \ '__|
| |_\ \ | |_| | | | |_| | |_) | | |\ \  __/ |_) | (_) | | \__/\ | | (_| |\ V  V /| |  __/ |
\____/_|\__|_| |_|\__,_|_.__/  \_| \_\___| .__/ \___/   \____/_|  \__,_| \_/\_/ |_|\___|_|
                                         | |
                                         |_|

usage: crawler.py [-h] [-u USERNAME] [-p PASSWORD] [-k KEYWORDS] [-f FILENAME]
                 [-r RESULTPERPAGE] [-l RESULTLIMIT]
                 code

crawl python repositories by keywords, file name and code

positional arguments:
 code                  Code to be searched in Github repositories

optional arguments:
 -h, --help            show this help message and exit
 -u USERNAME, --username USERNAME
                       Github username for authentication
 -p PASSWORD, --password PASSWORD
                       Github password for authentication
 -k KEYWORDS, --keywords KEYWORDS
                       Keywords for repository lookup (concatenated with +)
 -f FILENAME, --filename FILENAME
                       File name in which to search for the code
 -r RESULTPERPAGE, --resultPerPage RESULTPERPAGE
                       Number of results per page. 100 is the maximum and 50
                       the default
 -l RESULTLIMIT, --resultLimit RESULTLIMIT
                       Limit of the number of repo to download. 500 is the
                       default, there is no maximum
```

# Example Usage

### General use
python3 crawler.py codeToBeSearched -u yourUsernameOrEmail -p yourPassword -f fileWhereToSearchCode -k repoKeywords

### Crawl android open source applications
python3 crawler.py "apply plugin: 'com.android.application'" -u yourUsernameOrEmail -p yourPassword -f build.gradle -k android+application
