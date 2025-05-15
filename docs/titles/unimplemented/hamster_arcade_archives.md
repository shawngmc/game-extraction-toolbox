# Hamster Arcade Archives
## Windows Store
While there are tools to find the download URLs for the Windows Store packages, these are encrypted .eappx packages.

These are installed in C:\Program Files\WindowsApps\. This folder is hidden; however, revealing it and taking ownership in Windows Explorer/Powershell/etc. is still not enough for these titles. The executable - which appears to have all substantial game content - is protected via Windows Encrpyted File System. The file has a lock overlay on the icon, and any attempts to open/copy it yield 'Access is denied'.

[UWPDumper](https://github.com/Wunkolo/UWPDumper), however, allows us to bypass this.

1) Buy the appropriate app and install it.
2) Start the app.
3) Run UWPDumper, then find the HAMSTER process in the list.
   (There may be multiple; if one fails, reopen the list and choose another.)
4) It will hook into the process and pull all files into a special folder.

At this point, the executable is the only reasonably large file, and there's no clear data structure that looks like a ROM at this time. The other remaining concern is size; for example, Metal Slug 4's basic ROM, compressed in ZIP, is well over 50MB, but the executable is only 34MB. 

Unlike Arcade Classics Anniversay Collection (which is Konami but powered by Arcade Archives), there are no obvious Gzip blobs to decompress.