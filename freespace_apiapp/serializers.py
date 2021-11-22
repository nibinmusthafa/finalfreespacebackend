from rest_framework import serializers

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.renderers import JSONRenderer
from rest_framework import response
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework import generics

from rest_framework.decorators import api_view
# from rest_framework.permissions import IsAuthenticated

from freespace_apiapp.models import Designation

from .models import Address, Category, Category_Subtype, Customer, Designation, File, Lead, LeadSource, Leadcategory, Leadremarks, Project, Project_Payment, State, Status, Statustracker, Sub_Category, User



#--------------------------------------------designation--------------------------------------------------
class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields ='__all__'

#-------------------------------------------user----------------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):

    userdesignation = serializers.SerializerMethodField('get_designation') 
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password','designation_id','userdesignation']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def get_designation(self,obj):
        return obj.designation_id.designation_name

#--------------------------------customer--------------------------------------------
class CustomerSerializer(serializers.ModelSerializer):
    updated_by_name = serializers.SerializerMethodField('get_updatedbyname')

    class Meta:
        model = Customer
        fields = ('id','updated_by','updated_by_name','customer_firstname','customer_lastname','customer_phonenumber','email','updated_on')
    
    def get_updatedbyname(self, obj):
        return obj.updated_by.name

#-------------------------------state-------------------------------------------
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('id','state_name')

#------------------------------single address-------------------------------------------

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id','customer_id','addr_line1','addr_line2','city','pincode','updated_on','state_id')
# --------------------------------single customer address--------------------------------------------

class SingleaddressSerializer(serializers.ModelSerializer):
    customer_id=CustomerSerializer()

    class Meta:
        model = Address
        fields = ('id','customer_id','addr_line1','addr_line2','city','state_id','pincode','updated_on')
    def create(self, validated_data):
        items = validated_data.pop('customer_id')
        customer_obj = Customer.objects.create(**items)
        address =Address.objects.create(**validated_data,customer_id=customer_obj)
        return address



#-------------------------------category-------------------------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','category_name')

#-------------------------------subcategory-------------------------------------------
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Sub_Category
        fields = ('id','name','cat_id')

#-------------------------------categorysubtype-------------------------------------------
class CategorySubtypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category_Subtype
        fields = ('id','name','sub_cat_id')
#-------------------------------leadsource------------------------------------------
class LeadsourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeadSource
        fields = ('id','sourcevalue')

#-------------------------------Status-------------------------------------------
class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ('id','status_value','designation_id')

#-----------------------------Statustracker----------------------------------------
class StatustrackerSerializer(serializers.ModelSerializer):


    class Meta:
        model = Statustracker
        fields = ('id','lead_id','status_id','date','user_id')



#-----------------------------------------File------------------------------------

class FileSerializer(serializers.ModelSerializer):
  class Meta:
        model = File
        fields = ('id','file_name','date','user_id','lead_id')
#-----------------------------------lead--------------------------------------------

class LeadSerializer(serializers.ModelSerializer):
    customername = serializers.SerializerMethodField('get_customername')
    phonenumber = serializers.SerializerMethodField('get_phonenumber')
    statusvalue= serializers.SerializerMethodField('get_statusvalue')
    leadsource=serializers.SerializerMethodField('get_leadsource')
    
    class Meta:
        model = Lead
        fields =('id','leadsource','statusvalue','phonenumber','customername','created_by','designer_id','customer_id','status_id','leadname','description','renovation','leadsource_id','supervisor_id','updated_on')      
    
    def get_customername(self,obj):
        return '{} {}'.format(obj.customer_id.customer_firstname,obj.customer_id.customer_lastname)
    def get_phonenumber(self,obj):
        return obj.customer_id.customer_phonenumber
    def get_statusvalue(self,obj):
        return obj.status_id.status_value
    def get_leadsource(self,obj):
        return obj.leadsource_id.sourcevalue
    
    
    

#---------------------------------------multiple leadcategory----------------------------------------------------

class LeadcategorySerializer(serializers.ModelSerializer):
    lead_id=LeadSerializer()

    class Meta:
        model = Leadcategory
        fields = ('id','lead_id','category_id','sub_cat_id','updated_on','units')
    def create(self, validated_data,categories):
        print(categories)
        items = validated_data.pop('lead_id')
        lead_obj = Lead.objects.create(**items)
        # leadcat = Leadcategory.objects.create(lead_id=lead_obj)

        for c in categories:
            print(c)
            cat = Category.objects.get(id=c['category_id'])
            print(cat)
            
            try:
                sub_cat = Sub_Category.objects.get(id=c['sub_cat_id'])
            except:
                sub_cat = None

            
            
            leadcat = Leadcategory.objects.create(lead_id=lead_obj,category_id=cat,sub_cat_id=sub_cat,units=c['units'])
            leadcat.save()

#---------------------------------------lead remarks----------------------------------------------

class LeadremarksSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username')    
    class Meta:
        model = Leadremarks
        fields = ('id','username','lead_id','remark_data','datetime','user_id')

    def get_username(self,obj):
        return obj.user_id.name

#---------------------------------------project---------------------------------------------------------

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id','lead_id','completion_date','tentative_date','user_id','superuser_id','designer_id','status_id','updated_on')

#--------------------------------------project payement--------------------------------------------------
class ProjectpaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model =Project_Payment
        fields = ('id','project_id','paytype','pay_amount','reason','updated_on')


