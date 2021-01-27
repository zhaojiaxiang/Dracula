"""backends URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from accounts.views import UserViewSet, SystemSettingViewSet, MyGroupUserViewSet, UserDevelopmentDetail, MyTaskBar, \
    MyTesting, MyRelease, MyConfirm, MyApproval
from backends import settings
from liaisons.views import LiaisonsViewSet, LiaisonUpdateStatusViewSet
from projects.views import ProjectsViewSet
from qa.views import MCLQaHeadViewSet, MCLQaDetailViewSet, MCLQaDetailUpdateResultViewSet, \
    MCLQaDetailUpdateContentTextViewSet, QaHeadUpdateObjectSummaryViewSet, QaHeadModifyDetailViewSet, \
    QaHeadTargetAndActualViewSet, ImageUpload, FileUpload
from reports.views import ReportListViewSet
from reviews.views import DesignReviewViewSet, CodeReviewViewSet
from systems.views import SystemsViewSet

router = DefaultRouter()

router.register('accounts', UserViewSet, basename='accounts')
router.register('group_users', MyGroupUserViewSet, basename='group_users')
router.register('liaisons', LiaisonsViewSet, basename='liaisons')
router.register('liaison_update_status', LiaisonUpdateStatusViewSet, basename='liaison_update_status')
router.register('reports', ReportListViewSet, basename='reports')
router.register('projects', ProjectsViewSet, basename='projects')
router.register('systems', SystemsViewSet, basename='systems')
router.register('qa/mcl_head', MCLQaHeadViewSet, basename='mcl_head')
router.register('qa/mcl_head_update_summary', QaHeadUpdateObjectSummaryViewSet, basename='mcl_head_update_summary')
router.register('qa/mcl_head_modify_detail', QaHeadModifyDetailViewSet, basename='mcl_head_modify_detail')
router.register('qa/mcl_head_target_actual', QaHeadTargetAndActualViewSet, basename='mcl_head_target_actual')
router.register('qa/mcl_detail', MCLQaDetailViewSet, basename='mcl_detail')
router.register('qa/mcl_detail_update_result', MCLQaDetailUpdateResultViewSet, basename='mcl_detail_update_result')
router.register('qa/mcl_detail_update_content_text', MCLQaDetailUpdateContentTextViewSet,
                basename='mcl_detail_update_content_text')
router.register('qa/design_review', DesignReviewViewSet, basename='design_review')
router.register('qa/code_review', CodeReviewViewSet, basename='code_review')
router.register('accounts/system_setting', SystemSettingViewSet, basename='system_setting')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('docs/', include_docs_urls(title="drf docs")),
    path('api/', include(router.urls)),
    path('api/login/', obtain_jwt_token),
    #
    path('api/mine-order-info/', UserDevelopmentDetail.as_view()),
    path('api/mine-task-bar/', MyTaskBar.as_view()),
    path('api/mine-task-testing/', MyTesting.as_view()),
    path('api/mine-task-approval/', MyApproval.as_view()),
    path('api/mine-task-conform/', MyConfirm.as_view()),
    path('api/mine-task-release/', MyRelease.as_view()),
    path('api/image_upload/', ImageUpload.as_view()),
    path('api/file_upload/', FileUpload.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
