## Development
### Setup
1. Clone Repo
2. Run ```pip install -e --user .``` from the root project folder


## Deployment
### Setup
1. Install pipx (see README)
2. Install twine ```pipx install twine```
3. Install build ```pipx install build```

### Publish
1. Test via 'pip install -e --user .' if this isn't already the active copy
2. Update version number (in pyproject.toml) and CHANGELOG.md
2. Clean out dist folder
3. Build via 'py -m build'
4. Distribute via 'twine upload dist/*'
5. Clean out dist