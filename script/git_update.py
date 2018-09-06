"""
git checkout branch-name
git pull

Usage:
    git_update.py (--checkout | --update) <branchName>...
    git_update.py <branchName>...

Options:
    -h --help     help
    --checkout    checkout only.
    --update      update branch and checkout back.
"""
import os

from docopt import docopt


def checkout_branch(branch_name):
    command = 'git checkout %s' % branch_name
    print('execute cmd [%s]' % command)
    return os.popen(command).read()


arguments = docopt(__doc__)
print(arguments)
branch = arguments['<branchName>'][0]
print('select branch: [%s]' % branch)
main_dir = os.getcwd()
child_files = os.listdir(main_dir)
for file in child_files:
    workspace = os.path.join(main_dir, file)
    path_git = os.path.join(workspace, '.git')
    if os.path.isfile(workspace) or not os.path.exists(path_git):
        print('skip [%s]\n' % workspace)
        continue
    os.chdir(workspace)
    print('current workspace is: [%s]' % os.getcwd())
    output_cmd = os.popen('git rev-parse --abbrev-ref HEAD')
    current_branch = output_cmd.read().rstrip()
    print('current branch is [%s]' % current_branch)
    is_same_branch = branch == current_branch
    if not is_same_branch:
        print(checkout_branch(branch))
    if not arguments['--checkout']:
        print('execute cmd [git pull]')
        output_cmd = os.popen('git pull')
        print(output_cmd.read())
        if not is_same_branch and arguments['--update']:
            print(checkout_branch(current_branch))

print('git update complete!')
