from django.test import TestCase

# Create your tests here.
from django.urls import path
from django.conf import settings
from rest_framework import views

# from freespace_apiapp.serializers import requestserilaizer
from .views import *
from .import views
# from .views import AddAddress, AddCustomer, AddDesignation, DeleteAddress, DeleteCustomer, GetCustomer, GetDesignation, ListAddress, ListCustomers, ListDesignations, ListState, Listdesigners, Listsupervisor, ListuserView, PatchCustomer, RegisterView, LoginView, UpdateAddress, UserView, LogoutView

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
urlpatterns = [
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('listusers/', Listuserss.as_view()),
   


    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ------------------------ Designation----------------------------------------------------------
    path('adddesignation/', AddDesignation.as_view()),
    path('getdesignation/<int:pk>/', GetDesignation.as_view()),
    path('listdesignations/', ListDesignations.as_view()),
    path('UpdateDesignation/<int:pk>/', UpdateDesignation.as_view()),
    # -------designer-------
    path('listdesigners/', Listdesigners.as_view()),
    # --------supervisor-----
    path('listsupervisors/', Listsupervisor.as_view()),
    # ----------------------state--------------------------------------------------------------------
    path('AddState/',AddState.as_view()),
    path('liststate/', ListState.as_view()),
    # path('deletestate/<int:pk>/',DeleteState.as_view()),
    # path('updatestate/<int:pk>/',UpdateState.as_view()),
    path('listcountry/', ListCountry.as_view()),
    path('Addcountry/',AddCountry.as_view()),
    # ----------------------address------------------------------------------------------------------
    path('addaddress/', AddAddress.as_view()),
    path('listaddress/', ListAddress.as_view()),
    path('deleteaddress/<int:pk>/', DeleteAddress.as_view()),
    path('updateaddress/<int:pk>/', UpdateAddress.as_view()),
    # single customer single address
    path('addcustomer/', Createsingleaddress.as_view()),
    #path('updateecustomer/<int:pk>/', Updatesingleaddress.as_view()),
    #path('updatecustomerandaddress/<int:id>/<int:pk>/', UpdateAddresscustomer.as_view()),
    
    # ---------------------customer------------------------------------------------------------------
    path('addsinglecustomer/', AddCustomer.as_view()),
    path('listcustomers/', ListCustomers.as_view()),
    path('getcustomer/<int:pk>/', GetCustomer.as_view()),
    path('deletecustomer/<int:pk>/', DeleteCustomer.as_view()),
    path('updatecustomer/<int:pk>/', PatchCustomer.as_view()),

    # ---------------------------------category-------------------------------------------------------
    path('addcategory/', AddCategory.as_view()),
    path('listcategory/', ListCategory.as_view()),
    path('deletecategory/<int:pk>/', DeleteCategory.as_view()),
    path('updatecategory/<int:pk>/', UpdateCategory.as_view()),
    # ----------------------------------LEAD--------------------------------------------------------

    path('addlead/', AddLead.as_view()),
    path('listlead/', ListLead.as_view()),
    path('getlead/<int:pk>/', GetLead.as_view()),
    path('deletelead/<int:pk>/', DeleteLead.as_view()),
    path('updatelead/<int:pk>/', UpdateLead.as_view()),
    path('getleadbyfollowup/<int:pk>/',Getleadbyfollowup.as_view()),
    # ----update status in lead------
    path('updatestatusinlead/<int:pk>/',PatchLead.as_view()),
    path('updatefollowupinlead/<int:pk>/',PatchLead.as_view()),
 
    # ------list leads by ID ss------
    path('getleadbydesigners/<int:id>/', Getleadbydesigner.as_view()),
    path('getleadbyusers/<int:id>/', Getleadbyuser.as_view()),
    path('getleadbysupervisor/<int:id>/', Getleadbysupervisor.as_view()),
    
    # ------Lead + Category + SubCategory----------------------------------------------------
    path('createlead/', LeadView.as_view()),
    # 
    # path('leadleadeeey/', requestserilaizer.as_view()),


    # -------------------file------------------------------------------------------------------------
    path('addfile/', AddFile.as_view()),
    path('listfile/<int:pk>/', ListFile.as_view()),
    path('listfilebyid/<int:id>/<int:pk>/', ListFilebyid.as_view()),
    path('deletefile/<int:pk>/', DeleteFile.as_view()),
    path('updatefile/<int:pk>/', UpdateFile.as_view()),
    # --------------------lead remarks---------------------------------------------------------------
    path('addleadremarks/', AddLeadremarks.as_view()),
    path('listleadremarks/', ListLeadremarks.as_view()),
    path('deleteleadremarks/<int:pk>/', DeleteLeadremarks.as_view()),
    path('updateleadremarks/<int:pk>/', UpdateLeadremarks.as_view()),
    # lead remarks filter with lead id and userid
    path('getleadremarks/<int:id>/', GetLeadremarks.as_view()),
    # path('viewleadremarks/',Viewleadremarks.as_view()),
    path('getremarksbyuser/<int:id>/<int:pk>/',GetLeadremarksbyuserid.as_view()),

    # --------------------status---------------------------------------------------------------------
    path('addstatus/', AddStatus.as_view()),
    path('liststatus/', ListStatus.as_view()),
    path('getstatusfordesigner/', GetStatusfordesigner.as_view()),
    path('getstatusforsupervisor/', GetStatusforsupervisor.as_view()),
    path('deletestatus/<int:pk>/', DeleteStatus.as_view()),
    path('updatestatus/<int:pk>/', UpdateStatus.as_view()),
    # --------------------statustracker--------------------------------------------------------------

    path('addstatustracker/', AddStatustracker.as_view()),
    path('liststatustracker/', ListStatustracker.as_view()),
    path('deletestatustracker/<int:pk>/', DeleteStatustracker.as_view()),
    path('updatestatustracker/<int:pk>/', UpdateStatustracker.as_view()),

    # ----------------------subcategory--------------------------------------------------------------
    path('addsubcategory/', Addsubcategory.as_view()),
    path('listsubcategory/', Listsubcategory.as_view()),
    # path('listsubcategory/', Listsubcategory.as_view()),
    path('deletesubcategory/<int:pk>/', Deletesubcategory.as_view()),
    path('updatesubcategory/<int:pk>/', Updatesubcategory.as_view()),
    # ----------------------categorysubtype-----------------------------------------------------------
    # path('addcategorysubtype/', Addcategorysubtype.as_view()),
    # path('listscategorysubtype/', Listcategorysubtype.as_view()),
    # path('deletecategorysubtype/<int:pk>/', Deletecategorysubtype.as_view()),
    # path('updatecategorysubtype/<int:pk>/', Updatecategorysubtype.as_view()),
    # ----------------------------leadsource---------------------------------------------------------
    path('addleadsource/', AddLeadsource.as_view()),
    path('listleadsource/', ListLeadsource.as_view()),
    path('deleteleadsource/<int:pk>/', DeleteLeadsource.as_view()),
    path('updateleadsource/<int:pk>/', UpdateLeadsource.as_view()),
    # ----------------------------leadcategory-------------------------------------------------------
    path('addleadcategory/', AddLeadcategory.as_view()),
    path('listleadcategory/', ListLeadcategory.as_view()),
    path('getleadcategorybylead/<int:pk>/', ListLeadsubcategory.as_view()),
    path('deleteleadcategory/<int:pk>/', DeleteLeadcategory.as_view()),
    path('updateleadcategory/<int:pk>/', UpdateLeadcategory.as_view()),
    path('patchleadcategory/<int:pk>/', Patchleadcategory.as_view()),

    # path('leadCategorysubcategory/<int:id>/<int:pk>/',views.LeadCategorysubcategory),
    # path('getleadcategorysubcatbylead/<int:pk>/', ListLeadsubcategoryyyyy.as_view()),
    # path('getleadcategorysubcategory/<int:id>/', Leadcategorysubcategory.as_view()),

    # ----------------------------PROJECT------------------------------------------------------------
    path('addproject/', AddProject.as_view()),
    path('listproject/', ListProject.as_view()),
    path('deleteproject/<int:pk>/', DeleteProject.as_view()),
    path('updateproject/<int:pk>/', UpdateProject.as_view()),
    # ----------------------------Project Payment----------------------------------------------------
    path('addprojectpayment/', AddProjectpayment.as_view()),
    path('listprojectpayment/', ListProjectpayment.as_view()),
    path('deleteprojectpayment/<int:pk>/', DeleteProjectpayment.as_view()),
    path('updateprojectpayement/<int:pk>/', UpdateProjectpayment.as_view()),

    # path('remarksfile/',views.Createleadremarks.as_view()),
    path('addfollowup/', AddCustomer_Followup.as_view()),
    path('listfollowup/', Listcustomerfollowup.as_view()),
    path('getfollowup/<int:pk>/', Getcustomerfollowup.as_view()),
    path('updatecustomerfollowup/<int:pk>/', Updatecustomerfollowup.as_view()),
    path('addimage/', AddImage.as_view()),


  

]
