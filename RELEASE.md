# Release workflow

As a reminder to self, to release:
  1. Bump the version in `setup.py`
  2. Commit to master with a message something like "prepare 1.2.3 release"
  3. Add a "v1.2.3" tag with `git tag -a <tag name> REVISION`
  4. Release from GitHub with "v1.2.3" as title (this will trigger the release action)
