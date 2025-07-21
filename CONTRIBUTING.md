# Contributing to Stacking PR

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for our commit messages. This leads to more readable messages that are easy to follow when looking through the project history.

### Commit Message Format

Each commit message consists of a **header**, a **body** (optional), and a **footer** (optional).

```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Type
Must be one of the following:

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- **refactor**: A code change that neither fixes a bug nor adds a feature
- **perf**: A code change that improves performance
- **test**: Adding missing tests or correcting existing tests
- **build**: Changes that affect the build system or external dependencies
- **ci**: Changes to our CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

#### Scope (Optional)
The scope should be the name of the module affected (e.g., `api`, `models`, `schemas`, `db`, `docker`).

#### Subject
- Use the imperative, present tense: "change" not "changed" nor "changes"
- Don't capitalize the first letter
- No period (.) at the end
- Maximum 50 characters

#### Body (Optional)
- Use the imperative, present tense
- Include motivation for the change and contrast with previous behavior
- Wrap at 72 characters

#### Footer (Optional)
- Reference issues and pull requests
- Breaking changes should start with `BREAKING CHANGE:`

### Examples

#### Simple feature addition
```
feat(api): add pagination to task list endpoint
```

#### Bug fix with description
```
fix(models): correct task completion status update

The is_completed field was not being properly updated when using
the PATCH endpoint. This commit ensures the field is correctly
validated and persisted to the database.

Fixes #123
```

#### Documentation update
```
docs(readme): update installation instructions for Docker
```

#### Code formatting
```
style: format code with black and fix import sorting
```

#### Breaking change
```
feat(api)!: change task API response format

BREAKING CHANGE: The task API now returns tasks wrapped in a
data object with metadata. Previous format:
[{task1}, {task2}]

New format:
{
  "data": [{task1}, {task2}],
  "total": 2,
  "page": 1
}
```

### Commit Message Examples to Avoid

❌ **Bad:**
- `Update formating` (typo, vague)
- `fix bugs` (too vague, no scope)
- `Added new feature` (past tense, capitalized)
- `Update import are correctly sorted` (grammar error)

✅ **Good:**
- `style: format code with black`
- `fix(api): handle empty task list response`
- `feat(models): add created_at timestamp to tasks`
- `chore: update dependencies to latest versions`

## Pre-commit Checklist

Before committing, ensure:

1. Code is formatted: `black app tests`
2. Imports are sorted: `isort app tests`
3. Code passes linting: `flake8 app`
4. Tests pass with coverage: `make test-cov`
5. Commit message follows the format above

## Setting Up Git Hooks (Optional)

To automatically check commit messages, you can set up a commit-msg hook:

```bash
#!/bin/sh
# Save as .git/hooks/commit-msg and make executable

commit_regex='^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .{1,50}$'

if ! grep -qE "$commit_regex" "$1"; then
    echo "Invalid commit message format!"
    echo "Format: <type>(<scope>): <subject>"
    echo "Example: feat(api): add task filtering endpoint"
    exit 1
fi
```

Make it executable:
```bash
chmod +x .git/hooks/commit-msg
```