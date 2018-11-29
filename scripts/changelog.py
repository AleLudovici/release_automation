import requests

token = open('credentials.txt', 'r').read()
payload = {'Authorization: token': token, 'state': 'closed'}
request = requests.get("https://api.github.com/repos/AleLudovici/release_automation/issues", params=payload)
print(request.url)
# TODO: Get a list of closed PRs


# TODO: Get PR details



# TODO: Filter PRs containing merge_commit_sha
