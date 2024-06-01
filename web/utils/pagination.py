# -*- encoding: utf-8 -*-
"""
@Modify Time : 2024/5/31 12:27      
@Author : Mozinapig   
@Version : 1.0  
@Desciption : None
  
"""
from django.utils.safestring import mark_safe


# 自定义分页组件
class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        self.page_param = page_param
        page = request.GET.get(page_param, '1')
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]
        total_count = queryset.count()  # 数据总条数
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1  # 总页数
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        # 显示当前页的前五页和后五页
        # 增加极值,防止页码出bug
        if self.total_page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.total_page_count + 1
        else:
            # 数据库里面很多数据而且当前页面小于5
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 数据库里面数据很多而且当前页面大于5
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count + 1
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus + 1
        # start_page = page - plus
        # end_page = page + plus + 1

        # 页码
        page_str_list = []
        self.query_dict.setlist(self.page_param, [1])

        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        for i in range(start_page, end_page):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        search_string = '''
                <li>
                    <form method="get" style="float: left;margin-left: -1px">
                        <input type="text" class="form-control" placeholder="页码"
                               name="page"
                               style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0"/>
                        <button type="submit" class="btn btn-default" style="border-radius: 0;">跳转</button>
                    </form>
                </li>
            '''

        page_str_list.append(search_string)

        page_string = mark_safe("".join(page_str_list))
        return page_string
