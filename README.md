# Game Extraction Toolbox

CLI Tools for investigating game files and extracting known packages

## Requirements
- Python 3.7 - 3.11
  - This should be a final release, especially if on Windows / C++ build tools aren't installed
- PIPx

## Installation
### Quick (if Python and Pipx are already installed)
```
pipx install game-extraction-toolbox
```

### Full
#### Python 3.7+
Should be on Linux and MacOSX by default; for Windows, I recommend [Digital Ocean's tutorial](https://www.digitalocean.com/community/tutorials/install-python-windows-10)

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

## FAQ

### Why make this?
I want to get ROMs legally, or as legally as possible. I've bought cart readers, but these 'official' ROMs are often different or for platforms that aren't viable for cartridge dumping. I want this to be feasible for others as well.

### Why are you reimplementing others? Why Python?
Many solutions so far are written in Bash, Powershell, and Batch, none of which are not well suited to binary file manipulation. Some of these are documented in foreign languages. Many of these scripts haven't been updated in years. My ideal is that this CLI is useful for reasearching these packages and extracting them, and that common library improvements improve the extraction processes over time.

### Is this legal?
I am not a lawyer, but any good lawyer would probably tell you that 'It depends'. That said, this is an effort to be as legal as possible; this code doesn't download things you don't own, and I intend to leave decryption (bypassing copyright protection devices) out, which would be illegal under the DMCA. This is also at a weird intersection of older law, such as Fair Use, which generally - in most jurisdictions - has some protections for format-shifting. That's largely the point of this - ROMs are flexible and can be played on $20 cheap handhelds, phones, Steam Decks, PCs, tablets, Chromebooks, web pages, etc.

### Why not just play the official release?
I prefer not to be artificially locked to specific platforms - why play a 25 year old arcade title on my Steam PC that my phone can easily handle? Furthermore, some official releases are... not great. Subpar emulation on lower-end PCs, slow loading and menus, older MAME runtimes with known issues - we can do better.

### Why not just download the ROMs?
It is illegal. One can discuss economic moral implications all day, but at the end of the day, it's theft. As a software developer myself, I don't want my code stolen - so I can't claim a moral high ground there. Equally importantly, showing classic game owners that the market will support rereleases increases the liklihood of rereleases, and I want people who can't/won't download ROMs to enjoy these titles as well.


## Collections

**Collection**                             | **Status**     | **Notes**                                                               
---------------------------------|-------------|---------------------------------------------------------------------
 **Capcom Arcade Stadium 1**                    | 95%    | Requires Steam depot downloading, a couple shaky ROMs...
 **Capcom Beat 'Em Up Bundle**                  | 95%    | 6/7 playable on some version of MAME, but wof/wofj missing audiocpu data
 **Capcom Fighting Collection**                 | 90%    | CPS2 is semi-standard. No Enc keys present. CP3 game is a curveball!
 **Street Fighter 30th Anniversary Collection** | 100%   | All games are playable with some version of MAME!
 **Sega Genesis and Mega Drive Collection**     | 90%    | Some compressed variants not yet extracted
