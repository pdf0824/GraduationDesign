# coding=utf-8
# coding=utf-8
from ..models import Attend
from ..models import PageQueryBean
import json


def get_all_list(condition):
    count = (Attend.objects.all().filter(attend_date__range=(
        condition.get_start_date(), condition.get_end_date()))).count()
    page_result = PageQueryBean()
    items = []
    if count > 0:
        page_result.set_total_rows(count)
        page_result.set_current_page(condition.get_current_page())
        page_result.set_page_size(condition.get_page_size())
        param = []
        sql = '''select person.stu_name,person.class_name,attend.* from T_XUPT_PERSON person,T_XUPT_ATTEND attend WHERE person.stu_no=attend.stu_no '''
        if condition.get_class_name() is not None:
            sql += ''' and person.class_name="''' + condition.get_class_name() + '''" '''
        if condition.get_start_date() is not None and condition.get_end_date() is not None:
            sql += 'and attend_date between ' + "'" + condition.get_start_date() + "'" + ' and ' + "'" \
                   + condition.get_end_date() + "' "
        sql += 'limit ' + str(condition.get_start_row()) + ',' + str(condition.get_page_size())
        items = Attend.objects.raw(sql)
        print(items, 'items')
        page_result.set_items(items)
    dic = {
        'currentPage': page_result.get_current_page(),
        'pageSize': page_result.get_page_size(),
        'totalRows': page_result.get_total_rows(),
        'startRow': page_result.get_start_row(),
        'totalPage': page_result.get_total_page(),
        'items': [
            {'userId': attend.stu_no,
             'attendDate': str(attend.attend_date),
             'attendWeek': attend.attend_week,
             'attendOne': str(attend.attend_one),
             'attendTwo': str(attend.attend_two),
             'attendThree': str(attend.attend_three),
             'attendFour': str(attend.attend_four),
             'stateOne': attend.state_one,
             'stateTwo': attend.state_two,
             'stateThree': attend.state_three,
             'stateFour': attend.state_four,
             'className': attend.class_name,
             'stuName': attend.stu_name,
             } for attend in items
        ]
    }
    res = json.dumps(dic)
    return res
