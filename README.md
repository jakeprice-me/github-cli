## GitHub Personal Access Token

Create a [New Personal Access Token](https://github.com/settings/tokens/new) and give it `repo` access.

## Install CLI

```sh
pip3 install -r requirements.txt
pip3 install .
```

## Bash Completion

```sh
_GITHUB_COMPLETE=bash_source github > ./.github-complete.bash
```

## Configuration File

A configuration file needs to be created at `$HOME/.github.yml`.

```sh
mkdir $HOME/.github.yml
```

Make sure the following variables are added.

```yml
github_token: <token>
username: <github-username>
repo_list:
  - <repo-name>
  - <repo-name
```

