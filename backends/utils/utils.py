import os

from utils.db_connection import query_single_with_no_parameter


def create_folder(upload_path):
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)


def get_all_organization_belong_me(request):
    user = request.user

    if user.ammic_organization.isgroup:

        str_sql = f"select getallchildlist({user.ammic_organization.id})"
        organization_list = query_single_with_no_parameter(str_sql, 'list')
        organization = organization_list[0].split(',')
    else:
        str_sql = f"select getallchildlist({user.ammic_organization.parent.id})"
        organization_list = query_single_with_no_parameter(str_sql, 'list')
        organization = organization_list[0].split(',')

    if len(organization) == 1:
        # 由于元组中只有一个元素时，会有一个‘,’，因此让元组中有两个一样的元素
        organization = organization + organization

    return tuple(organization)


def get_all_organization_group_belong_me(request):
    user = request.user

    if user.ammic_organization.isgroup:

        str_sql = f"select getchildgrouplist({user.ammic_organization.id})"
        organization_list = query_single_with_no_parameter(str_sql, 'list')
        organization = organization_list[0].split(',')
    else:
        organization = [user.ammic_organization.parent.id]

    if len(organization) == 1:
        # 由于元组中只有一个元素时，会有一个‘,’，因此让元组中有两个一样的元素
        organization = organization + organization

    return tuple(organization)