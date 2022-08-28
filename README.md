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

### This MAME ROM is actually XXXXYY, not XXXXZZ - why do you have it that way?
The goal of this tool is not to create a perfect ROM set for the latest MAME, because it can't. A few factors go into what version of MAME we target:

* What version of MAME did the rerelease use?
* Are there missing files, like encryption keys or dl-1425.bin, that force us to target a different version of MAME to make a ROM that is usable out of the box?
* When did MAME split specific collections?
* What are file CRCs?
* Did the rerelease modify files for legal/moral reasons?
* How can we make a playable ROM?

For example, let's use Street Fighter 30th Anniversary Collection's copy of Street Fighter Alpha 2. It's technically both sfa2u and sfa2ur1, and neither! Here's why, using Arcade Italia's [SFA2U](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=sfa2u) and [SFA2UR1](http://adb.arcadeitalia.net/dettaglio_mame.php?game_name=sfa2ur1) as a source:

1. The primary difference between these two ROMs is maincpu, like sz2u.03.
2. At first glance, this looks like sfa2ur1, because the sz2u.03 we create has a CRC of 84a09006. Case closed, right?
3. Well, not so fast. If we make a sfa2ur1 or sfa2u zip file, neither are natively playable in MAME 0.246, because we don't have the sfa2u.key or dl-1425.bin.
4. The standard solution here - since this project will not add copyrighted material not in the source - is to target an older version of MAME, 0.139 (aka Mame 2010 in RetroArch). Except... sfa2ur1 didn't exist until MAME 0.141!
5. We then look at sfa2u before the split. Lo and behold, sz2u.03 has the CRC of 84a90006. OK, so it's sfa2u, right?
6. Kinda. The gfx CRCs don't match EITHER ROM. This is most likely because Capcom modified the graphics to remove copyrighted or offensive content. However, there's no MAME clone with the gfx CRCs we have.
7. Since our goal is to make a playable ROM, not a perfect one, we can test the ROM in MAME 0.139. It works, so we'll call it sfa2u, but make a note in the documentation for that command.

These are noted in the documentation for each script. If you think a ROM is misidentified, please:

1. Search for a closed issue - these will likely be brought up multiple times!
2. If none exists, use a source like [Arcade Italia](http://adb.arcadeitalia.net/) to verify. Make sure you look at the original file we create, and watch for the following things:
  * The MAME version we target
  * Any missing files
  * When a ROM was split
  * CRCs for every file
3. If you are solidly convinced that there's a misnaming, open a ticket and we'll take a look.


## Collections

**Collection**                             | **Status**     | **Notes**           
--------------------------------------------|-------------|---------------------------------------------------------------------  
 **Blizzard Arcade Collection**                 | 100%   |   
 **Bubsy Two-Fur**                              | 100%   |   
 **Capcom Arcade Stadium 1**                    | 95%    | Requires Steam depot downloading, a couple shaky ROMs...  
 **Capcom Beat 'Em Up Bundle**                  | 95%    | 6/7 playable on some version of MAME, but wof/wofj missing audiocpu data  
 **Capcom Fighting Collection**                 | 90%    | CPS2 is semi-standard. No Enc keys present. CP3 game is a curveball!  
 **Collection of SaGa/Final Fantasy Legend**    | 100%   |  
 **Disney Afternoon Collection**                | 100%   |  
 **Disney Classics Aladdin & Lion King w/DLC**  | 100%   | Includes Jungle Book DLC
 **Double Dragon Trilogy**                      | 100%   |  
 **Mega Man Legacy Collection 1**               | 100%   |  
 **Mega Man X Legacy Collection 1**             | 75%    | X4 doesn't appear to be ROM based  
 **Sega Genesis and Mega Drive Collection**     | 90%    | Some compressed variants not yet extracted  
 **Sonic Adventure DX (Hidden Game Gear games)**| 100%   | This is only the Game Gear games - SADX itself can not be made into a ROM/ISO!
 **SNK 40th Anniversary Collection**            | 80%    | A bunch of games are missing PROMs
 **Street Fighter 30th Anniversary Collection** | 90%    | Now includes all playable international versions.
