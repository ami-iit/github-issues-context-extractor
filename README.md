# github-issues-context-extractor

Simple utility to extract issues and pull requests from a GitHub repo in a single `.json` file, that can be passed to Large Language Models (LLMs).

> [!CAUTION]
> Always pay attention to avoid passing confidential information to a cloud-hosted LLMs.

## Installation

To run the command, make sure that you have [`pixi`](https://pixi.sh) installed and then just clone the repo and run:

```bash
git clone https://github.com/ami-iit/github-issues-context-extractor
cd github-issues-context-extractor
pixi run github-issues-context-extractor
```

You can also run the `github-issues-context-extractor` command without `pixi run` before by running `pixi shell`:

```bash
pixi shell
github-issues-context-extractor
```

Otherwise, just install it from source using `pip` or `uv`, in that case there is no need to have pixi installed, and then run the utility as `github-issues-context-extractor`.

> [!NOTE]
> To run the `github-issues-context-extractor` you need a GitHub Token. If you log in GitHub via the `gh auth` utility, the correct token will be automatically used, otherwise you can export the token you want to use via the `GITHUB_TOKEN` environment variable.


## Usage

To download all the issues of the repo `ami-iit/github-issues-context-extractor` in a file `this_repo_issues.json`, run:

```bash
pixi run github-issues-context-extractor --repo ami-iit/github-issues-context-extractor --output_file this_repo_issues.json
```

You can also pass a query to filter the issues, for example to get all the issues and prs created in October 2024:

```bash
pixi run github-issues-context-extractor --repo ami-iit/github-issues-context-extractor --query "created:>2024-09-01 created:<2024-10-31" --output_file this_repo_issues.json
```

The commands allowed in the query are the one that GitHub allows in its search, check the docs at https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/filtering-and-searching-issues-and-pull-requests for more details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[BSD-3-Clause](https://spdx.org/licenses/BSD-3-Clause.html)
