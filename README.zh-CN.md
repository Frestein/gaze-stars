# 🌟 gaze-stars

[English](README.md) | [中文版](README.zh-CN.md)

这个 GitHub Action 可以通过查询 GitHub API 以获取你标星的仓库们，然后按星标列表排序生成 README。

你可以参考我的仓库 [Frestein/awesome-stars](https://github.com/frestein/awesome-stars)。您可以将其用作模板。

## 文档

### 配置方法

| Variable          | Description                                         | Default                                    |
| ----------------- | --------------------------------------------------- | ------------------------------------------ |
| `github-username` | 生成星标列表的 GitHub 用户名                        | /                                          |
| `git-message`     | 用于 Git 提交的提交信息                             | `chore(updates): updated entries in files` |
| `sort-by`         | 排序方式，`stars` 或 `updated`                      | `stars`                                    |
| `style`           | README 生成风格，`table` 或 `list`                  | `table`                                    |
| `template-path`   | 自定义 `README.md` 模板，[了解更多](#template-path) | `template/template.md`                     |
| `output-path`     | 输出文件名                                          | `README.md`                                |

#### `template-path`

默认模板路径为 `template/template.md`，您可以自定义模板路径，模板路径为相对路径，相对于仓库根目录。

生成 README 时，生成的内容会替换模板中的 `[[GENERATE HERE]]` 字样，对于其他部分不会有变动，所以你可以根据需要自定义模板。

#### `output-path`

默认输出文件名 `README.md`，您可以自定义输出文件名，输出文件名相对于仓库根目录。

## 示例

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

## 许可证

[MIT](LICENSE)
