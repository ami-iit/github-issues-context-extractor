import click
import os
from urllib.parse import urlparse
from github import Github
import json
import base64
import requests
import itertools
import subprocess

import re

def encode_images_as_blobs(content, github_token=None, skip_images=False):
    # Search for image URLs and encode them as base64 blobs
    if skip_images:
        return content
    
    encoded_content = content
    image_urls = []
    # Assume image URLs are markdown-style ![alt text](url)
    for line in content.splitlines():
        if line.startswith("![") and "](" in line and line.endswith(")"):
            url = line.split("](")[-1][:-1]
            image_urls.append(url)

    for url in image_urls:
        try:
            # Prepare headers for authentication if token is available
            headers = {}
            if github_token and 'github.com' in url:
                headers['Authorization'] = f'Bearer {github_token}'
            
            image_response = requests.get(url, headers=headers)
            if image_response.status_code == 200:
                encoded_blob = base64.b64encode(image_response.content).decode('utf-8')
                encoded_content = encoded_content.replace(url, f"data:image;base64,{encoded_blob}")
            else:
                print(f"Failed to fetch image: {url}")
        except Exception as e:
            print(f"Error fetching image {url}: {e}")
    return encoded_content

def extract_issues(repo, branch, github_token, output_file, query, skip_images=False):
    # Initialize GitHub instance
    g = Github(github_token)

    issues_data = []

    # Search for issues
    query_issues = f"repo:{repo} {query} is:issue"
    query_prs = f"repo:{repo} {query} is:pull-request"

    # Perform the search
    issues = g.search_issues(query=query_issues)
    prs = g.search_issues(query=query_prs)
    for issue in itertools.chain(issues, prs):
        print(f"Processing issue {issue}")
        issue_data = {
            "title": issue.title,
            "body": encode_images_as_blobs(issue.body or "", github_token, skip_images),
            "comments": [],
        }

        # Get comments for each issue
        comments = issue.get_comments()
        for comment in comments:
            comment_data = {
                "author": comment.user.login,
                "body": encode_images_as_blobs(comment.body or "", github_token, skip_images)
            }
            issue_data["comments"].append(comment_data)

        issues_data.append(issue_data)

    # Save to JSON file
    with open(output_file, "w") as f:
        json.dump(issues_data, f, indent=4)


@click.command()
@click.option('--repo', prompt='GitHub repository', help='The GitHub repository, in the owner/name form.')
@click.option('--branch', default='main', help='The branch to load from the repository.')
@click.option('--github_token', default=None, hide_input=True, help='Your GitHub Personal Access Token.')
@click.option('--output_file', default='github_issues.json', help='The name of the file to save')
@click.option('--query', default='', help='The issues to select a subset of query')
@click.option('--skip-images', is_flag=True, help='Skip downloading and encoding images as base64 blobs')
def main(repo, branch, github_token, output_file, query, skip_images):
    """CLI entry point."""
    # Check if GITHUB_TOKEN is set in environment.
    if not github_token:
        if 'GITHUB_TOKEN' in os.environ:
            github_token = os.environ['GITHUB_TOKEN']

    if not github_token:
        # Try to get token from gh auth token
        try:
            result = subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True)
            if result.returncode == 0:
                token = result.stdout.strip()
                if token:
                    github_token = token
            else:
                print("No token found via `gh auth token` or command not successful.")
        except Exception as e:
            print(f"Error checking `gh auth token`: {e}")

    # If nothing worked, get it from comamnd line
    if not github_token:
        github_token = click.prompt('GitHub Token', hide_input=True)
    extract_issues(repo, branch, github_token, output_file, query, skip_images)
    print(f"Context of requested issue saved at {output_file}")

if __name__ == '__main__':
    main()
