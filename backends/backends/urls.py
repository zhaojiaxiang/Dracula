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
    MyMcl, MyRelease, MyConfirm, MyApproval, MyPcl
from backends import settings
from checkouts.views import CheckOutFilesViewSet
from liaisons.views import LiaisonsViewSet, LiaisonUpdateStatusViewSet, QaProjectViewSet, QaProjectForMineViewSet, \
    QaProjectForGroupViewSet, LiaisonFileUpload, QaProjectDetailView
from projects.views import ProjectsViewSet
from qa.views import MCLQaHeadViewSet, QaDetailViewSet, QaDetailUpdateResultViewSet, \
    QaDetailUpdateContentTextViewSet, QaHeadUpdateObjectSummaryViewSet, QaHeadModifyDetailViewSet, \
    QaHeadTargetAndActualViewSet, CkEditorImageUpload, CkEditorFileUpload, RecoverFile, PCLQaClass1ViewSet, \
    PCLQaClass2ViewSet, PCLCommitJudgment
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
router.register('qa/mcl_detail', QaDetailViewSet, basename='mcl_detail')
router.register('qa/pcl_class1', PCLQaClass1ViewSet, basename='pcl_class1')
router.register('qa/pcl_class2', PCLQaClass2ViewSet, basename='pcl_class2')
router.register('qa/mcl_detail_update_result', QaDetailUpdateResultViewSet, basename='mcl_detail_update_result')
router.register('qa/mcl_detail_update_content_text', QaDetailUpdateContentTextViewSet,
                basename='mcl_detail_update_content_text')
router.register('qa/design_review', DesignReviewViewSet, basename='design_review')
router.register('qa/code_review', CodeReviewViewSet, basename='code_review')
router.register('accounts/system_setting', SystemSettingViewSet, basename='system_setting')
# 开发项目，和上面的项目代码不一样
router.register('qa_project', QaProjectViewSet, basename='qa_project')
router.register('qa_project_group', QaProjectForGroupViewSet, basename='qa_project_group')
router.register('qa_project_mine', QaProjectForMineViewSet, basename='qa_project_mine')
router.register('pb_file_checkout', CheckOutFilesViewSet, basename='pb_file_checkout')


urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/api-auth/', include('rest_framework.urls')),
    path('api/docs/', include_docs_urls(title="drf docs")),
    path('api/', include(router.urls)),
    path('api/login/', obtain_jwt_token),
    #
    path('api/mine_order_info/', UserDevelopmentDetail.as_view()),
    path('api/mine_task_bar/', MyTaskBar.as_view()),
    path('api/mine_task_mcl/', MyMcl.as_view()),
    path('api/mine_task_pcl/', MyPcl.as_view()),
    path('api/mine_task_approval/', MyApproval.as_view()),
    path('api/mine_task_conform/', MyConfirm.as_view()),
    path('api/mine_task_release/', MyRelease.as_view()),
    path('api/files/<str:filename>', RecoverFile.as_view()),
    path('api/image_upload/', CkEditorImageUpload.as_view()),
    path('api/file_upload/', CkEditorFileUpload.as_view()),
    path('api/liaison_file_upload/', LiaisonFileUpload.as_view()),
    path('api/pcl_commit_judgment/', PCLCommitJudgment.as_view()),
    path('api/qa_project_detail_view/', QaProjectDetailView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
