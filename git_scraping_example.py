import requests
import json
import pandas as pd
from datetime import datetime
import time

class GitScraper:
    def __init__(self, token=None):
        """
        Initialize Git scraper with optional GitHub token
        """
        self.token = token
        self.headers = {}
        if token:
            self.headers['Authorization'] = f'token {token}'
        self.headers['Accept'] = 'application/vnd.github.v3+json'
    
    def get_repository_info(self, owner, repo):
        """
        Get basic repository information
        """
        url = f"https://api.github.com/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None
    
    def get_commits(self, owner, repo, since_date=None, until_date=None):
        """
        Get commits from a repository
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        params = {}
        
        if since_date:
            params['since'] = since_date
        if until_date:
            params['until'] = until_date
            
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return []
    
    def get_file_content(self, owner, repo, path, branch='main'):
        """
        Get content of a specific file
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        params = {'ref': branch}
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None
    
    def get_repository_files(self, owner, repo, path=''):
        """
        Get list of files in a repository
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return []
    
    def search_repositories(self, query, sort='stars', order='desc'):
        """
        Search for repositories
        """
        url = "https://api.github.com/search/repositories"
        params = {
            'q': query,
            'sort': sort,
            'order': order
        }
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None

# Example usage
def main():
    # Initialize scraper (you can add your GitHub token for higher rate limits)
    scraper = GitScraper()
    
    # Example 1: Get repository information
    print("=== Repository Information ===")
    repo_info = scraper.get_repository_info("pandas-dev", "pandas")
    if repo_info:
        print(f"Repository: {repo_info['name']}")
        print(f"Description: {repo_info['description']}")
        print(f"Stars: {repo_info['stargazers_count']}")
        print(f"Language: {repo_info['language']}")
    
    # Example 2: Get recent commits
    print("\n=== Recent Commits ===")
    commits = scraper.get_commits("pandas-dev", "pandas", limit=5)
    for commit in commits[:3]:
        print(f"Commit: {commit['sha'][:8]}")
        print(f"Message: {commit['commit']['message']}")
        print(f"Author: {commit['commit']['author']['name']}")
        print(f"Date: {commit['commit']['author']['date']}")
        print("-" * 50)
    
    # Example 3: Search for repositories
    print("\n=== Repository Search ===")
    search_results = scraper.search_repositories("machine learning", sort="stars", order="desc")
    if search_results:
        for repo in search_results['items'][:3]:
            print(f"Name: {repo['name']}")
            print(f"Owner: {repo['owner']['login']}")
            print(f"Stars: {repo['stargazers_count']}")
            print(f"Language: {repo['language']}")
            print("-" * 30)

if __name__ == "__main__":
    main() 