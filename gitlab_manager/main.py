import gitlab
import datetime
from dateutil import parser
from dateutil.tz import gettz

HEADER = '''
What a beautiful day to review merge requests =)
'''


def show_mr(mr):
    created_date = parser.isoparse(mr.created_at)
    updated_date = parser.isoparse(mr.updated_at)
    # Time elapsed warn!
    today = datetime.datetime.now().replace(tzinfo=updated_date.tzinfo)
    updated_delta = today - updated_date
    created_delta = today - created_date

    wip_text = '    #WIP' if mr.work_in_progress else ''
    too_old_text = '    #TOO_OLD' if updated_delta > datetime.timedelta(
        days=14) else ''
    not_updated_text = '    #NOT_UPDATED' if updated_delta > datetime.timedelta(
        days=7) else ''

    print('    ', mr.title)
    print('    ', mr.web_url)
    print('    ', 'Up votes:', mr.upvotes,
          ' ' * 8 + 'Down votes:', mr.downvotes)
    print('    ', 'MERGE STATUS: ', mr.merge_status, end='')
    print(wip_text + too_old_text + not_updated_text)
    print('    ', mr.source_branch, '-->', mr.target_branch)
    print('    ', 'Created at:', created_date.strftime('%d-%b-%Y, %H:%M'),
          'and updated at:', updated_date.strftime('%d-%b-%Y, %H:%M'))
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
