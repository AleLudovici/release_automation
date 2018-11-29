import requests


def build_issues_requests(credentials_file: str):
    token = open(credentials_file, 'r').read()
    payload = {'Authorization: token': token, 'state': 'closed'}
    return requests.get("https://api.github.com/repos/AleLudovici/release_automation/issues", params=payload)


# TODO: Get a list of closed PRs


# TODO: Get PR details



# TODO: Filter PRs containing merge_commit_sha
