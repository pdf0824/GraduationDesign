from django.db import models


# Create your models here.

class ReAttend(models.Model):
    status = (
        (1, '处理中'),
        (2, '审批通过'),
        (3, '审批未通过')
    )
    stu_no = models.CharField('学号', max_length=44, null=True)
    attend_date = models.DateField('补签日期', null=True)
    attend_status = models.CharField('哪节课，0:12,1:34,2:56,3:78', max_length=80, null=True)
    re_attend_starter = models.CharField('补签发起人姓名', max_length=254, null=True)
    current_handler = models.CharField('当前处理人', max_length=254, null=True)
    re_attend_status = models.CharField('补签状态', max_length=80, choices=status, null=True, default=1)
    comments = models.CharField('补签原因', max_length=254, null=True)

    class Meta:
        db_table = 'T_XUPT_REATTEND'


class Attend(models.Model):
    week = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday '),
        (7, 'Sunday'),
    )
    status = (
        (0, '迟到'),
        (1, '旷课'),
        (2, '正常'),
        (3, '已补签'),
    )
    # stu_no = models.CharField('学号', max_length=44, null=True)
    # attend_date = models.DateField('签到日期', auto_now_add=True, null=True)
    # attend_week = models.CharField('星期', max_length=80, choices=week, null=True)
    # attend_morning = models.TimeField('签到时间', null=True)
    # attend_evening = models.TimeField('签到时间', null=True)
    # absence = models.IntegerField('缺勤时长', null=True)
    # state = models.CharField('签到状态', max_length=80, choices=status, default=1, null=True)
    # stu_name = models.CharField('学生姓名', max_length=254, null=True)
    stu_no = models.CharField('学号', max_length=44, null=True)
    attend_date = models.DateField('签到日期', auto_now_add=True, null=True)
    attend_week = models.CharField('星期', max_length=80, choices=week, null=True)
    attend_one = models.TimeField('12签到时间', null=True)
    attend_two = models.TimeField('34签到时间', null=True)
    attend_three = models.TimeField('56签到时间', null=True)
    attend_four = models.TimeField('78签到时间', null=True)
    # absence = models.IntegerField('缺勤时长', null=True)
    state_one = models.CharField('签到状态', max_length=80, choices=status, default=2, null=True)
    state_two = models.CharField('签到状态', max_length=80, choices=status, default=2, null=True)
    state_three = models.CharField('签到状态', max_length=80, choices=status, default=2, null=True)
    state_four = models.CharField('签到状态', max_length=80, choices=status, default=2, null=True)
    stu_name = models.CharField('学生姓名', max_length=254, null=True)

    def __str__(self):
        return self.stu_name

    class Meta:
        ordering = ['-attend_date']
        db_table = 'T_XUPT_ATTEND'


class Person(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    stu_no = models.CharField('学号', max_length=44)
    stu_name = models.CharField('学生姓名', max_length=255)
    college = models.CharField('学院', max_length=80)
    class_name = models.CharField('班级', max_length=80)
    password = models.CharField('密码', max_length=80)
    sex = models.CharField('性别', max_length=80, choices=gender, default='male')
    age = models.IntegerField('年龄')
    phone = models.CharField('手机号', max_length=44)
    addr = models.CharField('地址', max_length=255)
    date = models.DateField('出生日期')

    def __str__(self):
        return self.stu_name

    class Meta:
        db_table = 'T_XUPT_PERSON'


class TimeTable(models.Model):
    class_name = models.CharField('班级', max_length=80, unique=True)
    Monday = models.CharField('星期一', max_length=80)
    Tuesday = models.CharField('星期二', max_length=80)
    Wednesday = models.CharField('星期三', max_length=80)
    Thursday = models.CharField('星期四', max_length=80)
    Friday = models.CharField('星期五', max_length=80)

    class Meta:
        db_table = 'T_XUPT_TIMETABLE'


class Count(models.Model):
    stu_no = models.CharField('学号', max_length=44)
    stu_name = models.CharField('学生姓名', max_length=255)
    class_name = models.CharField('班级', max_length=80)
    late_count = models.IntegerField('迟到次数', default=0)
    absence_count = models.IntegerField('缺勤次数', default=0)
    leave_early = models.IntegerField('早退次数', default=0)

    def __str__(self):
        return self.stu_name

    class Meta:
        db_table = 'T_XUPT_COUNT'


class PageQueryBean(object):
    __DEFAULT_PAGE_SIZE = 10
    __current_page = 0
    __page_size = 0
    __total_rows = 0
    __start_row = 0
    __total_page = 0
    __items = None
    dic = None
    count = 0

    def get_start_row(self):
        if self.__start_row == 0 or self.__start_row is None:
            self.__start_row = 0 if self.__current_page == 0 or self.__current_page is None \
                else (int(self.__current_page) - 1) * self.get_page_size()
        return self.__start_row

    def set_start_row(self, row):
        self.__start_row = row

    def get_page_size(self):
        return self.__DEFAULT_PAGE_SIZE if self.__page_size == 0 or self.__page_size is None else self.__page_size

    def set_page_size(self, page_size):
        self.__page_size = page_size

    def get_total_rows(self):
        return self.__total_rows

    def set_total_rows(self, total_rows):
        self.__total_rows = total_rows
        total_page = total_rows / self.get_page_size() if total_rows % self.get_page_size() == 0 \
            else total_rows / self.get_page_size() + 1
        self.set_total_page(total_page)

    def get_items(self):
        return self.__items if self.__items is not None else None

    def set_items(self, items):
        self.__items = items

    def get_current_page(self):
        return self.__current_page

    def set_current_page(self, current_page):
        self.__current_page = current_page

    def get_total_page(self):
        return 1 if self.__total_page == 0 or self.__total_page is None else self.__total_page

    def set_total_page(self, total_page):
        self.__total_page = total_page

    def to_string(self):
        return "PageQueryBean [currentPage=" + str(self.__current_page) + \
               ", pageSize=" + str(self.__page_size) + ", totalRows=" + str(self.__total_rows) + \
               ", startRow=" + str(self.__start_row) + ", totalPage=" + str(self.__total_page) + \
               ", items=" + str(self.__items) + "]"


class QueryCondition(PageQueryBean):
    __id = None
    __start_date = None
    __end_date = None
    __range_date = None
    __class_name = None

    def __init__(self, id, range_date, class_name):
        self.__id = id
        self.__range_date = range_date
        self.__class_name = None if len(class_name) == 0 else class_name

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_start_date(self):
        return self.__start_date

    def set_start_date(self, start_date):
        self.__start_date = start_date

    def get_end_date(self):
        return self.__end_date

    def set_end_date(self, end_date):
        self.__end_date = end_date

    def get_range_date(self):
        return self.__range_date

    def set_range_date(self, range_date):
        self.__range_date = range_date

    def get_class_name(self):
        return self.__class_name

    def set_class_name(self, attend_status):
        self.__class_name = attend_status
