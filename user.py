# 构建弱智查看系统

import time
import sbgc as sb


uname = "1120171224"
upass = "*********"

# 把想抢的课的id放进去
the_list = []
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


def grab_all_courses()->dict:
    # TODO 可以再增加一些filter？
    all_list = []
    all_list.extend(user.get_courses('t'))
    all_list.extend(user.get_courses('g'))
    all_list.extend(user.get_courses('x'))

    # 是不是应该再筛选一下？
    return all_list


def grab_course(the_list, total_times=100, sleep_time=1):
    "抢课，不多说"
    for i in range(total_times):
        print(f"{i} in {total_times}")
        for course_id in the_list:

            # 如果成功
            if user.choose_a_course(course_id)['success']:
                print(f'已经成功选课{course_id}')

                # 将不能选的课筛选走 TODO
                for all_id in the_list:
                    if user.choose_a_course(all_id) == 0:
                        the_list.remove(all_id)
                        print(f"因为冲突，已经移除对{all_id}的抢课")

        # 沉睡
        time.sleep(sleep_time)
        return
    print("任务完成")


# 测试代码start
the_list = list(create_course_id([1234, 3333, 2222, 8888, 7476, 2342]))
print(len(grab_all_courses()))
#——————end
