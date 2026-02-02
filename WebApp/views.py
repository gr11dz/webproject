from django.shortcuts import render, redirect, get_list_or_404
from django.http import HttpResponse, Http404
from django.views import View

from . import modelManager as mm

class AdminPage(View):

    def get(self, request):
        student_name_list = mm.CRUD().get_studentfull()
        return render(request, "WebApp/admin.html", {"students": student_name_list})
    
    def post(self, request):
        student_id = request.POST.get("studentID")

        student_data = mm.CRUD().getLearnerData(student_id)

        return render(request, "WebApp/admin.html", {"student_data": student_data})

class Admin_addPay(View):

    def get(self, request, student_id):
        data = mm.CRUD().get_addPay_data(student_id)

        if data == 404:
            raise Http404("No data")

        return render(request, "WebApp/addpay.html", {"data": data})
    
    def post(self, request, student_id):
        if "delete_submit" in request.POST:
            registerID = request.POST.get("registerID")
            crud = mm.CRUD()
            if mm.CRUD().delete_register(registerID) == 404:
                raise Http404
            data = crud.get_addPay_data(student_id)
            return render(request, "WebApp/addpay.html", {"data": data, "success": True})

        payment_method = request.POST.get("paymentMethod")
        pay_amount = request.POST.get("payAmount")

        crud = mm.CRUD()
        if crud.set_payment(student_id, pay_amount, payment_method) == 200:
            data = crud.get_addPay_data(student_id)
            return render(request, "WebApp/addpay.html", {"data": data, "success": True})
        else:
            raise Http404("Not Found")

class Register(View):
    def get(self, request):

        data = mm.CRUD().get_register()
        return render(request, "WebApp/register.html", {"data": data})
    
    def post(self, request):
        register_id = request.POST.get("registerID")
        crud = mm.CRUD()
        if crud.delete_register(register_id) == 404:
            print("test")
            raise Http404

        data = crud.get_register()
        return render(request, "WebApp/register.html", {"data": data}) 
        
class Classes(View):
    def get(self, request):

        data = mm.CRUD().get_classes_details()

        return render(request, "WebApp/classes.html", {"data": data})

class ClassList(View):
    def get(self, request, classID):
       
       data = mm.CRUD().get_student_class(classID)

       return render(request, "WebApp/classList.html", {"data": data})

class Class_alterstudent(View):
    def get(self, request, classID):
        data = mm.CRUD().get_addstudent(classID)

        return render(request, "WebApp/class_addstudent.html", {"data": data})

    def post(self, request, classID):
        studentID = request.POST.get("studentID")

        crud = mm.CRUD()
        if crud.update_register_class(studentID) == 404:
            raise Http404
        data = crud.get_addstudent(classID)

        return render(request, "WebApp/class_addstudent.html", {"data": data})
    
class CalenderList(View):
    def get(self, request):
        data = mm.CRUD().get_calender_list()
        return render(request, "WebApp/calenderList.html", {"data":data})

    def post(self, request):
        calenderID = request.POST.get("calenderID")

        crud = mm.CRUD()
        if crud.delete_calender(calenderID) == 404:
            raise Http404
        
        data = mm.CRUD().get_calender_list()
        return render(request, "WebApp/calenderList.html", {"data": data})

class ScoreList(View):
    def get(self, request):

        data = mm.CRUD().get_score()
        return render(request, "WebApp/scoreList.html", {"data": data})
    
    def post(self, request):
        scoreID = request.POST.get("scoreID")
        if mm.CRUD().delete_score(scoreID) == 404:
            raise Http404
        return redirect("scorelist")


class AddStudent(View):
    def get(self, request):
        data = mm.CRUD().get_province_cities()
        return render(request, "WebApp/studentinsert.html", {"data": data})
    
    def post(self, request):
        data = list()
        data.append(request.POST.get("firstname"))
        data.append(request.POST.get("lastname"))
        data.append(request.POST.get("nationalID"))
        data.append(request.POST.get("fathername"))
        data.append(request.POST.get("fatherphone"))
        data.append(request.POST.get("motherphone"))
        data.append(request.POST.get("phone"))
        data.append(request.POST.get("shenasnamehID"))
        data.append(request.POST.get("gender"))
        data.append(request.POST.get("certificate"))
        data.append(request.POST.get("provinceID"))
        data.append(request.POST.get("citiesID"))
        data.append(request.POST.get("sodoor"))
        data.append(request.POST.get("birthplace"))
        data.append(request.POST.get("address"))
        data.append(request.POST.get("incomplete"))

        crud= mm.CRUD()
        if crud.set_student(data) == 404:
            raise Http404
        
        return redirect("studentlist")
    
class StudentList(View):
    def get(self, request):

        data = mm.CRUD().get_studentfull()
        return render(request, "WebApp/studentList.html", {"data": data})
    def post(self, request):
        studentID = request.POST.get("studentID")

        crud = mm.CRUD()
        if crud.delete_student(studentID) == 404:
            raise Http404
        
        data = crud.get_studentfull()
        return render(request, "WebApp/studentList.html", {"data": data})

class TeacherList(View):
    def get(self, request):
        data = mm.CRUD().get_teacherfull()
        return render(request, "WebApp/teacherList.html", {"data": data})
    
    def post(self, request):
        teacherID = request.POST.get("teacherID")
        print(teacherID)
        crud = mm.CRUD()
        if crud.delete_teacher(teacherID) == 404:
            raise Http404
        
        data = crud.get_teacherfull()
        return render(request, "WebApp/studentList.html", {"data": data})

class Addteacher(View):
    def get(self, request):
        data = mm.CRUD().get_province_cities()
        return render(request, "WebApp/teacherinsert.html", {"data": data})
    def post(self, request):
        data = list()
        data.append(request.POST.get("firstname"))
        data.append(request.POST.get("lastname"))
        data.append(request.POST.get("nationalID"))
        data.append(request.POST.get("fathername"))
        data.append(request.POST.get("phone"))
        data.append(request.POST.get("shenasnamehID"))
        data.append(request.POST.get("gender"))
        data.append(request.POST.get("certificate"))
        data.append(request.POST.get("provinceID"))
        data.append(request.POST.get("citiesID"))
        data.append(request.POST.get("sodoor"))
        data.append(request.POST.get("birthplace"))
        data.append(request.POST.get("address"))
        data.append(request.POST.get("incomplete"))

        crud= mm.CRUD()
        if crud.set_teacher(data) == 404:
            raise Http404
        
        return redirect("teacherlist")
    
class InventoryList(View):
    def get(self, request):

        data, table= mm.CRUD().get_inventoryIndex()
        return render(request, "WebApp/inventoryIndex.html", {"data": data, "table": table})
    def post(self, request):
        courseID = request.POST.get("courseID")
        inventoryTitle = request.POST.get("inventoryTitle")
        inventoryamount = request.POST.get("inventoryamount")
        inventoryprice = request.POST.get("inventoryprice")
        levelID = request.POST.get("levelID")

        crud = mm.CRUD()
        result = crud.set_inventory(courseID, levelID, inventoryprice, inventoryamount, inventoryTitle)
        if result == 404:
            raise Http404
        data, table = crud.get_inventoryIndex()
        return render(request, "WebApp/inventoryIndex.html", {"data": data, "table": table})

class CourseList(View):
    def get(self, request):

        table = mm.CRUD().get_courselist()
        return render(request, "WebApp/courseIndex.html", {"table": table})
    def post(self, request):
        courseCaption = request.POST.get("courseCaption")
        crud = mm.CRUD()
        crud.set_course(courseCaption)
        table = crud.get_courselist()
        return render(request, "WebApp/courseIndex.html", {"table": table})
    
class levelList(View):
    def get(self, request):
        table = mm.CRUD().get_levelList()
        return render(request, "WebApp/levelList.html", {"table": table})

    def post(self, request):
        levelTitle = request.POST.get("title")
        levelNumber = request.POST.get("number")
        quiz_list = list()
        quiz_list.append(request.POST.get("quiz1"))
        quiz_list.append(request.POST.get("quiz2"))
        quiz_list.append(request.POST.get("quiz3"))
        quiz_list.append(request.POST.get("quiz4"))
        quiz_list.append(request.POST.get("quiz5"))
        quiz_list.append(request.POST.get("quiz6"))
        quiz_list.append(request.POST.get("quiz7"))
        quiz_list.append(request.POST.get("final"))

        crud = mm.CRUD()
        if crud.set_level(levelTitle, levelNumber, quiz_list) == 404:
            raise Http404
        table = crud.get_levelList()
        return render(request, "WebApp/levelList.html", {"table": table})

class TuitionList(View):
    def get(self, request):
        data, table = mm.CRUD().get_tuitionList()
        return render(request, "WebApp/tuitionList.html", {"data": data, "table": table})
    
    def post(self, request):
        courseID = request.POST.get("courseID")
        levelID = request.POST.get("levelID")
        price = request.POST.get("price")

        crud = mm.CRUD()
        if crud.set_tuition(courseID, levelID, price):
            return Http404
        data, table = crud.get_tuitionList()
        return render(request, "WebApp/tuitionList.html", {"data": data, "table": table})
    
class checkList(View):
    def get(self, request):
        
        table = mm.CRUD().get_checkList()
        return render(request, "WebApp/checkList.html", {"table": table})

class InventoryCopy(View):
    def get(self, request):
        course = mm.CRUD().get_courselist()
        return render(request, "WebApp/inventoryCopy.html", {"course": course})
    
    def post(self, request):
        old_courseID = request.POST.get("caption1")
        new_courseID = request.POST.get("caption2")
        raised_price = request.POST.get("raisedPrice")

        mm.CRUD().copy_inventory(old_courseID, new_courseID, raised_price)
        return redirect("inventorylist")

class ReportIndex(View):
    def get(self, request):

        course = mm.CRUD().get_courselist()
        return render(request, "WebApp/reportIndex.html", {"course": course})
    def post(self, request):
        courseID = request.POST.get("caption")
        return redirect("reportget", courseID)
    
class ReportGet(View):
    def get(self, request, courseID):
        crud = mm.CRUD()
        course = crud.get_courselist()
        values = crud.get_report_details(courseID)
        data = crud.get_report(courseID)
        detailed_tables = crud.get_report_levels_detailed(courseID)
        return render(request, "WebApp/reportGet.html", {"course": course, "data": data, "values": values, "table": detailed_tables})
    def post(self, request, courseID):
        courseID = request.POST.get("caption")
        return redirect("reportget", courseID)
    
class levelIndex(View):
    def get(self, request):
        course = mm.CRUD().get_courselist()
        return render(request, "WebApp/reportIndex.html", {"course": course})
    def post(self, request):
        courseID = request.POST.get("caption")
        crud = mm.CRUD()

        course = crud.get_courselist()
        data = crud.get_report_levels(courseID)
        return render(request, "WebApp/levelindex.html", {"course": course, "data": data})
    
class levelTable(View):
    def get(self, request, courseID, levelID):

        data = mm.CRUD().get_report_level_table(courseID, levelID)
        course = mm.CRUD().get_courselist()
        return render(request, "WebApp/reportlevelTable.html", {"data": data, "course": course})

class StudentUpdate(View):
    def get(self, request, studentID):
        data = mm.CRUD().get_province_cities()
        return render(request, "WebApp/studentinsert.html", {"data": data})
    
    def post(self, request, studentID):
        data ={
            "firstname": request.POST.get("firstname"),
            "lastname" : request.POST.get("lastname"),
            "nationalID" : request.POST.get("nationalID"),
            "fathername" : request.POST.get("fathername"),
            "fatherphone" : request.POST.get("fatherphone"),
            "motherphone" : request.POST.get("motherphone"),
            "phone" : request.POST.get("phone"),
            "shenasnamehID" : request.POST.get("shenasnamehID"),
            "gender" : request.POST.get("gender"),
            "certificate" : request.POST.get("certificate"),
            "provinceID" : request.POST.get("provinceID"),
            "citiesID" : request.POST.get("citiesID"),
            "sodoor" : request.POST.get("sodoor"),
            "birthplace" : request.POST.get("birthplace"),
            "address" : request.POST.get("address"),
            "incomplete" : request.POST.get("incomplete"),
        }

        crud = mm.CRUD()
        if crud.update_student(studentID, data) == 404:
            raise Http404
        return redirect("studentlist")

class TeacherUpdate(View):
    def get(self, request, teacherID):
        data = mm.CRUD().get_province_cities()
        return render(request, "WebApp/teacherinsert.html", {"data": data})
    def post(self, request, teacherID):
        data = {
            "firstname": request.POST.get("firstname"),
            "lastname": request.POST.get("lastname"),
            "nationalID": request.POST.get("nationalID"),
            "fathername": request.POST.get("fathername"),
            "phone": request.POST.get("phone"),
            "shenasnamehID": request.POST.get("shenasnamehID"),
            "gender": request.POST.get("gender"),
            "certificate": request.POST.get("certificate"),
            "provinceID": request.POST.get("provinceID"),
            "citiesID": request.POST.get("citiesID"),
            "sodoor": request.POST.get("sodoor"),
            "birthplace": request.POST.get("birthplace"),
            "address": request.POST.get("address"),
            "incomplete": request.POST.get("incomplete"),
        }
        if mm.CRUD().update_teacher(teacherID, data) == 404:
            return Http404
        return redirect("teacherlist")

class LevelUpdate(View):
    def get(self, request, levelID):
        data = mm.CRUD().get_level(levelID)
        if data == 404:
            raise Http404
        
        return render(request, "WebApp/levelupdate.html", {"data": data})
    def post(self, request, levelID):
        levelTitle = request.POST.get("title")
        levelNumber = request.POST.get("number")
        quiz_list = list()
        quiz_list.append(request.POST.get("quiz1"))
        quiz_list.append(request.POST.get("quiz2"))
        quiz_list.append(request.POST.get("quiz3"))
        quiz_list.append(request.POST.get("quiz4"))
        quiz_list.append(request.POST.get("quiz5"))
        quiz_list.append(request.POST.get("quiz6"))
        quiz_list.append(request.POST.get("quiz7"))
        quiz_list.append(request.POST.get("final"))

        if mm.CRUD().update_level(levelID, levelTitle, levelNumber, quiz_list) == 404:
            raise Http404
        return redirect("levellist")
    
class TuitionUpdate(View):
    def get(self, request, tuitionID):
        crud = mm.CRUD()
        level = crud.get_levelList()
        course = crud.get_courselist()

        return render(request, "WebApp/tuitionupdate.html", {"level": level, "course": course})
    
    def post(self, request, tuitionID):
        courseID = request.POST.get("courseID")
        levelID = request.POST.get("levelID")
        price = request.POST.get("price")

        crud = mm.CRUD()
        if crud.update_tuition(tuitionID, levelID, courseID, price) == 404:
            raise Http404
        return redirect("tuitionlist")

class InventoryUpdate(View):
    def get(self, request, inventoryID):
        crud = mm.CRUD()
        course = crud.get_courselist()
        level = crud.get_levelList()

        return render(request, "WebApp/inventoryupdate.html", {"course": course, "level": level})
    def post(self, request, inventoryID):
        courseID = request.POST.get("courseID")
        inventoryTitle = request.POST.get("inventoryTitle")
        inventoryamount = request.POST.get("inventoryamount")
        inventoryprice = request.POST.get("inventoryprice")
        levelID = request.POST.get("levelID")

        crud = mm.CRUD()
        if crud.update_inventory(courseID, levelID, inventoryprice, inventoryamount, inventoryTitle, inventoryID) == 404:
            raise Http404
        return redirect("inventorylist")
    
class Profile(View):
    def get(self, request):
        data = mm.CRUD().get_province_cities()
        return render(request, "WebApp/profile.html", {"data": data})
    def post(self, request):
        data = dict()
        data["username"] = request.POST.get("username")
        data["fullname"] = request.POST.get("fullname")
        data["phone"] = request.POST.get("phone")
        data["phone2"] = request.POST.get("phone2")
        data["password"] = request.POST.get("password")
        data["email"] = request.POST.get("email")
        data["sarparast"] = request.POST.get("sarparast")
        data["provinceID"] = request.POST.get("provinceID")
        data["citiesID"] = request.POST.get("citiesID")
        data["address"] = request.POST.get("address")
        data["password2"] = request.POST.get("password2")
        data["bankname"] = request.POST.get("bankname")
        data["cardnumber"] = request.POST.get("cardnumber")
        data["ibannumber"] = request.POST.get("ibannumber")

        if mm.CRUD().set_user(data) == 404:
            raise Http404
        return redirect("admin")

class RegisterAdd(View):
    def get(self, request):
        crud = mm.CRUD()
        student = crud.get_student()
        level = crud.get_levelList()
        classes = crud.get_classes()
        course = crud.get_courselist()
        inventory = crud.get_inventory()

        return render(request, "WebApp/registeradd.html", {"student": student, "level": level,"classes": classes,"course": course,"inventory": inventory})
                                                   
    def post(self, request):
        data= {
            "studentID": request.POST.get("studentID"),
            "quarterID": request.POST.get("quarter"),
            "levelID": request.POST.get("level"),
            "classID": request.POST.get("class"),
            "inventory1ID": request.POST.get("inventory1"),
            "inventory2ID": request.POST.get("inventory2"),
            "inventory3ID": request.POST.get("inventory3"),
            "fee": request.POST.get("fee"),
            "isdiscount": request.POST.get("isdiscount"),
            "discount": request.POST.get("discount"),
            "paymethod": request.POST.get("paymentMethod"),
            "payed": request.POST.get("payed"),
        }
        if mm.CRUD().set_register(data) == 404:
            raise Http404
        return redirect("register")

class ClassAdd(View):
    def get(self, request):
        crud = mm.CRUD()
        course = crud.get_courselist()
        level = crud.get_levelList()

        return render(request, "WebApp/classadd.html", {"course": course, "level": level})
    def post(self, request):
        data ={
            "title": request.POST.get("title"),
            "courseID": request.POST.get("quarter"),
            "levelID": request.POST.get("level"),
            "gender": request.POST.get("gender"),
            "type": request.POST.get("type"),
            "startdate": request.POST.get("startdate"),
            "enddate": request.POST.get("enddate"),
        }
        if mm.CRUD().set_class(data) == 404:
            raise Http404
        return redirect("classes")
    
class CalenderAdd(View):
    def get(self, request):
        crud = mm.CRUD()
        level = crud.get_levelList()
        course = crud.get_courselist()
        classes = crud.get_classes()
        return render(request, "WebApp/calenderadd.html", {"level": level, "course": course, "class": classes})

    def post(self, request):
        data={
            "courseID": request.POST.get("quarter"),
            "levelID": request.POST.get("level"),
            "classID": request.POST.get("class"),
            "startdate": request.POST.get("startdate"),
            "enddate": request.POST.get("enddate"),
            "shanbe": request.POST.get("shanbe"),
            "yekshanbe": request.POST.get("yekshabe"),
            "doshanbe": request.POST.get("doshanbe"),
            "seshanbe": request.POST.get("seshanbe"),
            "chaharshanbe": request.POST.get("chaharshanbe"),
            "panjshanbe": request.POST.get("panjshanbe"),
            "jome": request.POST.get("jome"),
        }
        if mm.CRUD().set_calender(data) == 404:
            raise Http404
        return redirect("calenderlist")
    
class ScoreAdd(View):
    def get(self, request):
        crud = mm.CRUD()
        student = crud.get_student()
        course = crud.get_courselist()
        level = crud.get_levelList()

        return render(request, "WebApp/scoreadd.html", {"student": student, "course": course, "level": level})
    def post(self, request):
        data={
            "studentID": request.POST.get("studentID"),
            "courseID": request.POST.get("quarter"),
            "levelID": request.POST.get("level"),
            "cardnumber": request.POST.get("cardnumber"),
            "room": request.POST.get("room"),
            "hour": request.POST.get("hour"),
            "days": request.POST.get("days"),
            "proceed": request.POST.get("proceed"),
            "oral": request.POST.get("oral"),
            "quiz": request.POST.get("quiz"),
            "class": request.POST.get("class"),
            "final": request.POST.get("final"),
            "total": request.POST.get("total")
        }
        if mm.CRUD().set_score(data) == 404:
            raise Http404
        return redirect("scorelist")

class RegisterUpdate(View):
    def get(self, request, registerID):
        crud = mm.CRUD()
        student = crud.get_student()
        level = crud.get_levelList()
        classes = crud.get_classes()
        course = crud.get_courselist()
        inventory = crud.get_inventory()
        table = crud.get_register_table(registerID)
        return render(request, "WebApp/registeradd.html", {"student": student, "level": level,"classes": classes,"course": course,"inventory": inventory, "table": table})
    def post(self, request, registerID):
        data= {
            "studentID": request.POST.get("studentID"),
            "quarterID": request.POST.get("quarter"),
            "levelID": request.POST.get("level"),
            "classID": request.POST.get("class"),
            "inventory1ID": request.POST.get("inventory1"),
            "inventory2ID": request.POST.get("inventory2"),
            "inventory3ID": request.POST.get("inventory3"),
            "fee": request.POST.get("fee"),
            "isdiscount": request.POST.get("isdiscount"),
            "discount": request.POST.get("discount"),
            "paymethod": request.POST.get("paymentMethod"),
            "payed": request.POST.get("payed"),
        }
        if mm.CRUD().update_register(data, registerID) == 404:
            return 404
        return redirect("register")

class ClassUpdate(View):
    def get(self, request, classID):
        crud = mm.CRUD()
        course = crud.get_courselist()
        level = crud.get_levelList()

        return render(request, "WebApp/classadd.html", {"course": course, "level": level})
    def post(self, request, classID):
        data ={
            "title": request.POST.get("title"),
            "courseID": request.POST.get("quarter"),
            "levelID": request.POST.get("level"),
            "gender": request.POST.get("gender"),
            "type": request.POST.get("type"),
            "startdate": request.POST.get("startdate"),
            "enddate": request.POST.get("enddate"),
        }
        if mm.CRUD().update_class(data, classID) == 404:
            raise Http404
        return redirect("classes")