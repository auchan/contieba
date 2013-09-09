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
    print('Site:', abs_url)

    count, skip = 0, 0
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
        if 'j_thread_list clearfix' in line or find:
            find = True
            # article title
            if u'class="j_th_tit"' in line:
                count += 1
                th_title = re.findall(r'href.*?title="(.*?)"', line)
                print('[{}]'.format(count), th_title[0])
            # article summary
            if u'threadlist_abs threadlist_abs_onlyline' in line:
                skip += 1
                if skip == 2:
                    summarys = re.findall(r'\<div.*?\>(.*)(\<!--+>)+\</div\>', line)
                    print('summary:', summarys[0][0])
                    print()
                    find = False
                    skip = 0
        # list first N number arcticls, where N is specifiled by amount
        # N must have a uppe bound for I'm not consider about.
        if count == amount and find == False:
            break
