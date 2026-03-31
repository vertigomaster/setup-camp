#!/usr/bin/env python3
"""
Setup script for creating a structured workspace with a cloned Git repository.

Usage:
    python setup_repo.py --org <org> --repo <repo>
    python setup_repo.py --url <full_git_url>
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


def parse_repo_info(url_or_org, repo=None):
    """Parse repository information from URL or org/repo."""
    if repo:
        # org/repo format
        org = url_or_org
        repo_name = repo
        url = f"https://github.com/{org}/{repo_name}"
    else:
        # Full URL format
        url = url_or_org
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')
        if len(path_parts) >= 2:
            org = path_parts[-2]
            repo_name = path_parts[-1]
            if repo_name.endswith('.git'):
                repo_name = repo_name[:-4]
        else:
            raise ValueError("Invalid Git URL format")

    return org, repo_name, url


def clone_repo(repo_url, repo_name):
    """Clone the repository using GitHub CLI."""
    try:
        subprocess.run(["gh", "repo", "clone", repo_url], check=True)
        print(f"Successfully cloned {repo_url} into {repo_name}")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        sys.exit(1)


def create_symlink(repo_name):
    """Create symbolic link .repo pointing to the cloned repository."""
    if os.name == 'nt':  # Windows
        # On Windows, use mklink for directory symlinks
        try:
            subprocess.run(["cmd", "/c", "mklink", "/d", ".repo", repo_name], check=True)
            print(f"Created symbolic link .repo -> {repo_name}")
        except subprocess.CalledProcessError as e:
            print(f"Error creating symbolic link: {e}")
            sys.exit(1)
    else:  # Unix-like systems
        try:
            os.symlink(repo_name, ".repo")
            print(f"Created symbolic link .repo -> {repo_name}")
        except OSError as e:
            print(f"Error creating symbolic link: {e}")
            sys.exit(1)


def create_folders():
    """Create builds and ext-resources folders."""
    Path("builds").mkdir(exist_ok=True)
    Path("ext-resources").mkdir(exist_ok=True)
    print("Created folders: builds, ext-resources")


def create_vscode_workspace(wd_name):
    """Create VS Code workspace file."""
    workspace_data = {
        "folders": [
            {
                "path": ".",
                "name": "[ROOT]"
            },
            {
                "path": ".repo",
                "name": "Repo"
            },
            {
                "path": "builds",
                "name": "Builds"
            },
            {
                "path": "ext-resources",
                "name": "External Resources"
            }
        ],
        "settings": {}
    }

    workspace_file = f"{wd_name}.code-workspace"
    with open(workspace_file, 'w') as f:
        json.dump(workspace_data, f, indent=4)
    print(f"Created VS Code workspace file: {workspace_file}")


def main():
    parser = argparse.ArgumentParser(description="Setup workspace with cloned Git repository")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--org", help="GitHub organization name")
    group.add_argument("--url", help="Full Git repository URL")

    parser.add_argument("--repo", help="Repository name (required if using --org)")

    args = parser.parse_args()

    if args.org and not args.repo:
        parser.error("--repo is required when using --org")

    if args.org:
        org, repo_name, repo_url = parse_repo_info(args.org, args.repo)
    else:
        org, repo_name, repo_url = parse_repo_info(args.url)

    wd_name = Path.cwd().name

    print(f"Setting up workspace for {org}/{repo_name} in {wd_name}")

    # Create folders
    create_folders()

    # Clone repository
    clone_repo(repo_url, repo_name)

    # Create symbolic link
    create_symlink(repo_name)

    # Create VS Code workspace
    create_vscode_workspace(wd_name)

    print("Setup complete!")


if __name__ == "__main__":
    main()