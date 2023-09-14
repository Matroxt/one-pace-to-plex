# One Pace To Plex
This project helps adapts the [One Pace](https://onepace.net/) releases to a format Plex can leverage, without the need to create an "Other videos" library just for One Piece. That way you can have One Piece along with you other animes.

You can visualize what it looks like in the images directory:
- Seasons are actually arcs, not TVDB seasons
- Episodes contains the metadata anyway

This project is not endorsed by the One Pace team, but I figured I might as well share the automation work if someone wanted to do the same.

## Before you begin
There are a few requirements to make this work:

1.  Install the [Absolute-Series-Scanner (ASS)](https://github.com/ZeroQI/Absolute-Series-Scanner) which has the job to map the files to the right episodes and seasons.
    1. Locate the [Plex system folder](https://github.com/ZeroQI/Absolute-Series-Scanner#plex-system-folder-location)
    2. Create the `Scanners/Series` in the `Plex Media Server` directory (eg: `/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Scanners/Series`)
    3. [Download the scanner](https://raw.githubusercontent.com/ZeroQI/Absolute-Series-Scanner/master/Scanners/Series/Absolute%20Series%20Scanner.py) (it's a python file), and place it in the directory created on step 2.
    4. If using Linux, make sure to change the permissions of that file so that Plex can use it. In doubts, refer to their [installation instructions](https://github.com/ZeroQI/Absolute-Series-Scanner#install--update)

2.  Install the [HAMA plugin](https://github.com/ZeroQI/Hama.bundle) whose job it is to get the metadata one the episodes.
    1. Follow their [installation instructions](https://github.com/ZeroQI/Hama.bundle#installation), but TL;DR, download the zip file of the repo and place it in the `Plug-ins` folder inside the `Plex Media Server` directory (or `git clone` the repo in that directory)

3.  Restart Plex

4.  Verify the installation, open your Anime library in Plex > Edit > Advanced. In the "Scanner" dropdown, you should be able to select "Absolute Series Scanner" and in the "Agent" dropdown, you should see HamaTV.

5.  For later in the turorial, you'll need Python3 installed on your computer to rename the files, but it can also be done with Docker

I highly recommend to have a look at Absolute-Series-Scanner/HAMA plugin as they can improve your Plex game to another level when used properly.


## Setting up One Pace in Plex

### 1. Folder structure
1.  As usual with Plex, the folder structure and naming is very important. Here's the one we'll be using
    ```
    └───media
        ├───anime
        │   ├───One Piece [tvdb4-81797]
        │   │   ├───Arc 01 - Romance Dawn
        │   │   │   ├───tvdb4.mapping
        │   │   │   └───One.Piece.E1.1080p.mkv
        │   │   ├───Arc 02 - Orange Town
        │   │   ├───Arc XX
        │   │   └───Arc 32 - Wano
        │   └───Other Anime
        ├───audiobooks
        │   └───An audiobook (1971)
        ├───movies
        │   └───A Movie (1970)
        └───tvshows
    ```

2.  Please note the "[tvdb4-81797]" that is added to the "One Piece" folder name. ASS is able to leverage that to enable customs seasons. In the case of One Piece, it allows us to group the different arcs as if they were seasons instead of using the ones provided by TVDB.

3. In each arc directory, place the `tvdb4.mapping` file. (You could also not use the arcs directory and keep all you episodes in the same folder, and have the `tvdb4.mapping` directly in the `One Piece [tvdb4-81797]` folder)

### 2. File renaming - No Directories
For Plex to be able to fetch the metadata of the episodes, we need to rename them to something that can be matched via the HAMA agent.
1.  Open a shell/powershell terminal.

2.  Change directory to the place where your One Pace mkv files are: `cd /path/to/my/mkv/folder`
    To make your life easier, you might want to move those files in the relevant arc directory before renaming.

3.  Copy the `rename.py` and `episodes-reference.json` and `chapters-reference.json` file in that directory

4.  Run the script in dry-run mode to see what change would occur (you can try with Docker or Python):
    1. Python: `python rename.py --dry-run`
    2. Docker: `docker run --rm -v "$PWD":/data -w="/data" python:3 python rename.py --dry-run`

5.  Once you are okay with the changes you see, remove the `--dry-run` flag from the command and run it again.
    Your files will be renamed to the corresponding One Piece epidode, eg:
    - `[One Pace][3-5] Romance Dawn 03 [1080p][F5E73C4E].mkv` --> `One.Piece.E3.1080p.mkv`
    - `[One Pace][677-678] Punk Hazard 12 [720p][CD83F1E9].mkkv` --> `One.Piece.E603-E604.720p.mkv`
    - `[One Pace] Chapter 700-701 [720p][2A35B710].mkv` -> `One.Piece.E628-E630.720p.mkv`

6.  If not done in step 2.2, move the resulting mkv files in their respective arc directory (or all in the `One Piece [tvdb4-81797]` directory if you don't care about organizing your files)

### 2.5 File Renaming - With a directory structure
If the files are already in their respective folder structure (see step 1) you can use the `-sd` or `--sub-dir` flag to inform the script to search sub directories
1.  Open a shell/powershell terminal.

2.  Change directory to the directory that contains your folder structure (e.g. `One Piece [tvdb4-81797]`)

3.  (optional) Copy the `rename.py` and `episodes-reference.json` and `chapters-reference.json` file in that directory

4.  Run the script in dry-run mode with the subdirectory flag to see what change would occur

    1.  If you did step 3: `python rename.py -sd --dry-run`
    2.  Or specify directory `python rename.py -d "/path/to/one/pace/files" -sd --dry-run`

5.  Once you are okay with the changes you see, remove the `--dry-run` flag from the command and run it again.
    Your files will be renamed to the corresponding One Piece epidode, eg:
    - `[One Pace][3-5] Romance Dawn 03 [1080p][F5E73C4E].mkv` --> `One.Piece.E3.1080p.mkv`
    - `[One Pace][677-678] Punk Hazard 12 [720p][CD83F1E9].mkkv` --> `One.Piece.E603-E604.720p.mkv`
    - `[One Pace] Chapter 700-701 [720p][2A35B710].mkv` -> `One.Piece.E628-E630.720p.mkv`

### 3. Plex library
1.  Make sure the Plex library that has One Piece in it uses ASS as the scanner and HAMA as the agent. Scan the library.
2.  If it's not picking it up properly, check:
    1. Make sure the directory structure of Step 1 is followed and that the `tvdb4.mapping` file is present in the arcs directories.
    2. Do the [Plex Dance](https://forums.plex.tv/t/the-plex-dance/197064)

## Disclaimer
Obviously, this project does not condone piracy, you should own the media (DVD/BD/..) you consume.

For contributions/constructive comments, feel free to open an issue on the Github page.

## TODO
- Craft posters for each arc and commit them to the repo. Placed properly, they could be picked up by HAMA automatically.