"弱智抢课模块"
from typing import Dict
import functools
import regex
import requests
from requests import Response


def print_response_info(res: requests.models.Response)->None:
    "打印response类的信息"
    print("url is :  ", res.url)
    print("status_code :  ", res.status_code)
    print("cookies is :  ", res.cookies)
    print("headers is :  ", res.headers)
    print("history is :  ", res.history)
    return


# 参考 http://python.jobbole.com/81423/
def typecheck(f):
    def do_typecheck(name, arg):
        expected_type = f.__annotations__.get(name, None)
        if expected_type and not isinstance(arg, expected_type):
            raise TypeError("{} should be of type {} instead of {}".format(
                name, expected_type.__name__, type(arg).__name__))

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        for i, arg in enumerate(args[:f.__code__.co_nlocals]):
            do_typecheck(f.__code__.co_varnames[i], arg)
        for name, arg in kwargs.items():
            do_typecheck(name, arg)

        result = f(*args, **kwargs)

        do_typecheck('return', result)
        return result
    return wrapper


class SBGC:
    "弱智抢课类"
    jwms_url = 'http://jwms.bit.edu.cn'
    jwms_choose_course_url = 'http://jwms.bit.edu.cn/jsxsd/xsxkkc/ggxxkxkOper'  # TODO 替换为{}
    jwms_quit_course_url = 'http://jwms.bit.edu.cn/jsxsd/xsxkjg/xstkOper'
    jxid = None
    #session = None

    @typecheck
    def __init__(self, username: str, pwd: str):
        "初始化，登录CAS系统"

        # print("正在登录")

        self.session = requests.Session()

        # 选课系统使用CAS验证获得登录cookie
        def cas_login(url: str, data: Dict=None)->Response:
            param = {'service': url}
            return self.session.post(f'https://login.bit.edu.cn/cas/login', data=data, params=param)

        def get_value(name: str, res: Response)->str:
            # <input type="hidden" name="execution" value="e4s1" />
            return regex.search(f'(?<={name}" value=")[^"]+', res.text)[0]

        res = cas_login(self.jwms_url)

        execution, lt = [get_value(x, res) for x in ['execution', 'lt']]

        data = {'username': username, 'password': pwd, 'rememberMe': 'true',
                '_eventId': 'submit', 'rmShown': '1', 'execution': execution,
                'lt': lt}
        response = cas_login(self.jwms_url, data)

        # 登录教务处选课, get一些奇奇怪怪的cookie
        if self.jxid is None:
            # 这里的判断好像有点多余，本意是想只get一次jxid，算了先不改了
            response = self.session.get(
                f'{self.jwms_url}/jsxsd/xsxk/xklc_list')
            self.jxid = regex.search(r'[^?]+(?=">进入选课)', response.text)[0]

        response = self.session.get(
            f'{self.jwms_url}/jsxsd/xsxk/xsxk_index?{self.jxid}')

        # 判断是否正确登录
        """
        if response.status_code == 200 and response.url == "http://jwms.bit.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid=AAA8EC1F210D4E13885F532C4A5E8B4F":
            #print("您已经正确登录教务处！")
        else:
            #print_response_info(response)
            #print("登录失败，请检查相关配置！")
        """

    @typecheck
    def get_courses(self, ctype: str)->Dict:
        "获取课程列表"

        # g->公选课|t->体育课|x->拓展英语
        types = {'g': 'xsxkGgxxkxk', 't': 'xsxkTykxk', 'x': 'xsxkXlxk'}

        # kcxz:课程性质 kcgs:课程归属 szjylb:种类 kcxx:课程 skls:上课老师
        # xkxq:选课星期 xkjc:选课节次 sfct:是否(过滤)冲突 sfym:根本没这选项...
        param = {'kcxz': '06', 'sfct': 'true', 'sfym': 'false',
                 'kcxx': '', 'skls': '', 'skxq': '', 'skjc': '',
                 'kcgs': '', 'szjylb': ''}
        data = {'iDisplayStart': 0, 'iDisplayLength': 1000}  # 一次加载所有的课程列表

        res = self.session.post(f'{self.jwms_url}/jsxsd/xsxkkc/{types[ctype]}',
                                data=data, params=param)

        return res.json()['aaData']

    @typecheck
    def choose_a_course(self, course_id: str)->Dict:
        "选择课程"
        params = {'xkzy': '', 'trjf': '', 'jx0404id': course_id}
        result = self.session.get(self.jwms_choose_course_url, params=params)

        #print("result:", result.text)
        return result.json()

        """
        if 'true' in result.text:
            # print(f"恭喜!你已经成功选则课程:{course_id}")
            #return 1
            pass
        else:
            
            #print(f"未能成功选择课程:{course_id}\n")
            # print(result.text)
            #return 0
        """

    @typecheck
    def quit_a_course(self, course_id: str)->Dict:
        "退选课程"
        params = {'jx0404id': course_id}
        result = self.session.get(self.jwms_quit_course_url, params=params)

        return result.json()

        """
        if 'true' in result.text:
            #print(f"嘻嘻，{course_id}已经退了")
            return 1
        else:
            #print_response_info(result)
            #print(f"未能成功退选课程:{course_id}")
            #print(result.text)
            return 0
        """


if __name__ == "__main__":
    user = SBGC('112017××××', "××××××××××")
    # user.get_courses('x')
    cid = 201720182001368
    print(user.choose_a_course(cid))
    user.quit_a_course(cid)