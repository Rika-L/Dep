"""
自定义分页组件
def pretty_list(request):
    # 1.根据情况筛选数据
    queryset = PrettyNum.objects.all()

    # 2.实例化分页对象
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        'page_string': page_object.html()  # 页码
    }
    return render(request, 'pretty_list.html', context)

在html页面中：

    {% for obj in queryset %}
        {{obj.xx}}
        {% endfor %}

    <div class="container">
        <ul class="pagination">
            {{ page_string }}
        </ul>
    </div>
"""

from django.utils.safestring import mark_safe
import copy


class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page", page_show=5):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据（根据数据分页）
        :param page_size: 每页显示的数据
        :param page_param: 获取分页的参数
        :param page_show: 显示当前页的前或后几页
        """
        # 防止搜索出结果时翻页url上没有搜索参数
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        total_data_count = queryset.count()

        total_page_count, div = divmod(total_data_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.page_show = page_show
        self.request = request
        self.page_param = page_param

    def html(self):

        # 计算出显示当前页的前5页，后5页

        if self.total_page_count <= 2 * self.page_show + 1:
            # 数据库数据比较少，没有达到11页
            start_page = 1
            end_page = self.total_page_count + 1
        else:
            # 数据库数据比较多

            # 当前页小于5时
            if self.page <= self.page_show:
                start_page = 1
                end_page = 2 * self.page_show + 1 + 1
            else:
                # 当前页大于5，判断极值
                # 当前页+5大于总页码不合适
                if (self.page + self.page_show) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.page_show
                    end_page = self.total_page_count + 1
                else:
                    start_page = self.page - self.page_show
                    end_page = self.page + self.page_show + 1

        # 页码
        page_str_list = []

        # 首页
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
            if i == self.page:
                self.query_dict.setlist(self.page_param, [i])
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                self.query_dict.setlist(self.page_param, [i])
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

        search_string = """<li>
                        <form method="get" style="float: left;margin-left: -1px">
                            <input style="position: relative;
                            float: left;
                            display: inline-block;
                            width: 80px;
                            border-radius: 0"
                            type="text" name="page" class="form-control" placeholder="页码" required/>
                            <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                        </form>
                    </li>"""
        page_str_list.append(search_string)

        page_string = mark_safe(''.join(page_str_list))

        return page_string
