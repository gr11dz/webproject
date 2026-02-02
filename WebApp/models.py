from django.db import models

class Access(models.Model):
    accessID = models.IntegerField(primary_key= True)
    access_permID = models.IntegerField()
    access_controllerName = models.CharField(max_length=100,)
    access_actionName = models.CharField(max_length= 100)
    class Meta:
        db_table = "access"

class Calender(models.Model):
    calenderID = models.AutoField(primary_key= True)
    calender_courseID = models.ForeignKey("Course", on_delete=models.CASCADE, db_column= "calender_courseID")
    calender_levelID = models.ForeignKey("Level", on_delete=models.CASCADE, db_column= "calender_levelID")
    calender_classessID = models.ForeignKey("Classess", on_delete=models.CASCADE, db_column= "calender_classessID")
    calender_startDate = models.CharField(max_length= 10, null= True)
    calender_endDate = models.CharField(max_length= 10, null= True)
    calender_day1 = models.CharField(max_length= 10, null= True)
    calender_day2 = models.CharField(max_length= 10, null= True)
    calender_day3 = models.CharField(max_length= 10, null= True)
    calender_day4 = models.CharField(max_length= 10, null= True)
    calender_day5 = models.CharField(max_length= 10, null= True)
    calender_day6 = models.CharField(max_length = 10, null= True)
    calender_day7 = models.CharField(max_length = 10, null= True)
    calenderCreatetime = models.DateTimeField(null= True)
    calender_lastUpdate = models.DateTimeField(null= True)
    calender_status = models.IntegerField(default= 1)
    class Meta:
        db_table = "calender"

class Check(models.Model):
    checkID = models.IntegerField(primary_key= True)
    # check_registerID = models.IntegerField(null= False, db_comment="شناسنامه ثبت نام")
    check_registerID = models.ForeignKey("Register", on_delete=models.CASCADE, db_column= "check_registerID")
    checkBankname = models.CharField(max_length= 20)
    checkBankFullname = models.CharField(max_length= 50, null= True)
    checkNumber = models.CharField(max_length= 50, null= True)
    checkBankFork = models.CharField(max_length= 20, null= True)
    checkBankForkcode = models.CharField(max_length= 12, null= True)
    checkPayDate = models.CharField(max_length= 10, null= True)
    checkPrice = models.IntegerField(null= True)
    checkDetail = models.CharField(max_length= 1000)
    checkCreatetime = models.DateTimeField(null= True)
    checkLastupdate = models.DateTimeField(null= True)
    checkStatus = models.IntegerField(default= 1)
    # check_studentID = models.IntegerField(null= False)
    check_studentID = models.ForeignKey("Student", on_delete=models.CASCADE, db_column="check_studentID")
    class Meta:
        db_table = "check"

class Cities(models.Model):
    id = models.IntegerField(primary_key = True)
    # province_id = models.IntegerField(null= False)
    province_id = models.ForeignKey("Provinces", on_delete=models.CASCADE, db_column="province_id")
    name = models.CharField(max_length= 255)
    class Meta:
        db_table = "cities"

class Classess(models.Model):
    classessID = models.AutoField(primary_key= True)
    classessCode = models.CharField(max_length= 20, null= True)
    classess_courseID = models.ForeignKey("Course", on_delete=models.CASCADE, db_column= "classess_courseID")
    classess_levelID = models.ForeignKey("Level", on_delete=models.CASCADE, db_column= "classess_levelID")
    classessTitle = models.CharField(max_length= 40, null= True)
    classessSex = models.CharField(max_length= 15, null= True)
    classessStartDate = models.CharField(max_length= 10, null= True)
    classessEndDate = models.CharField(max_length= 10, null= True)
    classessExamDate = models.CharField(max_length= 10, null= True)
    classessType = models.CharField(max_length= 40, null= True)
    classessCreateTime = models.DateTimeField(null= True, auto_now_add=True)
    classessLastUpdate = models.DateTimeField(null= True)
    classessStatus = models.IntegerField(default= 1)
    class Meta:
        db_table= "classess"

class Cost(models.Model):
    costID = models.IntegerField(primary_key= True)
    costCaption = models.CharField(max_length= 50, null= True)
    costCategory = models.IntegerField()
    costPrice = models.CharField(max_length= 6, null= True)
    costDate = models.DateTimeField(auto_now_add= True)
    costPicture = models.CharField(max_length= 100, null= True)
    costDescription = models.CharField(max_length= 500, null= True)
    costCreateTime = models.DateTimeField(auto_now_add= True, null= True)
    costLastUpdate = models.DateTimeField(auto_now_add= True, null= True)
    costStatus = models.IntegerField(default= 1)
    class Meta:
        db_table = "cost"

class CostCategory(models.Model):
    costcategoryID = models.IntegerField(primary_key= True)
    costcategoryName = models.CharField(max_length= 50)
    costcategoryParrent = models.IntegerField(default= 0, null= True)
    costcategoryLastupdate = models.DateTimeField(auto_now_add= True, null= True)
    class Meta:
        db_table = "costCategory"

class Course(models.Model):
    courseID = models.AutoField(primary_key= True)
    courseCaption = models.CharField(max_length= 50)
    courseCreateTime = models.DateTimeField(null= True, auto_now_add= True)
    courseLastupdate = models.DateTimeField(null= True)
    courseStatus = models.IntegerField(default= 0)
    class Meta:
        db_table = "course"

class Inventory(models.Model):
    inventoryID = models.AutoField(primary_key= True)
    inventoryTitle = models.CharField(max_length= 5)
    inventoryCount = models.IntegerField()
    inventoryPrice = models.IntegerField()
    inventoryCreatetime = models.DateTimeField(null= True, auto_now_add=True)
    inventoryLastupdate = models.DateTimeField(null= True)
    inventoryStatus = models.IntegerField(default= 1, null= True)
    inventory_levelID = models.ForeignKey("Level", on_delete=models.CASCADE, db_column="inventory_levelID")
    inventory_courseID = models.ForeignKey("Course", on_delete=models.CASCADE, db_column="inventory_courseID")
    class Meta:
        db_table = "inventory"

class Level(models.Model):
    levelID = models.AutoField(primary_key= True)
    levelTitle = models.CharField(max_length = 50)
    levelNumber = models.IntegerField(null= True)
    levelQuiz1 = models.CharField(max_length= 10)
    levelQuiz2 = models.CharField(max_length= 10)
    levelQuiz3 = models.CharField(max_length= 10)
    levelQuiz4 = models.CharField(max_length= 10)
    levelQuiz5 = models.CharField(max_length= 10)
    levelQuiz6 = models.CharField(max_length= 10)
    levelQuiz7 = models.CharField(max_length= 10)
    levelFinal = models.CharField(max_length= 10)
    levelCreatetime = models.DateTimeField(null= True, auto_now_add= True)
    levelLastupdate = models.DateTimeField(null= True)
    levelStatus = models.IntegerField(default= 1) 
    class Meta:
        db_table= "level"

class Order(models.Model):
    orderID = models.IntegerField(primary_key= True)
    orderName = models.CharField(max_length= 50)
    orderfamily = models.CharField(max_length= 50)
    orderMobile = models.CharField(max_length= 50)
    orderEmail = models.CharField(max_length=50)
    orderOstan = models.IntegerField()
    orderCity = models.IntegerField()
    orderRestaurantname = models.CharField(max_length= 200)
    orderRestaurantTell = models.CharField(max_length= 50)
    orderRestaurantAddress = models.CharField(max_length= 500)
    orderPackage = models.IntegerField()
    orderPackageName = models.CharField(max_length= 200, null= True)
    orderPrice = models.CharField(max_length= 50)
    orderDiscount = models.CharField(max_length= 50)
    orderDiscountCode = models.CharField(max_length= 50, null= True)
    orderPayprice = models.CharField(max_length= 50)
    orderAgentcode = models.CharField(max_length= 50, null= True)
    orderIn = models.CharField(max_length= 50, null= True)
    orderPaymethod = models.IntegerField(default= 0)
    orderPaystatus = models.IntegerField(default= 0)
    orderPaytime = models.DateTimeField(null= True)
    orderCreatetime = models.DateTimeField()
    orderLastupdate = models.DateTimeField(null= True)
    orderStatus = models.IntegerField()
    class Meta:
        db_table = "order"

class Payed(models.Model):
    payedID = models.IntegerField(primary_key= True)
    payed_registerID = models.ForeignKey("Register", on_delete=models.CASCADE, db_column="payed_registerID")
    payed_studentID = models.ForeignKey("Student", on_delete=models.CASCADE, db_column="payed_studentID")
    payed_courseID = models.ForeignKey("Course", on_delete=models.CASCADE, db_column="payed_courseID")
    payed_levelID = models.ForeignKey("Level", on_delete=models.CASCADE, db_column="payed_levelID")
    payedMethod = models.IntegerField()
    payedDate = models.DateTimeField(null= True)
    payedPayprice = models.CharField(max_length= 9)
    payedCreatedate = models.DateTimeField(null= True)
    payedStatus = models.IntegerField(default = 1)
    class Meta:
        db_table=  "payed"

class Profile(models.Model):
    profile_id = models.IntegerField(primary_key= True)
    # profile_user_ID = models.IntegerField(null = False)
    profile_user_ID = models.ForeignKey("User", on_delete=models.CASCADE, db_column="profile_user_ID")
    profile_avatar = models.CharField(max_length= 150, null= True)
    profile_nickname = models.CharField(max_length= 20)
    profile_mobile = models.CharField(max_length= 50, null= True)
    profile_tell = models.CharField(max_length= 50, null= True)
    profile_state = models.CharField(max_length= 20, null= True)
    profile_city = models.CharField(max_length= 20, null= True)
    profile_area = models.CharField(max_length= 20, null= True)
    profile_address = models.CharField(max_length= 150, null= True)
    profile_bankname = models.CharField(max_length= 20, null= True)
    profile_cardnumber = models.CharField(max_length= 19, null= True)
    profile_sheba = models.CharField(max_length= 25, null= True)
    profile_facebook = models.CharField(max_length= 25, null= True)
    profile_instagram = models.CharField(max_length= 20, null= True)
    profile_google = models.CharField(max_length= 20, null= True)
    profile_twitter = models.CharField(max_length= 20, null= True)
    profile_link = models.CharField(max_length= 20, null= True)
    class Meta:
        db_table= "profile"

class Provinces(models.Model):
    id = models.IntegerField(primary_key= True)
    name = models.CharField(max_length= 255)
    class Meta:
        db_table = "provinces"

class Register(models.Model):
    registerID = models.AutoField(primary_key= True)
    register_studentID = models.ForeignKey("Student", on_delete=models.CASCADE, db_column="register_studentID")
    register_courseID = models.ForeignKey("Course", on_delete=models.CASCADE, db_column="register_courseID")
    register_levelID = models.ForeignKey("Level", on_delete=models.CASCADE, db_column="register_levelID")
    registerShahrieh = models.CharField(max_length= 20, null= True)
    registerPaymethod = models.IntegerField(default= 1)
    registerPayment = models.IntegerField(default= 1, null= True)
    registerIsdiscount = models.IntegerField(default= 0, null= True)
    registerDiscount = models.CharField(max_length= 20, null= True)
    registerpayPrice = models.CharField(max_length= 20, null= True)
    registerPayed = models.CharField(max_length= 20, null= True)
    registerMustpay = models.CharField(max_length= 20, null= True)
    registerCreateTime = models.DateTimeField(null= True, auto_now_add= True)
    registerLastupdate = models.DateTimeField(null= True)
    registerStatus = models.IntegerField(default= 1)
    registerInventorysID = models.ForeignKey("Inventory", on_delete=models.CASCADE, db_column="registerInventorysID", null= True)
    registerInventorysprice = models.IntegerField(default= 0, null= True)
    registerInventorys2ID = models.ForeignKey("Inventory", on_delete=models.CASCADE, related_name="inventoryID2", db_column="registerInventorys2ID", null= True)
    registerInventorys2price = models.IntegerField(default= 0, null= True)
    registerInventorys3ID = models.ForeignKey("Inventory", on_delete=models.CASCADE, related_name="inventoryID3", db_column="registerInventorys3ID", null= True)
    registerInventorys3price = models.IntegerField(default= 0, null= True)
    register_classessID = models.ForeignKey("Classess", on_delete=models.CASCADE, db_column="register_classessID", null= True)
    class Meta:
        db_table = "register"

    def save(self, *args, **kwargs):
        if self.registerInventorysID == 0:
            self.registerInventorysID = None

        if self.registerInventorys2ID == 0:
            self.registerInventorys2ID = None

        if self.registerInventorys3ID == 0:
            self.registerInventorys3ID = None

        super().save(*args, **kwargs)
        
class Score(models.Model):
    scoreID = models.AutoField(primary_key= True)
    score_studentID = models.ForeignKey("Student", on_delete=models.CASCADE, db_column="score_studentID")
    score_courseID = models.ForeignKey("Course", on_delete=models.CASCADE, db_column="score_courseID")
    score_levelID = models.ForeignKey("Level", on_delete=models.CASCADE, db_column="score_levelID")
    scoreCardnumber = models.CharField(max_length= 10, null= True)
    scoreRoom = models.CharField(max_length= 50, null= True)
    scoreHour= models.CharField(max_length= 50, null= True)
    scoreDays = models.CharField(max_length= 50, null= True)
    scoreProceed = models.IntegerField(default= 0)
    scoreOral = models.IntegerField(default= 0)
    scoreAverage = models.IntegerField(default= 0)
    scorePerformance = models.IntegerField(default= 0)
    scoreFinal = models.IntegerField(default= 0)
    scoreTotal = models.IntegerField(default= 0)
    scoreProceed = models.IntegerField(default= 0)
    scoreTeacherName = models.CharField(max_length= 100, null= True)
    scoreCreateTime = models.DateTimeField(null= True)
    scoreLastupdate = models.DateTimeField(null= True)
    scoreStatus = models.IntegerField(default= 1)
    class Meta:
        db_table= "score"

class Student(models.Model):
    studentID = models.AutoField(primary_key= True)
    studentName = models.CharField(max_length= 50)
    studentFamily = models.CharField(max_length= 100)
    studentPedar = models.CharField(max_length= 50)
    studentMelli = models.CharField(max_length= 10)
    studentShenasnameh = models.CharField(max_length= 10, null= True)
    studentSodoor = models.CharField(max_length= 20, null= True)
    studenttavalod = models.CharField(max_length= 20, null= True)
    studentMadrak = models.CharField(max_length= 20)
    studentSex = models.IntegerField()
    studentOstan = models.CharField(max_length= 50)
    studentCity = models.CharField(max_length= 20, null= True)
    studentTell = models.CharField(max_length= 50, null= True)
    studentPedarmobile = models.CharField(max_length= 20, null= True)
    studentMadarmobile = models.CharField(max_length= 20, null= True)
    studentAddress = models.CharField(max_length= 250, null= True)
    studentNaghs = models.IntegerField(default= 1)
    studentCreatetime = models.DateTimeField(auto_now_add= True, null= True)
    studentLastUpdate = models.DateTimeField(null= True)
    studentStatus = models.IntegerField(default= 1)
    class Meta:
        db_table= "student"

class Teacher(models.Model):
    teacherID = models.IntegerField(primary_key= True)
    teacherName = models.CharField(max_length= 50)
    teacherFamily = models.CharField(max_length= 100)
    teacherPedar = models.CharField(max_length= 50)
    teacherMelli = models.CharField(max_length= 10)
    teacherShenasnameh = models.CharField(max_length= 10, null= True)
    teacherSodoor = models.CharField(max_length= 20, null= True)
    teacherTavalod = models.CharField(max_length= 20, null= True)
    teacherMadrak = models.CharField(max_length= 20)
    teacherSex = models.IntegerField()
    teacherOstan = models.CharField(20)
    teacherCity = models.CharField(max_length= 20, null= True)
    teacherTell = models.CharField(max_length= 50, null= True)
    teacherAddress = models.CharField(max_length= 250, null= True)
    teacherNaghs = models.IntegerField(default= 0)
    teacherCreateTime = models.DateTimeField(auto_now_add= True, null= True)
    teacherLastupdate = models.DateTimeField(null= True)
    teacherStatus = models.IntegerField(default= 1)
    class Meta:
        db_table = "teacher"

class Tuition(models.Model):
    tuitionID = models.AutoField(primary_key= True)
    tuition_courseID = models.ForeignKey("Course", on_delete=models.CASCADE, db_column="tuition_courseID")
    tuition_levelID = models.ForeignKey("Level", on_delete=models.CASCADE, db_column="tuition_levelID")
    tuitionPrice = models.CharField(max_length= 20)
    tuitionCreateTime = models.DateTimeField(null= True, auto_now_add= True)
    tuitionLastupdate = models.DateTimeField(null= True)
    tuitionStatus = models.IntegerField(default= 1)
    class Meta:
        db_table = "tuition"

class User(models.Model):
    user_id = models.AutoField(primary_key= True)
    user_parent_id = models.IntegerField(default= 0)
    user_name = models.CharField(max_length= 50)
    user_email = models.CharField(max_length= 50)
    user_active_code = models.TextField(null= True)
    user_token = models.CharField(max_length= 50, null= True)
    user_password = models.CharField(max_length= 50)
    user_lastlogin = models.DateTimeField(auto_now_add= True, null= True)
    user_registerdate = models.DateTimeField(auto_now_add= True, null= True)
    user_status = models.IntegerField(default= 1)
    user_access = models.IntegerField()
    user_perm = models.IntegerField()
    class Meta:
        db_table = "user"

