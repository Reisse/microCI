import threading
import subprocess

from github import Github


def schedule_deployment(deployment):
    threading.Timer(int(deployment['interval']) * 60, process_deployment, [deployment]).start()


def process_deployment(deployment):
    g = Github(deployment['token'])

    repo = g.get_repo(deployment['repository'])
    branch = repo.get_branch(deployment['branch'])

    if deployment['sha'] == '' and deployment['immediate'] != 'True':
        deployment['sha'] = branch.commit.sha
    elif branch.commit.sha != deployment['sha']:
        deployment['sha'] = branch.commit.sha
        try:
            subprocess.run(deployment['action'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as e:
            repo.create_issue(title='Deployment of \'' + deployment['sha'] + '\' failed',
                    body='Output:\n```\n' + e.stdout.decode("utf-8") +
                            '```\nErrors:\n```\n' + e.stderr.decode("utf-8") + '```')

    schedule_deployment(deployment)
