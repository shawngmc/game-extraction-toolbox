## Development
### Setup
1. Clone Repo
2. Run ```pip install -e --user .``` from the root project folder


## Deployment
### Setup
1. Install pipx (see README)
2. Install twine ```pipx install twine```
3. Install build ```pipx install build```

### Prep
1. Pre-test via local install (```pip install --user -e .```)
2. Update version number (in pyproject.toml) and CHANGELOG.md

### Build
1. Clean out dist dir
2. Build via ```py -m build```

### Test
1. Push to develop
2. Install via ```pipx install git+https://github.com/shawngmc/game-extraction-toolbox.git@develop```
  * Uninstall first if necessary!
3. Try running
4. Uninstall via ```pipx uninstall game-extraction-toolbox```
  * Reconfigure for local dev via ```pip install --user -e .```

### Publish
1. Distribute via twine ```twine upload dist/*```
2. Clean out dist dir

## TODO: Transition to release-based builds - GH Action in place, needs tested!