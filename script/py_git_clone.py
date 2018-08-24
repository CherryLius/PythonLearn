import os

git_url = 'git@git.homelabs.cn'
cmd = 'ssh -T %s' % git_url
format_git_url = '%s:{}.git' % git_url
ret = os.popen(cmd).read()
none_empty_list = filter(lambda x: x and '\t' in x, ret.split('\n'))
project_list = list(map(lambda x: x.split('\t')[1], none_empty_list))
print('all projects at server %s:\n' % git_url)
for i in range(len(project_list)):
    print('%d.\t%s' % (i, project_list[i]))
