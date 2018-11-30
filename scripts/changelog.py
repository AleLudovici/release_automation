import os
import re
import subprocess
import requests


def __run_cmd(cmd):
    cmds = list()
    cmds.append('bash')
    cmds.append('-c')
    cmds.append(cmd)

    environment = os.environ.copy()
    return subprocess.check_output(cmds, env=environment)


def __last_two_tags():
    cmd = "git tag --sort -version:refname | head -n 2"

    # Last 2 tags
    tags = __run_cmd(cmd).decode("utf-8").split('\n')
    valid_tags = filter(lambda tag: len(tag) > 0, tags)

    return list(valid_tags)


def __commit_with_pr_number(compiled_re, commit):
    match = compiled_re.search(commit)
    return match.group(0).strip('#') if match is not None else None


def __release_merge_commits(previous_tag, current_tag):
    # %s selects "subject" via the Git formatting args (https://git-scm.com/docs/pretty-formats)
    cmd = "git log {}..{} --merges --pretty=format:'%s'".format(previous_tag, current_tag)
    output = __run_cmd(cmd)
    commits = output.decode("utf-8").split('\n')

    # only merge commits from pull requests
    regex_pr_number = r'(#[0-9])\w+'
    compiled_re = re.compile(regex_pr_number)
    pr_commits = map(lambda commit: __commit_with_pr_number(compiled_re, commit), commits)
    return list(filter(lambda id: id is not None, pr_commits))


def __fetch_pull_request(pr_number, credentials_file='../credentials.txt'):
    token = open(credentials_file, 'r').read()
    payload = {'Authorization: token': token}
    url = "https://api.github.com/repos/AleLudovici/release_automation/pulls/{}".format(pr_number)
    return requests.get(url, params=payload)


def __pull_request_details(pull_requests_numbers):
    details = list()
    for number in pull_requests_numbers:
        result = __fetch_pull_request(number)
        if result.status_code == 200:
            response_json = result.json()
            title = response_json['title']
            labels = response_json['labels']
            details.append((title, labels))

    return details

# def fetch_closed_issues(credentials_file: str):
#
#
# def fetch_closed_pull_requests(credentials_file: str):
#     closed_issues_response = fetch_closed_issues(credentials_file)
#     if closed_issues_response.status_code == 200:
#         closed_issues = closed_issues_response.json()
#         pull_requests_filter = filter(lambda issue: issue['state'] == 'closed', closed_issues)
#         pull_requests = list(pull_requests_filter)
#         print('There are %s pull requests', len(pull_requests))
#         return pull_requests
#     else:
#         return None

# tags = __last_two_tags()
print(__release_merge_commits('7.12.0', '7.13.0'))
# TODO: Get PR details



# TODO: Filter PRs containing merge_commit_sha
