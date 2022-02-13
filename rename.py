from os import listdir, rename, getcwd
from os.path import isfile, join
import re
import json
import argparse

# load_episodes_reference_file takes the reference file path
# and returns a JSON object of it.
def load_episodes_reference_file(reference_file):
    with open(reference_file) as f:
        try:
            episode_mapping = json.load(f)
        except ValueError as e:
            print("Failed to load the episode reference file \"{}\": {}".format(reference_file, e))
            exit

    return episode_mapping


# list_mkv_files_in_directory returns all the files in the specified
# directory that have the .mkv extention
def list_mkv_files_in_directory(directory):
    return [f for f in listdir(directory) if (isfile(join(directory, f)) and "mkv" in f)]


# generate_new_name_for_episode parses the original one pace file name
# and tries to match it with the reference episodes. 
# It returns the new name the file should have
def generate_new_name_for_episode(original_file_name, episode_mapping, reference_file):
    reg = re.search(r'\[One Pace\]\[.*\] (.*?) (\d\d?) \[(\d+p)\].*\.mkv', original_file_name)

    if (reg is None):
        raise ValueError("File \"{}\" didn't match the regex".format(original_file_name))

    arc_name = reg.group(1)
    arc_ep_num = reg.group(2)
    resolution = reg.group(3)

    arc = episode_mapping.get(arc_name)
    if (arc is None):
        raise ValueError("\"{}\" Arc not found in file {}".format(arc_name, reference_file))

    episode_number = arc.get(arc_ep_num)
    if ((episode_number is None) or (episode_number == "")):
        raise ValueError("Episode {} not found in \"{}\" Arc in file {}".format(arc_ep_num, arc_name, reference_file))

    return "One.Piece.{}.{}.mkv".format(episode_number, resolution)


def main():
    parser = argparse.ArgumentParser(description='Rename One Pace files to a format Plex understands')
    parser.add_argument("-rf", "--reference-file", nargs='?', help="Path to the episodes reference file", default="episodes-reference.json")
    parser.add_argument("-d", "--directory", nargs='?', help="Data directory (aka path where the mkv files are)", default=None)
    parser.add_argument("--dry-run", action="store_true", help="If this flag is passed, the output will only show how the files would be renamed")
    args = vars(parser.parse_args())

    if args["directory"] is None:
        args["directory"] = getcwd()

    episode_mapping = load_episodes_reference_file(args["reference_file"])
    video_files = list_mkv_files_in_directory(args["directory"])

    if len(video_files) == 0:
        print("No mkv files found in directory \"{}\"".format(args["directory"]))

    for file in video_files:
        try:
            new_episode_name = generate_new_name_for_episode(file, episode_mapping, args["reference_file"])
        except ValueError as e:
            print(e)
            continue

        if args["dry_run"]:
            print("DRYRUN: \"{}\" -> \"{}\"".format(file, new_episode_name))
            continue
        
        rename(file, new_episode_name)

if __name__ == "__main__":
    main()