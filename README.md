# 🌟 gaze-stars

[English](README.md) | [中文版](README.zh-CN.md)

This GitHub Action queries the GitHub API to retrieve your starred repositories and generates a README sorted by your stargazed list.

You can reference my repository [Frestein/awesome-stars](https://github.com/frestein/awesome-stars).

## Documentation

### Prerequisites

- An empty repository
- A personal GitHub API token

### Configuration

| Variable          | Description                                                   | Default                                    |
| ----------------- | ------------------------------------------------------------- | ------------------------------------------ |
| `github-username` | GitHub username for generating starred list                   | /                                          |
| `git-message`     | Commit message for Git commits                                | `chore(updates): updated entries in files` |
| `sort-by`         | Sort by `stars` or `updated`                                  | `stars`                                    |
| `style`           | Style of README generation (`table` or `list`)                | `table`                                    |
| `template-path`   | Custom `README.md` template path [Learn more](#template-path) | `template/template.md`                     |
| `output-path`     | Output filename                                               | `README.md`                                |

#### `template-path`

The default template path is `template/template.md`. You can customize the template path (relative to repository root).

The generated content will replace the `[[GENERATE HERE]]` placeholder in the template while preserving other content.

#### `output-path`

Default output file name is `README.md`. You can customize the output path (relative to repository root).

## Example

```yml
name: Update by list
on:
  workflow_dispatch:
  schedule:
    - cron: "0 0 * * *"
jobs:
  update-by-list:
    runs-on: ubuntu-latest
    steps:
      - name: Update repo category by list
        uses: Frestein/gaze-stars@v1.3.0
        with:
          github-username: ${{ github.repository_owner }}
          git-message: "docs(list): bump data"
          sort-by: stars
          style: list
          template-path: .github/templates/template.md
          output-path: README.md
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## License

[MIT](LICENSE)
