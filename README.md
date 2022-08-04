# Game Extraction Toolbox

CLI Tools for investigating game files and extracting known packages

## Requirements
- Python 3.7+
- PIPx

## Installation
### Quick (if Python and Pipx are already installed)
```
pipx install game-extraction-toolbox
```

### Full
#### Python 3.7+
Should by on Linux and MacOSX by default; for Windows, I recommend [Digital Ocean's tutorial](https://www.digitalocean.com/community/tutorials/install-python-windows-10)

#### PIPX

##### Windows
```
py -m pip install --user pipx
py -m pipx ensurepath
```

##### Linux
```
py -m pip install --user pipx
py -m pipx ensurepath
```

##### MacOSX
```
brew install pipx
pipx ensurepath
```


## Usage
```gametoolbox --help```
You can get --help on any command or subcommand, for example:
```gametoolbox file --help```