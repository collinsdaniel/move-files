import fnmatch
import os
import shutil

xml_files_pattern = '*.xml'

source_folder = '/Users/collins/Documentos/QwertAI/labs/faceDetect/curadoria/imagens-curadas/'
destination_folder = '/Users/collins/Documentos/QwertAI/labs/faceDetect/curadoria/imagens-curadas/'


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


def locate():
    files = sorted(os.listdir(destination_folder))
    print("files: ", files)
    for file in files:
        # print("file: {}".format(file))
        if os.path.splitext(file)[0] not in get_xml_files():
            print("file not exist xml: {}".format(file))


if __name__ == '__main__':
    locate()
