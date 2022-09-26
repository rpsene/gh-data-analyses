# -*- coding: utf-8 -*-

"""
Copyright (C) 2022 Rafael Sene

Licensed under the Apache License, Version 2.0 (the “License”);
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
    Contributors:
        * Rafael Peria de Sene <rpsene@gmail.com>

  This scripts calculates the Pull Request Lead Time of a given
  GH Project, which provides the number of days between the moment
  a PR is opened until it is closed.
"""

from datetime import datetime
from github import Github

GH_TOKEN = 'CHANGE_ME:YOUR_GH_TOKEN'
GH_ORG = 'CHANGE_ME:THE_GH_ORG_NAME_FOR_THE_PROJECT_YOU_WANT_EXTRACT_DATA'
GH_REPOSITORY = 'CHANGE_ME:THE_GH_REPO_NAME'

git = Github(GH_TOKEN)
org = git.get_organization(GH_ORG)
repo = org.get_repo(GH_REPOSITORY)

pulls = repo.get_pulls(state='closed', sort='created', base='master')

date_format = "%Y-%m-%d"

# iterate over the prs which were merged, calculating the diff
# between date when the PR was created and the date it was closed.
print('"pr_number","creation_day","closure_day","lead_time"')
for pr in pulls:
    if pr and pr.is_merged:
        if pr.created_at.year and pr.created_at.month and pr.created_at.day:
            crday = str(pr.created_at.year) + '-' + \
                str(pr.created_at.month) + '-' + str(pr.created_at.day)
            pr_creation_day = datetime.strptime(crday, date_format)
        if pr.closed_at.year and pr.closed_at.month and pr.closed_at.day:
            clday = str(pr.closed_at.year) + '-' + \
                str(pr.closed_at.month) + '-' + str(pr.closed_at.day)
            pr_closure_day = datetime.strptime(clday, date_format)
        delta = pr_closure_day - pr_creation_day
        print('"' + str(pr.number) + '","' + str(crday) +
              '","' + str(clday) + '","' + str(delta.days) + '"')
