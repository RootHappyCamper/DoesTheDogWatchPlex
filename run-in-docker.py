#!/usr/bin/env python3.6 -u

import argparse
import os
import shlex
import shutil
import subprocess
import sys

"""
Helper script to run DoesTheDogWatchPlex cli commands in a Docker container.
Probably only works on *nix/BSD/macOS. Obviously requires Docker.
"""

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--tag", default="dtdd-plex", help="Docker image name/tag to use [default: dtdd-plex]")

subparsers = parser.add_subparsers(help='sub-command help')

docker_build_parser = subparsers.add_parser('docker_build', help='Build Docker image')
docker_build_parser.add_argument("--config", default='', type=str, help="path to config.py to use")
docker_build_parser.add_argument('--force', default=False, type=bool,
    help='force using config.py passed in via --config if one already exists (a backup will be created)')

build_json_parser = subparsers.add_parser('build_json', help='Build the DoesTheDogDie JSON file')
build_json_parser.add_argument('--output', default='output/movies.json',
    help='path to write file to [default: output/movies.json]')

write_to_plex_parser = subparsers.add_parser('write_to_plex', help='Write JSON to plex')
write_to_plex_parser.add_argument('--json-path', default='output/movies.json',
    help='path to JSON file containing movie update data [default: output/movies.json')


def _run(cmd):
    print(f'[DEBUG] Running "{cmd}"')
    """ convenience fn to write command as string """
    for line in _myexec(shlex.split(cmd)):
        print(line, end='')

def _myexec(cmd):
    """
    runs command yielding each line of stdout as generated allowing them to be
    printed unbuffered. Useful for commands that generate a lot of output like
    chef runs or docker image builds
    """
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def docker_build(args):
    if not args.config:
        print('⚠️ --config not specified, assuming a "config.py" exists in "{os.getcwd()}"')
    else:
        _setup_config(args.config, force=args.force)

    # setup config 
    if not os.path.exists(args.config):
        print(f'❌ No such config file "{args.config}"')

    cwd = os.getcwd()
    config_dir = os.path.dirname(args.config)
    if os.getcwd() != os.path.dirname(args.config):
        if not os.path.exists('config.py'):
            new_path = os.path.join(os.getcwd(), 'config.py')
            print('✅ No existing config.py that would get overwritten')
            print(f"... Copying '{args.config}' -> '{new_path}'")
            shutil.copyfile(args.config, new_path)
        elif os.path.exists('config.py') and not args.force:
            print('⚠️ A file "config.py" exists locally already and would be overwritten')
            print('... --force flag not set so not proceeding')
            sys.exit(1)
        
            
    _run(f"docker build -t {args.tag} .")

def _setup_config(config_path, force=False, default_path='config.py'):
    if not os.path.exists(config_path):
        print(f'❌ No such config file "{config_path}"')

    if os.getcwd() != os.path.dirname(config_path):
        if not os.path.exists(default_path):
            new_path = os.path.join(os.getcwd(), default_path)
            print(f'✅ No existing {default_path} that would get overwritten')
            print(f"... Copying '{config_path}' -> '{new_path}'")
            shutil.copyfile(config_path, new_path)
        elif os.path.exists(default_path) and not force:
            print(f'⚠️ A file "{default_path}" exists locally already and would be overwritten')
            print('... "--force" flag not set so not proceeding')
            sys.exit(1)
        elif os.path.exists(default_path) and force:
            print(f'⚠️ A file "{default_path}" exists locally already and will be overwritten')
            backup_path = default_path + '.bak'
            print(f'... Making backup of "{default_path}" -> "{backup_path}"')
            shutil.copyfile(default_path, backup_path)
            print(f'... Copying "{config_path}" -> "{default_path}"')
            shutil.copyfile(config_path, default_path)


def _docker_run(tag, cmd, **opts):
    opts_str = ''
    if opts:
        opts_str = ' '.join([f"{flag} {val}" for flag, val in opts.items()])
    _run(f"docker run {opts_str} {tag} {cmd}")

def build_json(args):
    # make data volume container
    data_volume_name = 'json-output-data'
    _run(f"docker create -v /data --name {data_volume_name} {args.tag}")
    _docker_run(args.tag, "build_json.py --output=/data/movies.json",
        **{'--volumes-from': data_volume_name, '--rm': '',})

    if not os.path.exists(os.path.dirname(args.output)):
        os.makedirs(os.path.dirname(args.output))

    _run(f"docker cp {data_volume_name}:/data/movies.json {args.output}")
    _run(f"docker rm -v {data_volume_name}")

def write_to_plex(args):
    if not os.path.exists(args.json_path):
        print(f'❌ No such file "{args.json_path}"')
        sys.exit(1)
    _docker_run(args.tag, f"write_to_plex.py --json-path={args.json_path}",
        **{'--rm': '',})

# set subparser functions.
for fn in [docker_build, build_json, write_to_plex]:
    fn_subparser = getattr(sys.modules[__name__], f"{fn.__name__}_parser")
    fn_subparser.set_defaults(func=fn)

if __name__ == '__main__':
    args = parser.parse_args()
    try:
        args.func
    except AttributeError:
        parser.print_help()
        sys.exit(0)
    if not args.func == docker_build:
        if not os.path.exists(args.config):
            print(f'configuration file "{args.config}" does not exist')
            sys.exit(1)

    args.func(args)
