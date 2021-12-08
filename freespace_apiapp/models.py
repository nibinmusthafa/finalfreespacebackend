from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models import DateTimeField
from django.db.models.expressions import OrderBy


# Create your models here.
#---------------------------------------------Desig model----------------------------------------------

class Designation(models.Model):
    designation_name =models.CharField(max_length=100,null=True)

    class Meta:
        ordering = ['id']
    def __str__(self):
        return self.designation_name

#---------------------------------------------User model----------------------------------------------
class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    designation_id=models.ForeignKey(Designation,on_delete=models.CASCADE,null=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 
    
     



#------------------------------------------------Customer model------------------------------------------
class Customer(models.Model):
    customer_firstname = models.CharField(max_length=100,null=True,blank=True)
    customer_lastname = models.CharField(max_length=100,null=True,blank=True)
    customer_phonenumber= models.CharField(max_length=15,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    updated_by =models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    updated_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering =['id']
    
    def __str__(self):
        return str(self.customer_phonenumber)

#------------------------------------------------State model-------------------------------------
class State(models.Model):
    state_name = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.state_name
class Country(models.Model):
    country_name = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.country_name
#------------------------------------------------Address model------------------------------------
class Address(models.Model):
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    addr_line1 = models.CharField(max_length=200,null=True)
    addr_line2 = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=50,null=True)
    state_id = models.ForeignKey(State,on_delete=models.CASCADE,null=True)
    country_id=models.ForeignKey(Country,on_delete=models.CASCADE,null=True)
    pincode = models.IntegerField(null=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
    def __str__(self):
        return self.customer_id     

#----------------------------------------------Category--------------------------------------------------


class Category(models.Model):
    category_name = models.CharField(max_length=100,null=True)

    class Meta:
        ordering =['id']

    def __str__(self):
        return self.category_name

#----------------------------------------------Sub Category--------------------------------------------------

class Sub_Category(models.Model):
    name = models.CharField(max_length=50,null=True)
    cat_id = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)

    class Meta:
        ordering =['id']

    def __str__(self):
        return self.name


#---------------------------------------------Status----------------------------------------------
class Status(models.Model):
    status_value=models.CharField(max_length=50,null=True)
    designation_id=models.ForeignKey(Designation,on_delete=models.CASCADE,null=True)
    display_for=models.ForeignKey(Designation,related_name='designer',on_delete=models.CASCADE,null=True)

    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.status_value

#---------------------------------------------Lead Source-------------------------------------------------------
class LeadSource(models.Model):
    sourcevalue = models.CharField(max_length=100,null=True)


    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.sourcevalue



#---------------------------------------------Lead-------------------------------------------------------

class Lead(models.Model):
    created_by = models.ForeignKey(User,related_name='fuser_id',on_delete=models.CASCADE,null=True,blank=True)
    designer_id = models.ForeignKey(User,related_name='designer_id',on_delete=models.CASCADE,null=True,blank=True)
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
    status_id = models.ForeignKey(Status,on_delete=models.CASCADE,null=True,blank=True)
    leadname = models.CharField(max_length=50,unique=True,null=True,blank=True)
    description = models.CharField(max_length=500,null=True,blank=True)
    renovation = models.BooleanField(null=True)
    leadsource_id = models.ForeignKey(LeadSource,on_delete=models.CASCADE,null=True)
    supervisor_id = models.ForeignKey(User,related_name='supervisor_id',on_delete=models.CASCADE,null=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    followup_date=models.DateField(null=True)
    quotation_amount=models.IntegerField(null=True)
    
    class Meta:
        ordering =['-id']

    def __str__(self):
        return str(self.leadname)
   
#--------------------------------------------status tracker-------------------------------------

class Statustracker(models.Model):
    lead_id = models.ForeignKey(Lead,on_delete=models.CASCADE,null=True)
    status_id = models.ForeignKey(Status,on_delete=models.CASCADE,null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    
    class Meta:
        ordering =['id']

    def __str__(self):
        return self.date





#------------------------------------------temp file-----------------------------------------
class Tempfile(models.Model):
    name=models.CharField(max_length=200,null=True)
    file=models.FileField(upload_to='images/',blank=True)
    lead_id= models.ForeignKey(Lead,on_delete=models.CASCADE,null=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    class Meta:
        ordering =['id']

    def __str__(self):
        return self.name
#------------------------------------------file table------------------------------------------

class File(models.Model):
    file_name = models.CharField(max_length=100,null=True)
    url=models.CharField(max_length=500,null=True)
    date=models.DateTimeField(auto_now_add=True)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    #tempfile_id=models.ForeignKey(Tempfile,related_name='tempfile_id',on_delete=models.CASCADE,null=True)
    lead_id= models.ForeignKey(Lead,on_delete=models.CASCADE,null=True)

    class Meta:
        ordering =['date']

    def __str__(self):
        return self.file_name


#---------------------------------------------Lead remarks-----------------------------------------

class Leadremarks(models.Model):
    lead_id= models.ForeignKey(Lead,on_delete=models.CASCADE,null=True)
    remark_data = models.CharField(max_length=500,null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    
    class Meta:
        ordering =['id']

    def __str__(self):
        return self.remark_data
#---------------------------------------------Lead category----------------------------------------

class Leadcategory(models.Model):
    lead_id= models.ForeignKey(Lead,on_delete=models.CASCADE,null=True)
    category_id = models.ForeignKey(Category,related_name="cats_id",on_delete=models.CASCADE,null=True)
    sub_cat_id = models.ForeignKey(Sub_Category,on_delete=models.CASCADE,  null=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    units = models.IntegerField(null=True,blank=True)

    class Meta:
        ordering =['-id']

    def __str__(self):
        return str(self.units)



#--------------------------------------Customer_Followup------------------------------------------------------------

class Customer_Followup(models.Model):
    lead_id=models.ForeignKey(Lead,on_delete=models.CASCADE)
    updated_by=models.ForeignKey(User,on_delete=models.CASCADE)
    followup_date=models.DateField(null=True)
    datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =['-datetime']

    def __str__(self):
        return self.followup_date



#--------------------------------------Project------------------------------------------------------------

class Project(models.Model):
    lead_id=models.ForeignKey(Lead,on_delete=models.CASCADE)
    completion_date=models.DateField()
    tentative_date=models.DateTimeField()
    user_id =models.ForeignKey(User,related_name='userid',on_delete=models.CASCADE)
    superuser_id = models.ForeignKey(User,related_name='superuserid',on_delete=models.CASCADE)
    designer_id = models.ForeignKey(User,related_name='designerid',on_delete=models.CASCADE)    
    status_id = models.ForeignKey(Status,on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering =['id']

    def __str__(self):
        return self.completion_date




#----------------------------------project payment----------------------------------------------------

class Project_Payment(models.Model):
    project_id = models.ForeignKey(Project,on_delete=models.CASCADE)
    pay_amount = models.IntegerField()
    reason = models.CharField(max_length=200,null=True)
    updated_on = models.DateTimeField(auto_now_add=True) 
    updated_by =models.ForeignKey(User,on_delete=CASCADE,null=True)
    lead_id=models.ForeignKey(Lead,on_delete=models.CASCADE,null=True)
    class Meta:
        ordering =['id']

    def __str__(self):
        return self.updated_on

#------------------------------------type------------------------------------------


class Type(models.Model):
    type=models.CharField(max_length=50)

    class Meta:
        ordering =['type']

    def __str__(self):
        return self.type


#------------------------------------size------------------------------------------


class Size(models.Model):
    size=models.CharField(max_length=50)

    class Meta:
        ordering =['size']

    def __str__(self):
        return self.size
#------------------------------------Categorytype------------------------------------------


class Categorytype(models.Model):
    remarks=models.CharField(max_length=200)
    lead_id=models.ForeignKey(Lead,on_delete=models.CASCADE)
    lead_cat_id=models.ForeignKey(Leadcategory,on_delete=models.CASCADE) 
    updated_by=models.ForeignKey(User,on_delete=models.CASCADE)
    updated_on=models.DateField(auto_now_add=True)

    class Meta:
        ordering =['remarks']

    def __str__(self):
        return self.remarks



# ----------------------------------------------Category Subtype--------------------------------------------------

class Category_Subtype(models.Model):
    cat_type_id=models.ForeignKey(Categorytype,on_delete=models.CASCADE,null=True)
    type_id=models.ForeignKey(Type,on_delete=models.CASCADE,null=True)
    texture=models.CharField(max_length=100,null=True)
    unit=models.IntegerField(null=True)
    area=models.IntegerField(null=True)
    color=models.CharField(max_length=50,null=True)
    size_id=models.ForeignKey(Size,on_delete=models.CASCADE,null=True)
    updated_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    updated_on=models.DateField(auto_now_add=True,null=True)

    class Meta:
        ordering =['id']

    def __str__(self):
        return self.texture

#----------------------------------------------Manpower--------------------------------------------------

class Manpower(models.Model):
    type=models.CharField(max_length=100)
    value=models.IntegerField()

    class Meta:
        ordering =['id']

    def __str__(self):
        return self.type
#----------------------------------------------Project Manpower--------------------------------------------------

class Projectmanpower(models.Model):
    lead_id=models.ForeignKey(Lead,on_delete=models.CASCADE)
    manpower_id=models.ForeignKey(Manpower,on_delete=models.CASCADE)
    numbers=models.IntegerField()
    updated_by=models.ForeignKey(User,on_delete=models.CASCADE)
    updated_on=models.DateField(auto_now_add=True)
    

    class Meta:
        ordering =['id']

    def __str__(self):
        return str(self.numbers)
#----------------------------------------------nature of work--------------------------------------------------

class Natureofwork(models.Model):
    nature=models.CharField(max_length=100)
    

    class Meta:
        ordering =['id']

    def __str__(self):
        return self.nature
   

#----------------------------------------------Manpowerdates--------------------------------------------------

class Manpowerdates(models.Model):
    project_manpower_id=models.ForeignKey(Projectmanpower,on_delete=models.CASCADE)
    start_date=models.DateField()
    end_date=models.DateField()
    nature_of_work_id=models.ForeignKey(Natureofwork,on_delete=models.CASCADE)
    updated_by=models.ForeignKey(User,on_delete=models.CASCADE)
    updated_on=models.DateField(auto_now_add=True)
    

    class Meta:
        ordering =['id']

    def __str__(self):
        return str(self.start_date)


