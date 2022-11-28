import os
from github import Github
from tabulate import tabulate
import click
import yaml


@click.group()
def cli():

    """
    GitHub API CLI
    """

    pass


@click.command(name="my-issues")
def my_issues():

    """
    Display a table of issues assigned to me
    """

    # Configuration file:
    with open(f"{os.environ['HOME']}/.github.yml", "r", encoding="utf-8") as config:

        # Load config file:
        config_file = yaml.safe_load(config)

    github = Github(config_file["github_token"])

    repo_list = config_file["repo_list"]

    issues_list_table = []

    for repo in repo_list:
        repo = github.get_repo(repo)
        issues = repo.get_issues(state="open", assignee=config_file["username"])

        for issue in issues:
            title = issue.title
            truncated_title = (issue.title[:80] + "...") if len(title) > 80 else title
            created_date = issue.created_at.strftime("%Y-%m-%d")
            updated_date = issue.updated_at.strftime("%Y-%m-%d %H:%m")
            number = issue.number
            link = issue.html_url
            user = issue.user.name if issue.user.name else issue.user.login
            labels = ", ".join(l.name for l in issue.labels)
            issues_list_row = [
                created_date,
                updated_date,
                number,
                truncated_title,
                labels,
                user,
                link,
            ]
            issues_list_table.append(issues_list_row)

    print(
        tabulate(
            sorted(issues_list_table),
            headers=[
                "created",
                "updated",
                "number",
                "title",
                "labels",
                "author",
                "link",
            ],
            maxcolwidths=[None, None, None, 100, None, None, None],
        )
    )


# Commands:
cli.add_command(my_issues)

# Call the CLI:
cli()
