import os
from datetime import datetime
import click
import yaml
from github import Github
from tabulate import tabulate

date_time = datetime.now().strftime("%Y-%m-%d %H:%M")


@click.group()
def cli():

    """
    GitHub API CLI
    """

    pass


@click.command(name="my-issues")
@click.option("--web_table", help="Create issue list as an HTML table", is_flag=True)
@click.option("--web_list", help="Create issue list as an HTML list", is_flag=True)
def my_issues(web_table, web_list):

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
    issues_list_table_html = []

    for repo in repo_list:
        repo = github.get_repo(repo)
        issues = repo.get_issues(state="open", assignee=config_file["username"])

        for issue in issues:
            repository = repo.full_name
            title = issue.title
            description = issue.body
            if description is not None:
                truncated_description = (
                    (issue.body[:160] + "...") if len(description) > 80 else description
                )
            truncated_title = (issue.title[:80] + "...") if len(title) > 80 else title
            created_date = issue.created_at.strftime("%Y-%m-%d")
            updated_date = issue.updated_at.strftime("%Y-%m-%d %H:%m")
            number = issue.number
            link = issue.html_url
            user = issue.user.name if issue.user.name else issue.user.login
            labels = ", ".join(l.name for l in issue.labels)
            issues_list_row_html = [
                created_date,
                updated_date,
                number,
                title,
                truncated_description,
                labels,
                user,
                link,
                repository,
            ]
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
            issues_list_table_html.append(issues_list_row_html)

    if web_list is True:

        with open("./github_issues.html", "w", encoding="utf-8") as html_list:

            html_head = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My GitHub Issues</title>
    <link rel="stylesheet" href="./stylesheet.css">
</head>
<body>
<h1>My GitHub Issues</h1>
<h2>{date_time}</h2>
<ul>
"""
            html_list.write(html_head)

            for issue in sorted(issues_list_table_html):

                list_template = f"""
<li id="block">
    <h3><a href="{issue[7]}" target="_blank"><span style="opacity:0.5">[{issue[2]}]</span> {issue[3]}</a></h3>
    <div id="content">
        <p>{issue[4]}</p>
    </div>
    <div id="metadata">
        <ul>
            <li>Repository: <a href="https://github.com/{issue[8]}" target="_blank">{issue[8]}</a></li>
            <li>Created: {issue[0]} - Updated: {issue[1]}</li>
            <li>Author: {issue[6]} - Updated: {issue[5]}</li>
        </ul>
    </div>
</li>
                """

                html_list.write(list_template)

            html_footer = """

</ul>
</body>
</html>
"""
            html_list.write(html_footer)

    elif web_table is True:

        with open("./github_issues.html", "w", encoding="utf-8") as html_view:

            html = tabulate(
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
                tablefmt="html",
            )

            html_view.write(html)

    else:

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
