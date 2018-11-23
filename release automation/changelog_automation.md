#Release notes automation

##Format
The release note will be divided in three sections:

- __New features__
- __Minor changes__
- __Bug fixes__

Each section contains a list of PR. Each of the entry will have the Jira ticket number and the title. This will be determined by the PR title. For this to be possible _every PR must follow the following format_:

- JIRA-TICKET: Title of the PR

To determine the section _every PR must have a label that match the section name_. 

##Steps
We will use the Github API to automate this process. This series of steps _must be perfomed only after the master branch has been merged into release_.

###1. Get a list of closed issues
A list of PRs can be obtaines with one of the following enpoints:

- GET repos/:owner/:repo/pulls
- GET repos/:owner/:repo/issues

We will choose `issues` as it allows to query them by time. This time corresponds to the previous release cut date. A request will looks like:

- GET repos/:owner/:repo/issues?state=close&since=YYYY-MM-DDTHH:MM:SSZ

The respone is a JSON array containing closed PRs and closes Issues. The get the PR we check for the existence of a `pull_request` key. This is a JSON object that contains a link to the PR.

###2. Get PR details

For each PR we issue the following request:

- GET repos/:owner/:repo/pulls/id

The response is a JSON object. We are interested in the following keys:

1. title
2. labels

###3. Create Changelog

After we finish looping trough the PRs on step 2 we will be able to create the Changelog.