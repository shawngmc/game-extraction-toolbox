## Capcom Arcade Stadium 1 - Game ID 1515950 - Old version

Pulling CAS1 via old Steam Depots:

The notes I found were at https://retropie.org.uk/forum/topic/10918/where-to-legally-acquire-content-to-play-on-retropie/606?lang=en-US. 
Essentially, while a new version was added to steam, the old version can be specifically downloaded.
You can pull these by visiting steam://nav/console (this opens a hidden CLI within Steam), then using the command 'download_depot <GameID> <DepotID> <ManifestID>'
This will download them into your Steam folder, under steamapps\content\app_<GameID>\depot_<DepotID>
An easier tool to pull the old versions can be found here: https://github.com/SteamRE/DepotDownloader

After that, this script will extract and prep the ROMs. Some per-rom errata are in the notes below.

 **Game**                             | **DepotID**     | **ManifestID**          | **MAME Ver.**     | **FB Neo**     | **ENG Filename**     | **ENG CRC**     | **JP Filename**     | **JP CRC**     | **Notes**  
---------------------------------|-------------|---------------------|---------------|------------|------------------|-------------|-----------------|------------|-----------  
 **Powered Gear**                     | 1556723     | 305464856399220085  | MAME 0.139    | Y          | pgear.zip        | OK          | N/A             | N/A        | (1)       
 **Warriors of Fate**                 | 1556720     | 4950348891858375781 | MAME 0.139    | Y          | wofu.zip         | Bad         | wofj.zip        | Bad        | (1)       
 **Senjo no Okamill**                 | 1556714     | 4064909307706647901 | MAME 0.139    | N          | N/A              | N/A         | mercsj.zip      | Bad        | (1)       
 **Captain Commando**                 | 1556718     | 2975445377289899248 | MAME 0.246    | Y          | captcomm.zip     | OK          | captcommj.zip   | OK         |           
 **Street Fighter II**                | 1556717     | 7823458246757484640 | MAME 0.246    | Y          | sf2um.zip        | OK          | sf2jl.zip       | OK         |           
 **Varth Operation Thunderstorm**     | 1556719     | 2957041054036881699 | MAME 0.246    | Y          | varth.zip        | OK          | varthj.zip      | OK         |           
 **1942**                             | 1556702     | 7110820738848130277 | MAME 0.246    | Y          | 1942.zip         | OK          | N/A             | OK         |           
 **Bionic Commando**                  | 1556707     | 3238877912290772385 | MAME 0.246    | Y          | bionicc2.zip     | OK          | N/A             | OK         |           
 **Commando**                         | 1556703     | 5154503909431550517 | MAME 0.246    | EN         | commandou.zip    | OK          | commandoj.zip   | Bad        | (2)       
 **Dynasty Wars**                     | 1556711     | 5906401061810674850 | MAME 0.246    | Y          | dynwar.zip       | OK          | dynwarj.zip     | OK         |           
 **Final Fight**                      | 1556712     | 1427558570204465271 | MAME 0.246    | N          | ffightu.zip      | Bad         | ffightj.zip     | Bad        | (2)       
 **Forgotton Worlds**                 | 1556708     | 2495421590891474725 | MAME 0.246    | EN         | forgottnuaa.zip  | OK          | lostwrld.zip    | Bad        | (2)       
 **Ghouls 'n Ghosts**                 | 1556709     | 7553746399143380961 | MAME 0.246    | Y          | ghoulsu.zip      | OK          | daimakai.zip    | OK         |           
 **Ghosts 'n Goblins**                | 1556690     | 5034024650887104340 | MAME 0.246    | Y          | gng.zip          | OK          | makaimurg.zip   | OK         |           
 **Pirate Ship Higemaru**             | 1556701     | 3568513687229079528 | MAME 0.246    | Y          | higemaru.zip     | OK          | N/A             | N/A        |           
 **Legendary Wings**                  | 1556706     | 8788446018740704096 | MAME 0.246    | Y          | lwings.zip       | OK          | lwingsja.zip    | OK         |           
 **Mega Twins**                       | 1556715     | 7832027131156162352 | MAME 0.246    | JP         | mtwins.zip       | Bad         | chikij.zip      | OK         | (2)       
 **Section Z**                        | 1556704     | 7517264779277019420 | MAME 0.246    | Y          | sectionza.zip    | OK          | N/A             | N/A        |           
 **Strider**                          | 1556710     | 8512960795726908906 | MAME 0.246    | EN         | striderua.zip    | OK          | striderjr.zip   | Bad        | (2) (3)   
 **Street Fighter II Hyper Fighting** | 1556721     | 317521835646003561  | MAME 0.246    | Y          | sf2hfu.zip       | OK          | sf2hfj.zip      | OK         |           
 **Tatakai no Banka**                 | 1556705     | 7200344018849026230 | MAME 0.246    | N          | N/A              | N/A         | trojanj.zip     | Bad        | (2)       
 **Vulgus**                           | 1556700     | 9143855046040096923 | MAME 0.246    | N          | vulgus.zip       | Bad         | vulgusj.zip     | Bad        | (2)       
 **US Navy: Carrier Air Wing**        | 1556716     | 187920547906050452  | MAME 0.246    | N          | cawingu.zip      | Bad         | cawingj.zip     | Bad        | (2)       
 **Cyberbots: Fullmetal Madness**     | 1556724     | 4293976514552436962 | MAME 0.139    | N          | cybotsu.zip      | OK          | cybotsj.zip     | OK         | (1)       
 **19XX: The War Against Destiny**    | 1556725     | 4171961223274458606 | MAME 0.139    | N          | 19xx.zip         | Bad?        | 19xxj.zip       | Bad?       | (1) (4)   
 **Battle Circuit**                   | 1556726     | 5500917457208551111 | MAME 0.139    | N          | batcir.zip       | OK          | batcirj.zip     | OK         | (1)       
 **Giga Wing**                        | 1556727     | 1585945610334979859 | MAME 0.139    | N          | gigawing.zip     | OK          | gigawingj.zip   | OK         | (1)       
 **1944: The Loop Master**            | 1556728     | 3525105251099559918 | MAME 0.139    | N          | 1944.zip         | OK          | 1944j.zip       | OK         | (1) (4)   
 **Progear**                          | 1556729     | 6184184127241976915 | MAME 0.139    | N          | progear.zip      | OK          | progearj.zip    | OK         | (1)       
 **1941: Counter Attack**             | 1556713     | 2745567461535328718 | MAME 0.246    | Y          | 1941u.zip        | OK          | 1941j.zip       | OK         | (7)       
 **Super Street Fighter II Turbo**    | 1556722     | 2744654918197522324 | MAME 0.139    | N          | ssf2tu.zip       | OK          | ssf2xj.zip      | Bad        | (1)       
 **1943: The Battle of Midway**       | 1515951     | 1597238681896386079 | N/A           | EN         | 1943u.zip        | OK          | 1943j.zip       | BAD        | (5)       
 **3 Wonders**                        | 1556709     | 7553746399143380961 | MAME 0.246    | Y          | 3wondersu.zip    | OK          | N/A             | N/A        | (6)       




1. These ROMs require an older version MAME. They test fine in MAME 0.139 (Mame 2010 in RetroArch). This is typically due to a missing decryption key, dl-1425.bin qsound rom, or other ROM files that the older MAME did not strictly require
2. These ROMs play fine, even in the current MAME, despite the bad CRCs. This is likely due to Capcom redumping or making a minor modification to omit copyright/trademark material.
3. This ROM specifically complains about a bad dump on a specific file; it still plays OK.
4. This ROM is using an older naming convention to help allow emulation in the older MAME it requires.
5. Embedded in main package; JP version is missing too much, but US version can run in FB Neo
6. Embedded in a specific depot of Ghouls n Ghosts
7. Includes extra ROM 1941.zip; same solid compatibility