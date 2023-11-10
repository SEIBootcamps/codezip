# codezip

Build `.zip` archives of materials to be distributed to students. Use this to zip up
lecture demos, starter code, solution code, etc.

Automatically ignores files exluded by `.gitignore` and `.codezipignore`!

## Usage

Install with your favorite package manager:

```
FIXME
```

Then, use `zip_code`:

```python
from codezip import zip_code

zip_code("react-1-solution.zip", "contents/exercises/react-1/solution")
```

### Ignore files with `.codezipignore`

Works just like `.gitignore` (except it doesn't support globs that start with `!`).
