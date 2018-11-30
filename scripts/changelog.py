import os
import re
import subprocess
from collections import defaultdict

import requests


def __run_cmd(cmd):
    cmds = list()
    cmds.append('bash')
    cmds.append('-c')
    cmds.append(cmd)

    environment = os.environ.copy()
    return subprocess.check_output(cmds, env=environment)


def _last_two_tags():
    cmd = "git tag --sort -version:refname | head -n 2"

    # Last 2 tags
    tags = __run_cmd(cmd).decode("utf-8").split('\n')
    valid_tags = filter(lambda tag: len(tag) > 0, tags)

    return list(valid_tags)


def __commit_with_pr_number(compiled_re, commit):
    match = compiled_re.search(commit)
    return match.group(0).strip('#') if match is not None else None


def _release_merge_commits(previous_tag, current_tag):
    # %s selects "subject" via the Git formatting args (https://git-scm.com/docs/pretty-formats)
    cmd = "git log {}..{} --merges --pretty=format:'%s'".format(previous_tag, current_tag)
    output = __run_cmd(cmd)
    commits = output.decode("utf-8").split('\n')
    # only merge commits from pull requests
    regex_pr_number = r'#\d+'
    compiled_re = re.compile(regex_pr_number)
    pr_commits = map(lambda commit: __commit_with_pr_number(compiled_re, commit), commits)
    return list(filter(lambda id: id is not None, pr_commits))


def __fetch_pull_request(pr_number, credentials_file='credentials.txt'):
    token = open(credentials_file, 'r').read()
    payload = {'Authorization: token': token}
    url = "https://api.github.com/repos/AleLudovici/release_automation/pulls/{}".format(pr_number)
    return requests.get(url, params=payload)


def _pull_request_details(pr_numbers):
    details = defaultdict(list)
    for number in pr_numbers:
        result = __fetch_pull_request(number)
        if result.status_code == 200:
            response_json = result.json()
            title = response_json['title']
            label_titles = list(map(lambda l: l['name'], response_json['labels']))
            label = label_titles[0] if label_titles else None
            if label is not None:
                details[label].append(title)

    return dict(details)


def create_changelog():
    print('creating changelog...')
    tags = _last_two_tags()
    print(tags)
    pull_requests_numbers = _release_merge_commits(tags[1], tags[0])
    print(pull_requests_numbers)
    pull_requests_details = _pull_request_details(pull_requests_numbers)
    print(pull_requests_details)

    changelog_file = open('changelog.txt', 'w')
    for key, value in pull_requests_details.items():
        changelog_file.write('{}\n'.format(key))
        changes = '\n'.join(value)
        changelog_file.write('{}\n'.format(changes))
        changelog_file.write('\n')
    changelog_file.close()


create_changelog()
