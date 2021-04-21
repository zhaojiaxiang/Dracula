from rest_framework import filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from backends.settings import env
from checkouts.filters import CheckOutFilesFilter
from checkouts.models import CheckOutFiles
from checkouts.serializers import CheckOutFilesSerializer
from utils.email import send_email


class CheckOutFilesPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CheckOutFilesViewSet(viewsets.ModelViewSet):
    serializer_class = CheckOutFilesSerializer
    pagination_class = CheckOutFilesPagination

    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filter_class = CheckOutFilesFilter

    def get_queryset(self):
        return CheckOutFiles.objects.all().order_by('fchkstatus', '-fregisterdte', 'fslipno')


class SendEmail(APIView):
    """
    邮件发送接口
    目前没有使用多联络票多邮件发送，每次请求只发送一次邮件
    多邮件发送存在问题，代码注释进行保留
    """

    def post(self, request):
        data = request.data
        user = request.user

        check_list = data['tableData']

        mail_html_start = '''<p>你好</p>
                             <p>请迁出以下文档：</p>
                             <table border="1px" cellspacing="0px" style="border-collapse:collapse">
                                <thead>
                                    <tr>
                                        <th>系统</th>
                                        <th>备注</th>
                                        <th>联络票号</th>
                                        <th>文件名称</th>
                                    </tr>
                                </thead>
                             <tbody>'''

        mail_html_end = '''</tbody>
                           </table>
                           <p>''' + user.name + ''', 谢谢</p>'''

        '''多邮件发送'''
        # old_fslipno = ''
        # mail_html_mid = ''
        # for inx, row in enumerate(chklist):
        #     new_fslipno = row['fslipno']
        #     if new_fslipno != old_fslipno and old_fslipno != '':
        #         if not send_email(mail_html_start + mail_html_mid + mail_html_end, sender, data['addresslist'],
        #                           '[ AMMIC ] 程序迁出-' + user.name + '-' + old_fslipno, mail_host, mail_post,
        #                           mail_user,
        #                           mail_pass,
        #                           receivers):
        #             ret_data = {
        #                 'code': '400',
        #                 'message': '邮件发送失败'
        #             }
        #             return Response(ret_data, status=status.HTTP_200_OK)
        #
        #         mail_html_mid = ''
        #
        #     mail_html_mid += "<tr>"
        #     mail_html_mid += "<td>" + row['fsystem'] + "</td>"
        #     mail_html_mid += "<td>" + row['fcomment'] + "</td>"
        #     mail_html_mid += "<td>" + row['fslipno'] + "</td>"
        #     mail_html_mid += "<td>" + row['fchkoutobj'] + "</td>"
        #     mail_html_mid += "</tr>"
        #     old_fslipno = new_fslipno
        #     if inx == len(chklist) - 1:
        #         if not send_email(mail_html_start + mail_html_mid + mail_html_end, sender, data['addresslist'],
        #                           '[ AMMIC ] 程序迁出-' + user.name + '-' + old_fslipno, mail_host, mail_post,
        #                           mail_user,
        #                           mail_pass,
        #                           receivers):
        #             ret_data = {
        #                 'code': '400',
        #                 'message': '邮件发送失败'
        #             }
        #             return Response(ret_data, status=status.HTTP_200_OK)

        '''单邮件发送'''
        mail_html_mid = ''
        for row in check_list:
            mail_html_mid += "<tr>"
            mail_html_mid += "<td>" + row['fsystem'] + "</td>"
            mail_html_mid += "<td>" + row['fcomment'] + "</td>"
            mail_html_mid += "<td>" + row['fslipno'] + "</td>"
            mail_html_mid += "<td>" + row['fchkoutobj'] + "</td>"
            mail_html_mid += "</tr>"

        email_title = '[ AMMIC ] 程序迁出-' + user.name
        email_content = mail_html_start + mail_html_mid + mail_html_end
        address_list = data['addresslist']
        receivers = address_list.split(',')

        if not send_email(email_title, email_content, address_list, receivers):
            ret_data = {
                'code': '400',
                'message': '邮件发送失败'
            }
            return Response(ret_data, status=status.HTTP_200_OK)

        ret_data = {}
        return Response(ret_data, status=status.HTTP_200_OK)
