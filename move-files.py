import fnmatch
import os
import shutil

xml_files_pattern = '*.xml'

source_folder = '---'
destination_folder = '---'


def get_xml_files():
    return [os.path.splitext(file)[0] for file in os.listdir(source_folder) if fnmatch.fnmatch(file, xml_files_pattern)]


def move():
    all_files = sorted(os.listdir(source_folder))
    print("all files len: {}".format(len(all_files)))

    for file in all_files:
        if os.path.splitext(file)[0] in get_xml_files():
            shutil.move(source_folder + file, destination_folder)

    choosed_files = sorted(os.listdir(destination_folder))
    print("choosed files len: {}".format(len(choosed_files) / 2))


# TODO create function to find uncured file...

if __name__ == '__main__':
    move()
