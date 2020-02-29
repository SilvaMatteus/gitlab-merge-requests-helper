import gitlab


HEADER = '''
What a beautiful day to review merge requests =)
'''


def show_mr(mr):
    print('    ', mr.title)
    print('    ', mr.web_url)
    print('    ', 'Up votes:', mr.upvotes,
          ' ' * 8 + 'Down votes:', mr.downvotes)
    print('    ', 'MERGE STATUS: ', mr.merge_status, end='')
    print('    ', '#WORK_IN_PROGRESS') if mr.work_in_progress else print()
    print('    ', mr.source_branch, '-->', mr.target_branch)
    print('    ', 'Created at:', mr.created_at,
          'and updated at:', mr.updated_at)
    print('    ', 'By', mr.author['name'])
    print()


def process_mr_list(g):
    print('PROJECT:', g.name.upper(), '\n')
    for mr in g.mergerequests.list(state='opened', order_by='updated_at', sort='desc'):
        show_mr(mr)


def main(gitlab_addr, list_of_interest, private_token):
    gl = gitlab.Gitlab(gitlab_addr,
                       private_token=private_token)
    gl.auth()

    for group in [g for g in gl.groups.list() if g.name in list_of_interest]:
        process_mr_list(group)


if __name__ == '__main__':
    gitlab_addr = ''
    list_of_interest = []
    private_token = ''
    print(HEADER)
    main(gitlab_addr, list_of_interest, private_token)
