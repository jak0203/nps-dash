from django.core.management.base import BaseCommand, CommandError
from nps.models import RawResults, Comments

IGNORE_COMMENTS = (
    '',
    '  -  ', '  nn', ' ...', ' ...,pk ij', ' asddf', ' asdsa', ' dddd', ' dsa', ' dsfa', ' f', ' m', ' N/A', ' nanny',
    '_', ',,,', ',myntbrvfe', '!', '!!!', '?', '??', '???', '????', '.', '. ', '..', '...', '....', '.....', '......',
    '.......', '........', '......./', "'", '*', '/', '+', '3d', '4gtaerg a3', '98uh98', 'a', 'a;slkfj', 'abc',
    'abcdefghijklmnopqrstuvwxyz.', 'ADFD', 'adfg', 'adsf', 'adsfas', 'adsfasf', 'aerg', 'ahh', 'ai', 'ak n;dfgafgio',
    'aksdjl;fh;sh', 'asd', 'asdf', 'asdfa', 'asdfasdf', 'asdfs', 'asdfsdf', 'asdfvsdf', 'asdkjf;lk', 'asfasdf', 'asfd',
    'asfdsa', 'asgadsb', 'b', 'b s', 'bbb', 'bc ', 'blah', 'blah blah blah', 'bo', 'boo', 'c', 'cx', 'd', 'dd', 'dddd',
    'dddddd', 'dfdf', 'dfdgfd', 'dfdgfdrtg', 'dfgmadf;lgk', 'dfhdhsd', 'dfkljladh', 'dfsdfsdf', 'dfsfsdfdsf', 'dfynhfx',
    'dghfhn', 'djdjdhyd', 'dkfjdk', 'ds', 'dsfafa', 'dsgs', 'dsgv', 'dslkj', 'Dumb', 'dvcx', 'e', 'edfdfdf', 'ee', 'ef',
    'erwr', 'EWLKHTGSIURLGHRSIH', 'f', 'fafa', 'fb', 'fbfgghbg', 'fdadfsad', 'fdghfd', 'fdsafdsa', 'ff', 'fg',
    'fgghdghdzsfgdf', 'fjfjfjklsdjfklsdajfdsla;kaf;s', 'fsdf', 'fskdlfjdskl;f', 'fyjgkgkg', 'fzdh', 'g', 'ggg', 'ghg',
    'ghhh', 'ghigigh', 'ghjkghj','h', 'hdf', 'hf', 'hfh', 'hfhfg', 'hgfkjhglkjb', 'hgi', 'Hgiggh', 'hgjf', 'hguig',
    'hgyfhu', 'hh', 'hhh', 'hhhh', 'Hi', 'hj', 'hjdklas', 'hjh', 'hjhj', 'hoijp', 'hol;j.', 'i', 'idk',
    'iiiiiiiiiiiiiiiiiiii', 'iijkjkj', 'IKJILKJ', 'iuu', 'j', 'j,', 'jdjdmlkfzsdkln;fdsgcj;,fc', 'jf', 'jfldsjf',
    'jfoisdfjsdfio', 'jgh', 'JGJDF', 'jgjh;', 'jh', 'jhhl', 'jhj', 'jhk', 'ji', 'jj', 'jjj', 'jjjj', 'JJJJJ', 'jk',
    'jk.,k', "jkdlfsaj;ogr'ae", 'jkgfouyfgouyg', 'jkgh', 'jkhjk', 'jkhjtjyhj', 'jkl', 'jkl;jl', 'jkljlk', 'jksdfh',
    'jlh.jklh', 'k', 'kdsjflaksjfklsdjf', 'kjahsdkjfh', 'kjb', 'kjgh', 'kjh', 'kjhgh', 'kjhkh', 'kjhkjh', 'kjk', 'KK',
    'kkihkjh', 'kkkkk', 'kkkkkkk', 'kl;lkj', 'kldfldsfg', 'kugiilugfku.jgh/iolk', 'l', 'L,,,', "l;kk'j'lk", 'ljoijkl;j',
    'lkhj', 'lkhkh', 'lkj', 'lknblsbns', 'lksdfjl', 'll', 'lll', 'lllllll', 'lllllllll', 'lolcfg', 'lwefk', 'm', 'n',
    'n;jk/', 'n.a', 'na', 'NA - no review', 'Nah.', 'naoishfoieh', 'nierndt', 'nnn', 'nnnn', 'nnnnnnnnnnnnnnnnnnnnnnnn',
    'no', 'No ', 'ns', 'o', "ohi'oj", 'oiukh', 'ooooooooopoooooooooooooooooooooooooooooooooooooooooooooooooo', 'q',
    'q.kwdhg', 'r', 'sef', 'sfd', 'sfsafws', 'sfsdfdf', 'sgfd', 'sgfds', 'shdhj', 't', 'u', 'uibuio', 'uil', 'ujg',
    'ukhiul', 'utjhk', 'v', 'vbfgbxgfvb ', 'vbvbvb', 'ww', 'x', 'x.', 'xcxx', 'xdfghxfgh', 'xdjdfj', 'xfgsdsgd',
    'xfhgmjfyj,lfuy', 'xx', 'xxx', 'xxxx', 'xxxxx', 'xxxxxx vv  vv  ', 'Xxxxxxx', 'Xxxxxxxx', 'xyz', 'y', 'Yaaaaaaa',
    'yay', 'yes', 'yguygyugig', 'yikyrk7', 'ytuwstfry', 'yup', 'yup.', 'yyjukik', 'z', 'zcsdfs', 'zdsdvzdsv', 'zz',
    'Zzzzz',

)


class Command(BaseCommand):
    help = 'Pulls just the comment responses from the RawResults table and stores them in the Comments table for ' \
           'analysis.'

    def handle(self, *args, **options):
        print('Wiping comments table')
        Comments.objects.all().delete()
        for comment in RawResults.objects.filter(question_name='comments'):
            comment_dict = {
                'client': comment.client,
                'survey_name': comment.survey_name,
                'user_id': comment.user_id,
                'response': comment.response,
                'ignore': False,
            }

            if comment.response in IGNORE_COMMENTS:
                comment_dict['ignore'] = True
            c = Comments(**comment_dict)
            c.save()
