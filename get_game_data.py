import os
import json
import shutil
import sys
from subprocess import PIPE, run


search = 'game'
file_extension = '.go'
compile_command = ['go', 'build']

def find_all_game_paths(source):
    game_paths = []

    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if search in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)
        break

    return game_paths

def get_name_from_paths(paths, strip):
    new_names = []

    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(strip, '')
        new_names.append(new_dir_name)

    return new_names

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def copy_and_overwrite(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def make_json_metadata_file(path, game_dirs):
    data = {
        'game names': game_dirs,
        'number of games': len(game_dirs)
    }

    with open(path, 'w') as f:
        json.dump(data, f)


def compile_code(path):
    code_file_name = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(file_extension):
                code_file_name = file
                break
        break

    if code_file_name is None:
        return
    
    command = compile_command + [code_file_name]
    # run_command(command, path)    # must have go intepreter to run this command

def run_command(command, path):
    cwd = os.getcwd()
    os.chdir(path)

    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print(result)

    os.chdir(cwd)

def main(source, target):
    cwd = os.getcwd()
    sourcePath = os.path.join(cwd, source)
    targetPath = os.path.join(cwd, target)

    create_dir(targetPath)

    game_paths = find_all_game_paths(sourcePath)
    new_game_dirs = get_name_from_paths(game_paths, 'game')

    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(targetPath, dest)
        copy_and_overwrite(src, dest_path)
        compile_code(dest_path)
    
    json_path = os.path.join(targetPath, 'metadata.json')
    make_json_metadata_file(json_path, new_game_dirs)



if __name__ == '__main__':
    args = sys.argv
    print(args)

    if len(args) != 3:
        raise Exception('You must pass in source directory and target directory only.')
    
    source, target = args[1:]

    main(source, target)
    