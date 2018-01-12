# 构建弱智查看系统

import time
import sbgc as sb


uname = "1120171224"
upass = "Bsfdsdf0"

# 把想抢的课的id放进去
the_list = set({201720182002231,201720182002251,
201720182002410,201720182001822,201720182001819,
201720182001820,201720182001823,201720182001826,201720182001426,
201720182001430,201720182001429,201720182001433,201720182002261,
201720182002259,201720182002266,201720182001829,201720182000663,
201720182002350,201720182000128,201720182000127,201720182002200,
201720182002204,201720182002205,201720182000680,201720182000771,
201720182000659,201720182000654,201720182000673,201720182000669,
201720182002289,201720182002296,201720182001821,201720182002248,
201720182002409,201720182001378,201720182000120,
201720182002238,201720182002250,201720182002228})
total_times = 100
user = sb.SBGC(uname, upass)
sleep_time = 1  # seconds
"""
return 1:
{'success': True}

return 0:
{'success': False, 'message': '选课失败：当前教学班已选择！'}
{'success': False, 'message': '选课失败：文化素质通识课，限选1门，已选1门！'}
{'success': False, 'message': '选课失败：与已选课程 “离散数学Ⅰ” 冲突'}

return 2:
OTHER?

"""


def create_course_id(suffix_list: str)->str:
    "输入后四位，生成完整值"
    return map(lambda x: '20172018200' + str(x), suffix_list)


def process_response_json(jsondict: dict, boolean: bool)->int:
    "对传进来的json进行处理，boolean表示是否把输出到终端上"
    if jsondict['success']:
        if boolean:
            print("成功")
        return 1
    else:
        if boolean:
            print(jsondict['message'])

            # 似乎还可以再优化速度
        if '当前教学班已选择' in jsondict['message'] \
                or '限选' in jsondict['message'] \
                or '与已选课程' in jsondict['message']:
            return 0

        # 留给其他消息
        return 2


def grab_all_courses(user: sb.SBGC, filters: bool)->dict:
    # TODO 可以再增加一些filter？
    all_list = []
    all_list.extend(user.get_courses('t', filters))
    all_list.extend(user.get_courses('g', filters))
    all_list.extend(user.get_courses('x', filters))

    # 是不是应该再筛选一下？
    return all_list


def grab_course(the_list: set, total_times: int= 100, sleep_time: int=1, if_mamual: bool =1):
    "抢课，不多说"
    
    #total_times并没有卵用
    #for i in range(total_times):
    while True:
        #print(f"{i} in {total_times}")
        for course_id in the_list:

            # 如果成功
            if user.choose_a_course(course_id)['success']:
                print(f'已经成功选课{course_id}')

                # 将不能选的课筛选走 TODO
                # for all_id in the_list:
                #     if user.choose_a_course(all_id) == 0:
                #         the_list.remove(all_id)
                #         print(f"因为冲突，已经移除对{all_id}的抢课")

                # 如果是手动输入模式就直接退出
                # 原因是：手动模式要避免对get_course函数的依赖
                if if_mamual:
                    the_list.remove(course_id)
                else:
                    intercourse = grab_all_courses(user, True)
                    the_list &= intercourse

                    break
        # 沉睡
        time.sleep(sleep_time)
        return
    print("任务完成")


# 测试代码start

# 选出所有的可以抢的课程
def auto_GC(total_times=20000, sleep_time=1):
    the_list = set(grab_all_courses(user, 1))
    grab_course(the_list, total_times, sleep_time)


def manual_GC(total_times=20000, sleep_time=1):
    the_list = set({201720182002231,201720182002251,
201720182002410,201720182001822,201720182001819,
201720182001820,201720182001823,201720182001826,201720182001426,
201720182001430,201720182001429,201720182001433,201720182002261,
201720182002259,201720182002266,201720182001829,201720182000663,
201720182002350,201720182000128,201720182000127,201720182002200,
201720182002204,201720182002205,201720182000680,201720182000771,
201720182000659,201720182000654,201720182000673,201720182000669,
201720182002289,201720182002296,201720182001821,201720182002248,
201720182002409,201720182001378,201720182000120,
201720182002238,201720182002250,201720182002228})
    grab_course(the_list, total_times, sleep_time)
    #——————end
"""
问题1：
没抢到课的响应头中的json是什么？
因为要针对这个进行分析

问题2：
如果
"""
if __name__ == "__main__":
    manual_GC(None,sleep_time)
