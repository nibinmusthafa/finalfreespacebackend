from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import AddressSerializer, CategorySerializer, CountrySerializer, Customer_FollowupSerializer, CustomerSerializer, DesignationSerializer, FileSerializer, LeadSerializer, LeadcategorySerializer,LeadremarksSerializer, LeadsourceSerializer, ListuserSerializer, ProjectSerializer, ProjectpaymentSerializer, SingleaddressSerializer, StateSerializer, StatusSerializer, StatustrackerSerializer, SubCategorySerializer, TempfileSerializer, UserSerializer
from .models import Address, Category,  Country, Customer, Customer_Followup, Designation, File, Lead, LeadSource, Leadcategory, Leadremarks, Project, Project_Payment, State, Status, Statustracker, Sub_Category, User
import jwt, datetime

from rest_framework import generics

from rest_framework import status


from rest_framework.decorators import api_view








# from rest_framework.permissions import IsAuthenticated

# Create your views here.

#----------------------------------------register--------------------------------------------
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
#-------------------------------------------loginview--------------------------------------

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
    
        response = Response()
        
        # response.set_cookie(key='jwt', value=token, httponly=False)
        response.data = {
            'jwt': token,
            'id':user.id,
            'name':user.name
        }
        return response

#----------------------------------------------------userview--------------------------------------
class UserView(APIView):
    #permisson_classes =[IsAuthenticated]  
    def get(self, request):
        
        #token = request.COOKIES.get('token')
        token = request.headers.get('token')
        #token = request.data['jwt']
        #token = request.data.get('jwt')
        #token = request.authenticate_header.get('jwt_key')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
   
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)



class Listuserss(generics.GenericAPIView):
       
    serializer_class=ListuserSerializer        
    def get(self, request):
        queryset = User.objects.all()
        serializer = ListuserSerializer(queryset, many=True)
        return Response(serializer.data)

#--------------------------------------------------logout----------------------------------------
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

# -----------------------------------Designation--------------------------------------------------------
class AddDesignation(generics.CreateAPIView):
    
       
    serializer_class=DesignationSerializer        
    def post(self, request):
        duplicate = Designation.objects.filter(
            designation_name__icontains=request.data['designation_name']).count()
        if duplicate > 0:
            return Response("Already Existing Designation ")
        else:
            serializer = DesignationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data['id'])
            return Response("failed")


class GetDesignation(generics.GenericAPIView):
       
    serializer_class=DesignationSerializer        
    def get(self, request, pk):
        queryset = Designation.objects.filter(id=pk)
        serializer = DesignationSerializer(queryset, many=True)
        return Response(serializer.data)


class ListDesignations(generics.GenericAPIView):
       
    serializer_class=DesignationSerializer        
    def get(self, request):
        queryset = Designation.objects.all()
        serializer = DesignationSerializer(queryset, many=True)
        return Response(serializer.data)


# class DeleteDesignation(generics.DestroyAPIView):
       
#     serializer_class=DesignationSerializer        
#     def delete(self, request, pk):
#         des = Designation.objects.get(id=pk)
#         des.delete()
#         return Response("Deleted!!")


class UpdateDesignation(generics.UpdateAPIView):
       
    serializer_class=DesignationSerializer        
    def put(self, request, pk):
        des = Designation.objects.get(id=pk)
        ser = DesignationSerializer(instance=des, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response("Updated!!")


#------------------------------------------designers--------------------------------------------


class Listdesigners(generics.GenericAPIView):
       
    serializer_class=UserSerializer        
    def get(self, request):
        queryset = User.objects.filter(designation_id=3)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
#-----------------------------------------supervisor--------------------------------------


class Listsupervisor(generics.GenericAPIView):
       
    serializer_class=UserSerializer        
    def get(self, request):
        queryset = User.objects.filter(designation_id=2)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

#---------------------------------------------customer--------------------------------------------

class AddCustomer(generics.CreateAPIView):
       
    serializer_class=CustomerSerializer        
    def post(self, request):
        duplicate = Customer.objects.filter(
            email__icontains=request.data['email']).count()
        if duplicate > 0:
            return Response("Already Existing customer ")
        else:
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("customer added succesfully")
            return Response("failed")


class ListCustomers(generics.GenericAPIView):
       
    serializer_class=CustomerSerializer        
    def get(self, request):
        queryset = Customer.objects.all()
        serializer = CustomerSerializer(queryset, many=True)
        return Response(serializer.data)


class GetCustomer(generics.GenericAPIView):
       
    serializer_class=CustomerSerializer        
    def get(self, request, pk):
        queryset = Customer.objects.get(id=pk)
        serializer = CustomerSerializer(queryset, many=False)
        return Response(serializer.data)


class DeleteCustomer(generics.DestroyAPIView):
       
    serializer_class=CustomerSerializer        
    def delete(self, request, pk):
        des = Customer.objects.get(id=pk)
        des.delete()
        return Response("Deleted!!")


class PatchCustomer(generics.UpdateAPIView):
       
    serializer_class=CustomerSerializer        
    def patch(self, request, pk):
        des = Customer.objects.get(id=pk)
        ser = CustomerSerializer(instance=des, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response("Updated!!")


#----------------------------------address---------------------------------------------


class AddAddress(generics.CreateAPIView):
       
    serializer_class=AddressSerializer        
    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("added succesfully")
        return Response("failed")


class ListAddress(generics.GenericAPIView):
       
    serializer_class=AddressSerializer        
    def get(self, request):
        queryset = Address.objects.all()
        serializer = AddressSerializer(queryset, many=True)
        return Response(serializer.data)


class DeleteAddress(generics.DestroyAPIView):
       
    serializer_class=AddressSerializer        
    def delete(self, request, pk):
        des = Address.objects.get(id=pk)
        des.delete()
        return Response("Deleted!!")


class UpdateAddress(generics.UpdateAPIView):
       
    serializer_class=AddressSerializer        
    def patch(self, request, pk):
        des = Address.objects.get(id=pk)
        ser = AddressSerializer(instance=des, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response("updated")

# class UpdateAddresscustomer(generics.UpdateAPIView):
       
#     serializer_class=AddressSerializer        
#     def put(self, request,id,pk):
#         des = Address.objects.get(customer_id=id)
#         ser = AddressSerializer(instance=des, data=request.data)
#         dess = Customer.objects.get(id=pk)
#         serr = CustomerSerializer(instance=dess, data=request.data)
#         if ser and serr.is_valid():
#             ser and serr.save()
#             return Response("updated")

# --------------------------------state------------------------------------------


class AddState(generics.CreateAPIView):
       
    serializer_class=StateSerializer        
    def post(self, request):
        duplicate = State.objects.filter(
            state_name__icontains=request.data['state_name']).count()
        if duplicate > 0:
            return Response("Already Existing state ")
        else:
            serializer = StateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("added succesfully")
            return Response("failed")


class ListState(generics.GenericAPIView):
       
    serializer_class=StateSerializer        
    def get(self, request):
        queryset = State.objects.all()
        serializer = StateSerializer(queryset, many=True)
        return Response(serializer.data)


# class DeleteState(generics.DestroyAPIView):
       
#     serializer_class=StateSerializer        

#     def delete(self, request, pk):
#         des = State.objects.get(id=pk)
#         des.delete()
#         return Response("Deleted!!")


# class UpdateState(generics.UpdateAPIView):
       
#     serializer_class=StateSerializer        
#     def put(self, request, pk):
#         des = State.objects.get(id=pk)
#         ser = StateSerializer(instance=des, data=request.data)
#         if ser.is_valid():
#             ser.save()
#             return Response("updated")



class AddCountry(generics.CreateAPIView):
       
    serializer_class=CountrySerializer        
    def post(self, request):
        duplicate = Country.objects.filter(
            country_name__icontains=request.data['country_name']).count()
        if duplicate > 0:
            return Response("Already Existing country ")
        else:
            serializer = CountrySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("added succesfully")
            return Response("failed")


class ListCountry(generics.GenericAPIView):
       
    serializer_class=CountrySerializer        
    def get(self, request):
        queryset = Country.objects.all()
        serializer = CountrySerializer(queryset, many=True)
        return Response(serializer.data)


# ------------------------CUSTOMER and ADDRESS------------------------------------------


class Createsingleaddress(generics.CreateAPIView):
       
    serializer_class = SingleaddressSerializer
    model = Address

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            address_obj = SingleaddressSerializer.create(self, serializer.validated_data)
            address = SingleaddressSerializer(address_obj).data
           
            return Response({"status": True, "message": "Success", "response": {}})
        return Response({"status": False, "message": serializer.errors, "response": {}})


# class Updatesingleaddress(generics.UpdateAPIView):
       
#     serializer_class=SingleaddressSerializer        
#     def put(self, request, pk):
#         des = Address.objects.get(customer_id=pk)
#         ser = SingleaddressSerializer(instance=des, data=request.data)
#         if ser.is_valid():
#             ser.save()
#             return Response("updated")



#--------------------------------------category-------------------------------------------


class AddCategory(generics.CreateAPIView):
       
    serializer_class=CategorySerializer        
    def post(self, request):
        duplicate = Category.objects.filter(
            category_name__icontains=request.data['category_name']).count()
        if duplicate > 0:
            return Response("Already Existing category ")
        else:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("added succesfully")
            return Response("failed")


class ListCategory(generics.GenericAPIView):
       
    serializer_class=CategorySerializer        
    def get(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)


class DeleteCategory(generics.DestroyAPIView):
       
    serializer_class=CategorySerializer        
    def delete(self, request, pk):
        des = Category.objects.get(id=pk)
        des.delete()
        return Response("Deleted!!")


class UpdateCategory(generics.UpdateAPIView):
       
    serializer_class=CategorySerializer        
    def put(self, request, pk):
        des = Category.objects.get(id=pk)
        ser = CategorySerializer(instance=des, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response("Updated!!")


#---------------------------------------lead----------------------------------------------

class AddLead(generics.CreateAPIView):
       
    serializer_class=LeadSerializer        
    def post(self, request):
        serializer = LeadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Lead added succesfully")
        return Response("failed")


class ListLead(generics.GenericAPIView):
       
    serializer_class=LeadSerializer        
    def get(self, request):
        queryset = Lead.objects.all()
        serializer = LeadSerializer(queryset, many=True)
        return Response(serializer.data)

class GetLead(generics.GenericAPIView):
       
    serializer_class=LeadSerializer        
    def get(self, request, pk):
        queryset = Lead.objects.get(id=pk)
        serializer = LeadSerializer(queryset, many=False)
        return Response(serializer.data)

class DeleteLead(generics.DestroyAPIView):
       
    serializer_class=LeadSerializer        
    def delete(self, request, pk):
        des = Lead.objects.get(id=pk)
        des.delete()
        return Response("Deleted!!")


class UpdateLead(generics.UpdateAPIView):
       
    serializer_class=LeadSerializer        
    def put(self, request, pk):
            des = Lead.objects.get(id=pk)
            ser = LeadSerializer(instance=des, data=request.data)
            if ser.is_valid():
                ser.save()
                return Response("Updated!!")


class PatchLead(generics.UpdateAPIView):
       
    serializer_class=LeadSerializer        
    def patch(self, request, pk):
            des = Lead.objects.get(id=pk)
            ser = LeadSerializer(instance=des, data=request.data,partial=True)
            if ser.is_valid():
                ser.save()
                print(ser)
                return Response(ser.data)

class Getleadbyfollowup(generics.GenericAPIView):
       
    serializer_class=LeadSerializer        
    def get(self, request, pk):
        queryset = Lead.objects.get(id=pk)
        serializer = LeadSerializer(queryset, many=False)
        print(serializer.data)
        # followup = serializer.data['followup_date']
        # print(followup)
        return Response({'followup_date':serializer.data['followup_date']})      



#-----------------------listleadby_designer#---------------------------------------------


class Getleadbydesigner(generics.GenericAPIView):
       
    serializer_class=LeadSerializer        
    def get(self, request, id):
        queryset = Lead.objects.filter(designer_id=id)
        serializer = LeadSerializer(queryset, many=True)
        return Response(serializer.data)
#-----------------------listleadby_fuser--------------------------------------------


class Getleadbyuser(generics.GenericAPIView):
       
    serializer_class=LeadSerializer        
    def get(self, request, id):
        queryset = Lead.objects.filter(created_by=id)
        serializer = LeadSerializer(queryset, many=True)
        return Response(serializer.data)

# -----------------------listleadby_fuser---------------------------------------------


class Getleadbysupervisor(generics.GenericAPIView):
       
    serializer_class=LeadSerializer        
    def get(self, request, id):
        queryset = Lead.objects.filter(supervisor_id=id)
        serializer = LeadSerializer(queryset, many=True)
        return Response(serializer.data)


 # -------------------------LEAD  AND  CATEGORY (single / multiple)---------------------------


class LeadView(generics.CreateAPIView):
       
    serializer_class = LeadcategorySerializer
    model = Leadcategory
    

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=self.request.data)
        categories = self.request.data['categories']

        if serializer.is_valid():
            # print(serializer.validated_data)
            # print('#####################')
            leadcategory_obj = LeadcategorySerializer.create(
                self, serializer.validated_data, categories)
            leadcategory = LeadcategorySerializer(leadcategory_obj).data
            obj = Lead.objects.latest('id')
            print(obj.id)
            return Response({"lead_id":obj.id})
        # return Response(leadcategory_obj)
        return Response({"status": False, "response": {}})


# class listleadbysupervisor(generics.GenericAPIView):
       
#     serializer_class=LeadcategorySerializer        
#     def get(self, request, id):
#         queryset = Lead.objects.filter(supervisor_id=id)
#         serializer = LeadSerializer(queryset, many=True)
#         return Response(serializer.data)



    



# class Listleadcategorysubcategory(generics.CreateAPIView):
       
#     serializer_class = LeadcategorysubcategorySerializer
#     model = Leadcategory

#     def get(self, request,id, *args, **kwargs):

#         serializer = self.get_serializer(data=self.request.data)
#         designer_id = self.request.data[id]
#         categories = self.request.data['categories']

#         if serializer.is_valid():
#             # print(serializer.validated_data)
#             # print('#####################')
#             leadcategory_obj = LeadcategorysubcategorySerializer.filter(
#                 self, serializer.validated_data, categories)
#             designer_obj = LeadcategorysubcategorySerializer.filter(
#                 self, serializer.validated_data, designer_id)
#             leadcategory = LeadcategorysubcategorySerializer(leadcategory_obj).data

#         else:
#             return Response({"status": False, "message": serializer.errors, "response": {}})

#         return Response({"status": True, "message": "Success", "response": {}})




# -------------------------------------file--------------------------------------


class AddFile(generics.CreateAPIView):
       
    serializer_class=FileSerializer        
    def post(self, request):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("added succesfully")
        return Response("failed")


class ListFile(generics.GenericAPIView):
       
    serializer_class=FileSerializer        
    def get(self, request,pk):
        queryset = File.objects.filter(lead_id=pk)
        serializer = FileSerializer(queryset, many=True)
        return Response(serializer.data)

class ListFilebyid(generics.GenericAPIView):
       
    serializer_class=FileSerializer        
    def get(self, request,id,pk):
        queryset = File.objects.filter(lead_id=id,user_id=pk)
        serializer = FileSerializer(queryset, many=True)
        return Response(serializer.data)

class DeleteFile(generics.DestroyAPIView):
       
    serializer_class=FileSerializer        
    def delete(self, request, pk):
        des = File.objects.get(id=pk)
        des.delete()
        return Response("Deleted!!")


class UpdateFile(generics.UpdateAPIView):
       
    serializer_class=FileSerializer        
    def put(self, request, pk):
        des = File.objects.get(id=pk)
        ser = FileSerializer(instance=des, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response("Updated!!")

#-------------------------------------------------temp file----------------------------------

class AddImage(generics.CreateAPIView):
       
    serializer_class=TempfileSerializer        
    def post(self, request):
        serializer = TempfileSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)   
            file_obj = FileSerializer.create(
                self, serializer.validated_data, serializer.data)
            #leadcategory = FileSerializer(file_obj).data
            return Response(serializer.data)         
        return Response("upload failed")


# ----------------------------lead remarks---------------------------------------

class AddLeadremarks(generics.CreateAPIView):
       
    serializer_class=LeadremarksSerializer        
    def post(self, request):
        serializer = LeadremarksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("added succesfully")
        return Response("failed")


class ListLeadremarks(generics.GenericAPIView):
       
    serializer_class=LeadremarksSerializer        
    def get(self, request):
        queryset = Leadremarks.objects.all()
        serializer = LeadremarksSerializer(queryset, many=True)
        return Response(serializer.data)



class GetLeadremarks(generics.GenericAPIView):
       
    serializer_class=LeadremarksSerializer        
    def get(self, request,id):
        queryset = Leadremarks.objects.filter(lead_id=id)   #lead_id=id,use_
        serializer = LeadremarksSerializer(queryset, many=True)
        return Response(serializer.data)

class GetLeadremarksbyuserid(generics.GenericAPIView):
       
    serializer_class=LeadremarksSerializer        
    def get(self, request,id,pk):
        queryset = Leadremarks.objects.filter(lead_id=id,user_id=pk)   #lead_id=id,use_
        serializer = LeadremarksSerializer(queryset, many=True)
        return Response(serializer.data)


# class Viewleadremarks(generics.CreateAPIView):
#     def post(self, request):
#         lead_id=request.POST.get('id')
#         user_id= request.POST.get('pk')
#         try:
#             queryset = Leadremarks.objects.filter(lead_id='id',user_id='pk')
#             serializer = LeadremarksSerializer(queryset, data=request.data)
#             if serializer.is_valid():
#                 return Response(serializer.data)
#         except:
#             return Response("no remark")




class DeleteLeadremarks(generics.DestroyAPIView):
       
    serializer_class=LeadremarksSerializer        
    def delete(self, request, pk):
        des = Leadremarks.objects.get(id=pk)
        des.delete()
        return Response("Deleted!!")


class UpdateLeadremarks(generics.UpdateAPIView):
       
    serializer_class=LeadremarksSerializer        
    def patch(self, request, pk):
        des = Leadremarks.objects.get(id=pk)
        ser = LeadremarksSerializer(instance=des, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response("Updated!!")

#---------------------------------status---------------------------------------------------


class AddStatus(generics.CreateAPIView):
       
    serializer_class=StatusSerializer        
    def post(self, request):
        serializer = StatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("added succesfully")
        return Response("failed")


class ListStatus(generics.GenericAPIView):
       
    serializer_class=StatusSerializer        

    def get(self, request):
        queryset = Status.objects.all()
        serializer = StatusSerializer(queryset, many=True)
        return Response(serializer.data)


class GetStatusfordesigner(generics.GenericAPIView):
    
    serializer_class=StatusSerializer
    
    def get(self,request):
        queryset = Status.objects.filter(display_for=3)
        serializer = StatusSerializer(queryset, many=True)
        return Response(serializer.data)

class GetStatusforsupervisor(generics.GenericAPIView):
    
    serializer_class=StatusSerializer
    
    def get(self,request):
        queryset = Status.objects.filter(display_for=2)
        serializer = StatusSerializer(queryset, many=True)
        return Response(serializer.data)


class DeleteStatus(generics.DestroyAPIView):
       
    serializer_class=StatusSerializer        
    def delete(self, request, pk):
        des = Status.objects.get(id=pk)
        des.delete()
        return Response("Deleted!!")


class UpdateStatus(generics.UpdateAPIView):
       
    serializer_class=StatusSerializer        
    def put(self, request, pk):
        des = Status.objects.get(id=pk)
        ser = StatusSerializer(instance=des, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response("Updated!!")

# ----------------------------status tracker--------------------------------------


class AddStatustracker(generics.CreateAPIView):
       
    serializer_class=StatustrackerSerializer        
    def post(self, request):
        serializer = StatustrackerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("added succesfully")
        return Response("failed")


class ListStatustracker(generics.GenericAPIView):
       
    serializer_class=StatustrackerSerializer        


    def get(self, request):
        queryset = Statustracker.objects.all()
        serializer = StatustrackerSerializer(queryset, many=True)
        return Response(serializer.data)


class DeleteStatustracker(generics.DestroyAPIView):
       
    serializer_class=StatustrackerSerializer        
    def delete(self, request, pk):
        des = Statustracker.objects.get(id=pk)
        des.delete()
        return Response("Deleted!!")


class UpdateStatustracker(generics.UpdateAPIView):
       
    serializer_class=StatustrackerSerializer        
    def put(self, request, pk):
        des = Statustracker.objects.get(id=pk)
        ser = StatustrackerSerializer(instance=des, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response("Updated!!")


 #---------------------------------subcategory------------------------------------------------


class Addsubcategory(generics.CreateAPIView):
       
    serializer_class=SubCategorySerializer        
    def post(self, request):
        duplicate = Sub_Category.objects.filter(
            name__icontains=request.data['name']).count()
        if duplicate > 0:
            return Response("item already exists")
        else:
            serializer = SubCategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("sub category added successfully")
            return Response("failed")


class Listsubcategory(generics.GenericAPIView):
       
    serializer_class=SubCategorySerializer        
    def get(self, request):
        queryset = Sub_Category.objects.all()
        ser = SubCategorySerializer(queryset, many=True)
        return Response(ser.data)


class Deletesubcategory(generics.DestroyAPIView):
       
    serializer_class=SubCategorySerializer        
    def delete(self, request, pk):
        des = Sub_Category.objects.get(id=pk)
        des.delete()
        return Response("Deleted!!")


class Updatesubcategory(generics.UpdateAPIView):
       
    serializer_class=SubCategorySerializer        
    def put(self, request, pk):
        des = Sub_Category.objects.get(id=pk)
        ser = SubCategorySerializer(instance=des, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response("updated")

#--------------------------Category_Subtype#-----------------------------------------------


# class Addcategorysubtype(generics.CreateAPIView):
       
#     serializer_class=CategorySubtypeSerializer        
#     def post(self, request):
#         duplicate = Category_Subtype.objects.filter(
#             name__icontains=request.data['name']).count()
#         if duplicate > 0:
#             return Response("item already exists")
#         else:
#             serializer = CategorySubtypeSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response("added successfully")
#             return Response("failed")


# class Listcategorysubtype(generics.GenericAPIView):
       
#     serializer_class=CategorySubtypeSerializer        
#     def get(self, request):
#         queryset = Category_Subtype.objects.all()
#         ser = CategorySubtypeSerializer(queryset, many=True)
#         return Response(ser.data)


# class Deletecategorysubtype(generics.DestroyAPIView):
       
#     serializer_class=CategorySubtypeSerializer        
#     def delete(self, request, pk):
#         des = Category_Subtype.objects.get(id=pk)
#         des.delete()
#         return Response("Deleted!!")


# class Updatecategorysubtype(generics.UpdateAPIView):
       
#     serializer_class=CategorySubtypeSerializer        
#     def put(self, request, pk):
#         des = Category_Subtype.objects.get(id=pk)
#         ser = CategorySubtypeSerializer(instance=des, data=request.data)
#         if ser.is_valid():
#             ser.save()
#             return Response("updated")

#---------------------------leadsource-------------------------------------------------------


class AddLeadsource(generics.CreateAPIView):
       
    serializer_class=LeadsourceSerializer        
    def post(self, request):
        serializer = LeadsourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("added successfully")
        return Response("failed")


class ListLeadsource(generics.GenericAPIView):
       
    serializer_class=LeadsourceSerializer        
    def get(self, request):
        queryset = LeadSource.objects.all()
        ser = LeadsourceSerializer(queryset, many=True)
        return Response(ser.data)


class DeleteLeadsource(generics.DestroyAPIView):
       
    serializer_class=LeadsourceSerializer        
    def delete(self, request, pk):
        des = LeadSource.objects.get(id=pk)
        des.delete()
        return Response("Deleted!!")


class UpdateLeadsource(generics.UpdateAPIView):
       
    serializer_class=LeadsourceSerializer        
    def put(self, request, pk):
        des = LeadSource.objects.get(id=pk)
        ser = LeadsourceSerializer(instance=des, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response("updated")

#-------------------lead category--------------------------------------------------------------


class AddLeadcategory(generics.CreateAPIView):
       
    serializer_class=LeadcategorySerializer        
    def post(self, request):
        serializer = LeadcategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("added successfully")
        return Response("failed")


class ListLeadcategory(generics.GenericAPIView):
       
    serializer_class=LeadcategorySerializer        
    def get(self, request):
        queryset = Leadcategory.objects.all()
        ser = LeadcategorySerializer(queryset, many=True)
        return Response(ser.data)



class ListLeadsubcategory(generics.GenericAPIView):
       
    serializer_class=LeadcategorySerializer        
    def get(self, request, pk):
        queryset = Leadcategory.objects.filter(lead_id=pk)
        ser = LeadcategorySerializer(queryset, many=True)
        return Response(ser.data)




class GetLeadcategory(generics.GenericAPIView):
       
    serializer_class=LeadcategorySerializer        
    def get(self, request ,id):
        queryset = Leadcategory.objects.filter(designer_id=id)
        ser = LeadcategorySerializer(queryset, many=True)
        return Response(ser.data)


        

class DeleteLeadcategory(generics.DestroyAPIView):
       
    serializer_class=LeadcategorySerializer        
    def delete(self, request, pk):
        des = Leadcategory.objects.get(id=pk)
        des.delete()
        return Response("Deleted!!")


class UpdateLeadcategory(generics.UpdateAPIView):
       
    serializer_class=LeadcategorySerializer        
    def put(self, request, pk):
        des = Leadcategory.objects.get(id=pk)
        ser = LeadcategorySerializer(instance=des, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response("updated")


class Patchleadcategory(generics.UpdateAPIView):
       
    serializer_class=LeadcategorySerializer        
    def put(self, request, pk):
            des = Leadcategory.objects.get(id=pk)
            ser = LeadcategorySerializer(instance=des, data=request.data,  partial=True)
            if ser.is_valid():
                ser.save()
                return Response(ser.data)

#-------------------------------------project-----------------------------------------------


class AddProject(generics.CreateAPIView):
       
    serializer_class=ProjectSerializer        
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("added successfully")
        return Response("failed")


class ListProject(generics.GenericAPIView):
       
    serializer_class=ProjectSerializer        
    def get(self, request):
        queryset = Project.objects.all()
        ser = ProjectSerializer(queryset, many=True)
        return Response(ser.data)


class DeleteProject(generics.DestroyAPIView):
       
    serializer_class=ProjectSerializer        
    def delete(self, request, pk):
        des = Project.objects.get(id=pk)
        des.delete()
        return Response("Deleted!!")


class UpdateProject(generics.UpdateAPIView):
       
    serializer_class=ProjectSerializer        
    def put(self, request, pk):
        des = Project.objects.get(id=pk)
        ser = ProjectSerializer(instance=des, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response("updated")


# ------------------------------------project payment-----------------------------------------------
class AddProjectpayment(generics.CreateAPIView):
       
    serializer_class=ProjectpaymentSerializer        
    def post(self, request):
        serializer = ProjectpaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("added successfully")
        return Response("failed")


class ListProjectpayment(generics.GenericAPIView):
       
    serializer_class=ProjectpaymentSerializer        
    def get(self, request):
        queryset = Project_Payment.objects.all()
        ser = ProjectpaymentSerializer(queryset, many=True)
        return Response(ser.data)


class DeleteProjectpayment(generics.DestroyAPIView):
       
    serializer_class=ProjectpaymentSerializer        
    def delete(self, request, pk):
        des = Project_Payment.objects.get(id=pk)
        des.delete()
        return Response("Deleted!!")


class UpdateProjectpayment(generics.UpdateAPIView):
       
    serializer_class=ProjectpaymentSerializer        
    def put(self, request, pk):
        des = Project_Payment.objects.get(id=pk)
        ser = ProjectpaymentSerializer(instance=des, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response("updated")

#------------------customer follow up--------------------------------------------------------------


class AddCustomer_Followup(generics.CreateAPIView):
       
    serializer_class=Customer_FollowupSerializer        
    def post(self, request):
        print(request.data)
        serializer = Customer_FollowupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("added succesfully")
        return Response("failed")



class Listcustomerfollowup(generics.GenericAPIView):
       
    serializer_class=Customer_FollowupSerializer        
    def get(self, request):
        queryset = Customer_Followup.objects.all()
        ser = Customer_FollowupSerializer(queryset, many=True)
        return Response(ser.data)



class Getcustomerfollowup(generics.GenericAPIView):
       
    serializer_class=Customer_FollowupSerializer        
    def get(self, request, pk):
        queryset = Customer_Followup.objects.filter(lead_id=pk).order_by('-datetime')[:1]
        # queryset = Customer_Followup.objects.filter(lead_id=pk).first('datetime')
        # querysett = queryset.first()
        ser = Customer_FollowupSerializer(queryset, many=True)
        return Response(ser.data)



class Updatecustomerfollowup(generics.UpdateAPIView):
       
    serializer_class=Customer_FollowupSerializer        
    def patch(self, request, pk):
            des = Customer_Followup.objects.get(id=pk)
            ser = Customer_FollowupSerializer(instance=des, data=request.data,partial=True)
            if ser.is_valid():
                ser.save()
                return Response(ser.data)

# class ListLeadddddd(generics.GenericAPIView):
       
#     serializer_class=LeadSerializerrrr        
#     def get(self, request,pk):
#         queryset = Lead.objects.all()
#         querysett = Customer_Followup.objects.filter(lead_id=pk).order_by('-datetime')[:1]
#         lead = LeadSerializer(queryset, many=True)
#         custfollow = Customer_FollowupSerializer(querysett,many=True)
#         result = lead+custfollow
#         return Response(result)




#--------------------------------list lead category subcategory-------------------------------------


# class ListLeadsubcategoryyyyy(generics.GenericAPIView):       
#     serializer_class=LeadcategorysubcategorySerializer        
#     def get(self, request, pk):
#         queryset = Leadcategory.objects.filter(lead_id=pk)
#         ser = LeadcategorysubcategorySerializer(queryset, many=True)
#         return Response(ser.data)








# @api_view(['GET'])

# def LeadCategorysubcategory(request,id,pk):
#     obj=Lead()
#     obj2=Leadcategory()
#     if (obj.designer_id==id and obj2.lead_id==pk):
#         lead=Lead.objects.(designer_id=id)
#         leadid = Leadcategory.filter(lead_id=pk)
#         leadcat = LeadcategorySerializer(leadid)
#         leadser=LeadSerializer(lead)
#         result =leadcat.data+leadser.data
#         return Response(result)



# @api_view(['GET'])

# def LeadCustfollow(request):

#     queryset = Lead.objects.all()
#     querysett = Customer_Followup.objects.all()
#     leadser = LeadSerializer(queryset,many=True)
#     custfollow=Customer_FollowupSerializer(querysett,many=True)
#     result =leadser.data+custfollow.data
#     return Response(result)









