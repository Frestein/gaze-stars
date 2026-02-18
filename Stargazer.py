#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# @Author    : Arthals (huozhiyongde@126.com)
# @Co-author : Frestein (frestein@tuta.io)

import json
import os
import re

import requests


class Stargazer:
    def __init__(self):
        self.username = os.getenv("GITHUB_USERNAME")
        self.token = os.getenv("GITHUB_TOKEN")
        self.template = os.getenv("TEMPLATE_PATH", "template/template.md")
        self.output = os.getenv("OUTPUT_PATH", "README.md")
        self.sort_by = os.getenv("SORT_BY", "stars").lower()
        self.style = os.getenv("STYLE", "table").lower()
        self.star_lists = []
        self.star_list_repos = {}
        self.data = {}

    def get_all_starred(self):
        url = f"https://api.github.com/users/{self.username}/starred?per_page=100"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "Stargazer",
        }
        all_repos = {}
        while url:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            for repo in response.json():
                all_repos[repo["full_name"]] = {
                    "html_url": repo["html_url"],
                    "description": repo["description"] or "",
                    "listed": False,
                    "stars": repo["stargazers_count"],
                }
            url = response.links.get("next", {}).get("url")
        self.data = all_repos
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(all_repos, f, indent=4, ensure_ascii=False)
        return all_repos

    def get_lists(self):
        url = f"https://github.com/{self.username}?tab=stars"
        response = requests.get(url)
        pattern = rf'href="/stars/{self.username}/lists/(\S+)"[\s\S]*?<h3 class=".*?">(.*?)</h3>'
        match = re.findall(pattern, response.text, re.DOTALL)
        self.star_lists = [(url, name.strip()) for url, name in match]
        return self.star_lists

    def get_list_repos(self, list_name):
        url = "https://github.com/stars/{username}/lists/{list_name}?page={page}"
        page = 1
        while True:
            current_url = url.format(
                username=self.username, list_name=list_name, page=page
            )
            response = requests.get(current_url)
            pattern = r'<h2 class="h3">\s*<a href="[^"]*">\s*<span class="text-normal">(\S+) / </span>(\S+)\s*</a>\s*</h2>'
            match = re.findall(pattern, response.text)
            if not match:
                break
            if list_name not in self.star_list_repos:
                self.star_list_repos[list_name] = []
            self.star_list_repos[list_name].extend(match)
            page += 1
        return self.star_list_repos[list_name]

    def get_all_repos(self):
        for list_url, _ in self.star_lists:
            self.get_list_repos(list_url)
        return self.star_list_repos

    def remove_emojis(self, data):
        emoj = re.compile(
            "["
            "\U0001f600-\U0001f64f"
            "\U0001f300-\U0001f5ff"
            "\U0001f680-\U0001f6ff"
            "\U0001f1e0-\U0001f1ff"
            "\U00002500-\U00002bef"
            "\U00002702-\U000027b0"
            "\U000024c2-\U0001f251"
            "\U0001f926-\U0001f937"
            "\U00010000-\U0010ffff"
            "\u2640-\u2642"
            "\u2600-\u2b55"
            "\u200d"
            "\u23cf"
            "\u23e9"
            "\u231a"
            "\ufe0f"
            "\u3030"
            "]+",
            re.UNICODE,
        )
        return emoj.sub("", data)

    def generate_readme(self):
        text = ""

        contents_lines = []
        contents_lines.append("## Contents")
        for _, list_name in self.star_lists:
            clean_name = self.remove_emojis(list_name)
            anchor = clean_name.lower().replace(" ", "-")
            contents_lines.append(f"- [{list_name}](#{anchor})")
        contents_lines.append("")

        if self.style == "list":
            body_lines = []
            for _, list_name in self.star_lists:
                body_lines.append(f"## {list_name}")
                repos = []
                for user, repo in self.star_list_repos.get(_, []):
                    full_name = f"{user}/{repo}"
                    if full_name in self.data:
                        repos.append((full_name, self.data[full_name]))
                if not repos:
                    body_lines.append("- No repositories")
                else:
                    for full_name, repo_data in repos:
                        desc = repo_data["description"].replace("|", "\\|")
                        body_lines.append(
                            f"- [{full_name}](https://github.com/{full_name}) - {desc}"
                        )
                body_lines.append("")
            text = "\n".join(contents_lines) + "\n" + "\n".join(body_lines)

        else:
            text += "\n".join(contents_lines) + "\n\n"
            for _, list_name in self.star_lists:
                text += f"## {list_name}\n\n"
                text += "| Repository | Description | Stars |\n"
                text += "|------------|-------------|-------|\n"
                repos = []
                for user, repo in self.star_list_repos.get(_, []):
                    full_name = f"{user}/{repo}"
                    if full_name in self.data:
                        repos.append((full_name, self.data[full_name]))
                if not repos:
                    text += "| *No repositories* | | |\n"
                else:
                    repos_sorted = sorted(
                        repos, key=lambda x: x[1]["stars"], reverse=True
                    )
                    for full_name, repo_data in repos_sorted:
                        desc = repo_data["description"].replace("|", "\\|")
                        stars = repo_data["stars"]
                        text += f"| [{full_name}](https://github.com/{full_name}) | {desc} | ⭐{stars} |\n"
                text += "\n"

        with open(self.template, "r", encoding="utf-8") as f:
            template = f.read()
        with open(self.output, "w", encoding="utf-8") as f:
            f.write(template.replace("[[GENERATE HERE]]", text.strip()))


if __name__ == "__main__":
    stargazer = Stargazer()
    stargazer.get_all_starred()
    stargazer.get_lists()
    stargazer.get_all_repos()
    stargazer.generate_readme()
