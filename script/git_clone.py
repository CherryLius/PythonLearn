import os

git_url = 'git@git.homelabs.cn'
cmd = 'ssh -T %s' % git_url
format_git_url = '%s:{}.git' % git_url


def clone_from_git(project_name):
    _name = input('Input a new project name. Default is %s: ' % project_name)
    print('new_name=%s. project name=%s' % (_name, project_name))
    clone_cmd = 'git clone %s' % format_git_url.format(project_name)
    _command = clone_cmd if not _name else ' '.join([clone_cmd, _name])
    print(os.popen(_command).read())


ret = os.popen(cmd).read()
none_empty_list = filter(lambda x: x and '\t' in x, ret.split('\n'))
project_list = list(map(lambda x: x.split('\t')[1], none_empty_list))
print('There is [%d] projects at git [%s]' % (len(project_list), git_url))
if len(project_list):
    project_list.append('** All Projects.** ')
print('all projects at server %s:\n' % git_url)
for i in range(len(project_list)):
    print('%d.\t%s' % (i, project_list[i]))
while True:
    try:
        index = int(input('Please Select:'))
        if 0 <= index < len(project_list):
            break
    except ValueError:
        pass
    print('input a valid number.')
print(index)
len_real_project = len(project_list) - 1
[clone_from_git(project_list[i]) for i in range(len_real_project)] if index == len_real_project else clone_from_git(
    project_list[index])
