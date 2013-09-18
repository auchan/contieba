import re
from urllib.request import urlopen
from . import gbk_code

def monite(argv = ['linux', 10]):
    """     
command bar_name display_amount
        bar_name [display_amount=10]
        [bar_name=linux] [display_amount=10]
        -h = --help 查看帮助
    """
    rel_url = argv[0]
    amount = 10
    if isinstance(argv, str):
        if argv == '-h' or argv == '--help' or argv[0] == '-':
            print(monite.__doc__)
            return
        rel_url = argv
    elif len(argv) == 2:
        amount = int(argv[1])

    abs_url = 'http://tieba.baidu.com/' + str(gbk_code.getGBKCode(s=rel_url))

    print('开始解析网页\n')
    print('Site:', abs_url)

    find = False
    for line in urlopen(abs_url):
        line = line.decode('gbk')
        # html title
        if 'title' in line:
            titles = re.findall(r'\<title\>(.*)\</title\>', line) 
            if titles != []:
                print('Title:', titles[0])
                print()
        # subject symbol
        if 'j_thread_list thread_top clearfix' in line:
            not_top = re.findall('j_thread_list clearfix(.*)', line)
            if len(not_top) != 1:
                raise ValueError('置顶贴数为', len(not_top))

            contents = re.findall(r'class="threadlist_text.*?">(.*?)<s', not_top[0])
            authors = re.findall(r'class="tb_icon_author" title="主题(.*?)"', not_top[0])
            last_replyers = re.findall(r'tb_icon_author_rely j_replyer" title="(.*?)"', not_top[0])
            last_rep_dates = re.findall(r'threadlist_reply_date j_reply_data" title="最后回复时间">(.*?)</', not_top[0])

            count = 0
            for l in contents:
                if count % 2 == 0:
                    title = re.findall(r'title="(.*?)"', l)[0]
                    # 一个汉字的宽度等于两个ascii的宽度
                    # 百度贴吧标题最长为30个汉字
                    ascii_num = 0
                    for index in title:
                        if ord(index) < 128:
                            ascii_num += 1
                    sup = 62 - (2*len(title) - ascii_num)
                    print('[{}] {}'.format(count//2 + 1, title) + '.'*sup + '{}'.format( 
                        authors[count//2])) 
                else:
                    summary = re.findall(r'.*threadlist_abs_onlyline"\>(.*?)\<!--', l)
                    if summary:
                        summary = summary[0]
                    else:
                        summary = ''
                    print(' '*4 + '({})'.format(summary))
                    print('{}  {}\n'.format(last_replyers[(count-1)//2],
                        last_rep_dates[(count-1)//2]))
                count += 1
                # list first N number arcticls, where N is specifiled by amount
                # N must have a uppe bound for I'm not consider about.
                if count >= 2*amount:
                    break
            print('解析结束.')
            break

    print('  '*10 + '#')
    print('.'*10 + '#')
    print('人'*10 + '#')
