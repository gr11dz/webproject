from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Count

from .models import *
#singleton
class CRUD:
    def __init__(self):
        pass

    def getStudentList(self) -> list:
        students = Student.objects.all()
        student_name_list= list()
        for iter in students:
            fullname = iter.studentName + iter.studentFamily
            student_name_list.append(fullname)

        return student_name_list

    def getLearnerData(self, student_id):
        student = Student.objects.get(studentID= student_id)
        try:
            register = Register.objects.get(register_studentID = student_id)
            level = register.register_levelID
        except ObjectDoesNotExist:
            # register= None
            # level = None
            return None

        try:
            score = Score.objects.get(score_studentID= student_id)
        except Score.DoesNotExist:
            score= None

        student_data= {
            "student":{
                "id": student.studentID,
                "name": student.studentName,
                "family": student.studentFamily,
                "nationID": student.studentMelli,
                "phone": student.studentTell,
                "momPhone": student.studentMadarmobile,
                "fatherPhone": student.studentPedarmobile,
            },
            "level":{
                "title": level.levelTitle
            },
            "register":{
                "createTime": register.registerCreateTime,
                "fee": register.registerShahrieh,
                "discount": register.registerDiscount,
                "alreadyPayed": register.registerPayed,
                "remainingPay": register.registerMustpay,
            },
            "score":{
                "total": score.scoreTotal if score else None
            }
        }

        return student_data
    
    def get_addPay_data(self, student_id):
        try:
            student = Student.objects.get(studentID = student_id)
            register_list = Register.objects.filter(register_studentID= student_id)
        except (Student.DoesNotExist, Register.DoesNotExist):
            return 404

        table = list()
        alreadypayed_counter = 0
        remainingpay_counter = 0
        fee_counter = 0
        paymentMethod = None

        for reg in register_list:
            course = reg.register_courseID
            level = reg.register_levelID
            
            if method:=reg.registerPaymethod:
                match method:
                    case 1:
                        paymentMethod = "نقدی"
                    case 2:
                        paymentMethod = "واریز حساب"
                    case 3:
                        paymentMethod = "کارت"
                    case 4:
                        paymentMethod = "چک"
            else:
                paymentMethod = None

            if not (date:= reg.registerLastupdate):
                date = reg.registerCreateTime

            table.append({
                "registerID": reg.registerID,
                "discount": reg.registerDiscount,
                "fee": reg.registerShahrieh,
                "method": paymentMethod,
                "alreadyPayed": reg.registerPayed,
                "remainingPay": reg.registerMustpay,
                "date": date,
                "quarter": course.courseCaption if course else None,
                "title": level.levelTitle if level else None,
            })
            alreadypayed_counter += int(reg.registerPayed) if reg.registerPayed else 0
            remainingpay_counter += int(reg.registerMustpay) if reg.registerMustpay else 0
            fee_counter += int(reg.registerShahrieh) if reg.registerShahrieh else 0
        

        try:
            register_data = Register.objects.filter(register_studentID= student_id).order_by("registerCreateTime").first()
            if not register_data:
                return 
            course_data = register_data.register_courseID
            level_data = register_data.register_levelID
       
        except Register.DoesNotExist:
            register_data = None

        data ={
            "student":{
                "fullname": f"{student.studentName} {student.studentFamily}"
            },
            "table": table,
            "sum":{
                "payedSum": alreadypayed_counter,
                "oldPaymentSum": remainingpay_counter,
                "payedtotal": alreadypayed_counter + remainingpay_counter,
                "remainingFee": fee_counter - alreadypayed_counter - remainingpay_counter,
            },
            "info":{
                "discount": register_data.registerDiscount,
                "fee": register_data.registerShahrieh,
                "method": register_data.registerPaymethod,
                "alreadyPayed": register_data.registerPayed,
                "remainingPay": register_data.registerMustpay,
                "date": register_data.registerCreateTime,
                "quarter": course_data.courseCaption,
                "title": level_data.levelTitle,
            },
        }
        return data

    def get_register(self):
        register = Register.objects.all()
        
        table = list()
        for iter in register:
            student = iter.register_studentID
            level = iter.register_levelID
            course = iter.register_courseID
            try:
                score = Score.objects.get(score_studentID= student.studentID)
            except Score.DoesNotExist:
                score = None

            table.append({
                "registerID": iter.registerID,
                "fullname": f"{student.studentName} {student.studentFamily}",
                "nationalID": student.studentMelli,
                "course": course.courseCaption,
                "level": level.levelTitle,
                "mark": score.scoreTotal if score else None
            })

        return table
    
    def get_student_class(self, classID):
        try:
            classes = Classess.objects.get(classessID= classID)
            register_list = Register.objects.filter(register_classessID= classID)
        except (Register.DoesNotExist, Classess.DoesNotExist):
            return 404
        
        table = list()
        for register in register_list:
            student = register.register_studentID

            table.append({
                "studentID": student.studentID,
                "nationalID": student.studentMelli,
                "fullname": f"{student.studentName} {student.studentFamily}",
                "phone": student.studentTell,
                "momPhone": student.studentMadarmobile,
                "dadPhone": student.studentPedarmobile,
            })
        level = classes.classess_levelID
        course = classes.classess_courseID

        data={
            "header":{
                "title": classes.classessTitle,
                "classTime": classes.classessType,
                "quarter": course.courseCaption,
                "level": level.levelTitle,
            },
            "table": table,
        }
        return data
    
    def get_addstudent(self, classID):
        try:
            register_list = Register.objects.filter(register_classessID= classID)
            first_table = list()
        except Register.DoesNotExist:
            register_list = None

        for register in register_list:
            student = register.register_studentID

            first_table.append({
                "nationalID": student.studentMelli,
                "fullname": f"{student.studentName} {student.studentFamily}",
                "phone": student.studentTell,
                "momPhone": student.studentMadarmobile,
                "dadphone": student.studentPedarmobile,
            })

        data = self.get_student_class(classID)
        data["first_table"] = first_table

        return data
    
    def get_classes_details(self):

        classes = Classess.objects.all()
        table = list()
        for iter in classes:
            level = iter.classess_levelID
            course = iter.classess_courseID
            table.append({
                "ID": iter.classessID,
                "title": iter.classessTitle,
                "quarter": course.courseCaption,
                "level": level.levelTitle,
                "type": iter.classessType,
                "gender": iter.classessSex,
                "startDate": iter.classessStartDate,
                "endDate": iter.classessEndDate,
            })
        return table

    def get_calender_list(self):
        calender_list = Calender.objects.all()

        table = list()
        for calender in calender_list:
            classes = calender.calender_classessID
            course = calender.calender_courseID
            level = calender.calender_levelID

            table.append({
                "calenderID": calender.calenderID,
                "title": classes.classessTitle,
                "quarter": course.courseCaption,
                "level": level.levelTitle,
                "startDate": calender.calender_startDate,
                "endDate":  calender.calender_endDate,
            })
        return table

    def get_score(self):
        score_list = Score.objects.all()
        table = list()

        for score in score_list:
            student = score.score_studentID
            level = score.score_levelID
            course = score.score_courseID

            table.append({
                "scoreID": score.scoreID,
                "nationalID": student.studentMelli,
                "fullname": f"{student.studentName} {student.studentFamily}",
                "quarter": course.courseCaption,
                "level": level.levelTitle,
                "total": int(score.scoreTotal),
            })
        return table
    
    def get_cities(self) -> list:
        cities_list = Cities.objects.all()
        table= list()

        for iter in cities_list:
            table.append({
                "ID": iter.id,
                "name": iter.name
            })
        return table

    def get_provinces(self) -> list:
        provinces_list = Provinces.objects.all()
        table= list()
        for iter in provinces_list:
            table.append({
                "ID": iter.id,
                "name": iter.name,
            })
        return table

    def get_province_cities(self):
        cities_list = self.get_cities()
        provinces_list = self.get_provinces()

        data = {
            "cities": cities_list,
            "provinces": provinces_list, 
        }
        return data

    def get_studentfull(self) -> list:
        student_list = Student.objects.all()

        table= list()
        for student in student_list:

            table.append({
                "studentID": student.studentID,
                "nationalID": student.studentMelli,
                "fullname": f"{student.studentName} {student.studentFamily}",
                "phone": student.studentTell,
                "motherphone": student.studentMadarmobile,
                "fatherphone": student.studentPedarmobile,
                "incomplete": True if student.studentNaghs == 1 else False,
            })
        return table

    def get_teacherfull(self) -> list:
        teacher_list = Teacher.objects.all()
        table= list()

        for teacher in teacher_list:
            table.append({
                "teacherID": teacher.teacherID,
                "fullname": f"{teacher.teacherName} {teacher.teacherFamily}",
                "phone": teacher.teacherTell,
                "incomplete": teacher.teacherNaghs
            })
        return table

    def get_inventoryIndex(self):
        course_list = Course.objects.all()
        level_list = Level.objects.all()
        data={
            "course": course_list,
            "level": level_list,
        }

        inventory_list = Inventory.objects.all()
        table = list()
        for inventory in inventory_list:
            course = inventory.inventory_courseID
            table.append({
                "inventoryID": inventory.inventoryID,
                "caption": course.courseCaption,
                "title": inventory.inventoryTitle,
                "count": inventory.inventoryCount,
                "price": inventory.inventoryPrice,
                "total": inventory.inventoryPrice * inventory.inventoryCount,
                "createDate": inventory.inventoryCreatetime,
            })
        return data, table
            
    def get_courselist(self) -> list:
        course_list = Course.objects.all()
        table = list()
        for course in course_list:
            table.append({
                "ID": course.courseID,
                "title": course.courseCaption,
                "date": course.courseCreateTime
            })
        return table

    def get_levelList(self) -> list:
        level_list = Level.objects.all()

        table= list()
        for level in level_list:
            table.append({
                "levelID": level.levelID,
                "title": level.levelTitle,
                "createDate": level.levelCreatetime,
            })
        return table

    def get_tuitionList(self):
        tuition_list = Tuition.objects.all()

        table = list()
        for tuition in tuition_list:
            level = tuition.tuition_levelID
            course = tuition.tuition_courseID

            table.append({
                "tuitionID": tuition.tuitionID,
                "caption": course.courseCaption,
                "level": level.levelTitle,
                "price": tuition.tuitionPrice,
                "createDate": tuition.tuitionCreateTime
            })

        data ={
            "level": self.get_levelList(),
            "course": self.get_courselist()
        }
        return data, table

    def get_checkList(self):
        check_list = Check.objects.all()
        table = list()
        for check in check_list:
            register = check.check_registerID
            student = check.check_studentID

            table.append({
                "studentname": f"{student.studentName} {student.studentFamily}",
                "checkdate": check.checkCreatetime,
                "fullname": check.checkBankFullname,
                "checkNumber": check.checkNumber,
                "bank": check.checkBankname,
                "fork": check.checkBankForkcode,
                "price": check.checkPrice,
                "createDate": register.registerCreateTime
            })

        return table

    def get_report(self, courseID):
        payed_list = Payed.objects.filter(payed_courseID= courseID)
        table = list()

        fee_total = 0
        inventory_total = 0
        discount_total = 0
        payed_total = 0
        remaining_total = 0

        for payed in payed_list:
            student = payed.payed_studentID
            register = payed.payed_registerID
            level = payed.payed_levelID
            classes = register.register_classessID

            inventoryPrice = 0
            if register.registerInventorysprice:
                inventoryPrice += register.registerInventorysprice
            if register.registerInventorys2price:
                inventoryPrice += register.registerInventorys2price
            if register.registerInventorys3price:
                inventoryPrice += register.registerInventorys3price

            if register.registerShahrieh:
                fee_total += int(register.registerShahrieh)

            if inventoryPrice:
                inventory_total += inventoryPrice

            if register.registerDiscount:
                discount_total += int(register.registerDiscount)

            if register.registerPayed:
                payed_total += int(register.registerPayed)

            if register.registerMustpay:
                remaining_total += int(register.registerMustpay)

            table.append({
                "fullname": f"{student.studentName} {student.studentFamily}",
                "nationalID": student.studentMelli,
                "level": level.levelTitle,
                "classname": classes.classessTitle,
                "date": payed.payedDate,
                "fee": register.registerShahrieh,
                "inventoryPrice": inventoryPrice,
                "discount": register.registerDiscount,
                "payed": register.registerPayed,
                "remainingPay": register.registerMustpay
            })
        data={
            "table": table,
            "payed_total": payed_total,
            "fee_total": fee_total,
            "discount_total": discount_total,
            "remaining_total": remaining_total,
            "inventory_total": inventory_total
        }
        return data

    def get_report_details(self, courseID):
        payed_list = Payed.objects.filter(payed_courseID= courseID)
        cash = 0
        deposit = 0
        card = 0
        cheque = 0

        for payed in payed_list:
            match payed.payedMethod:
                case 1:
                    cash += int(payed.payedPayprice)
                case 2:
                    deposit += int(payed.payedPayprice)
                case 3:
                    card += int(payed.payedPayprice)
                case 5:
                    cheque += int(payed.p)
                case _:
                    continue
        values={
            "cash": cash,
            "deposit": deposit,
            "card": card,
            "cheque": cheque
        }
        return values

    def get_report_levels_detailed(self, courseID):
        unique_payed_list = Payed.objects.filter(payed_courseID= courseID).distinct()
        table = list()
        for payed in unique_payed_list:
            level = payed.payed_levelID

            registered_count = Payed.objects.filter(
                payed_courseID= courseID,
                payed_levelID=payed.payed_levelID
            ).values("payed_studentID").count()
            
            payed_total = Payed.objects.filter(
                payed_courseID= courseID,
                payed_levelID= payed.payed_levelID
            )
            sum_total = 0
            for payed in payed_total:
                sum_total += int(payed.payedPayprice)

            inventory_amount = 0
            inventory_price_total = 0
            register = payed.payed_registerID

            if (temp:=register.registerInventorysprice):
                inventory_amount += 1
                inventory_price_total += temp
            if (temp:=register.registerInventorys2price):
                inventory_amount += 1
                inventory_price_total += temp
            if (temp:=register.registerInventorys3price):
                inventory_amount += 1
                inventory_price_total += temp

            table.append({
                "levelTitle": level.levelTitle,
                "registerCount": registered_count,
                "sum_total": sum_total,
                "fee": register.registerShahrieh,
                "inventory_amount": inventory_amount,
                "inventory_price_total": inventory_price_total,
                "discount": register.registerDiscount,
                "remaining": sum_total - int(register.registerShahrieh) - int(inventory_price_total),
            })
        return table

    def get_report_levels(self, courseID) -> list:
        unique_payed_list = Payed.objects.filter(payed_courseID= courseID).distinct()
        table = list()
        for payed in unique_payed_list:
            level = payed.payed_levelID
            table.append({
                "levelID": level.levelID,
                "levelTitle": level.levelTitle,
            })

        data = {
            "table": table,
            "courseID": courseID
        }
        return data
    
    def get_report_level_table(self, courseID, levelID):
        payed_list = Payed.objects.filter(payed_courseID= courseID, payed_levelID= levelID)
        data= list()
        for payed in payed_list:
            student = payed.payed_studentID
            data.append({
                "fullname": f"{student.studentName} {student.studentFamily}",
                "nationalID": student.studentMelli,
                "date": payed.payedDate
            })
        return data

    def get_level(self, levelID):
        try:
            level = Level.objects.get(levelID = levelID)
            data = {
                "title": level.levelTitle,
                "number": level.levelNumber,
                "quiz1": level.levelQuiz1,
                "quiz2": level.levelQuiz2,
                "quiz3": level.levelQuiz3,
                "quiz4": level.levelQuiz4,
                "quiz5": level.levelQuiz5,
                "quiz6": level.levelQuiz6,
                "quiz7": level.levelQuiz7,
                "final": level.levelFinal,
            }
            return data
        except Level.DoesNotExist:
            return 404

    def get_student(self):
        student_list= Student.objects.all()
        table = list()
        for st in student_list:
            table.append({
                "studentID": st.studentID,
                "fullname": f"{st.studentName} {st.studentFamily}"
            })
        return table
    
    def get_classes(self):
        classes_list = Classess.objects.all()
        table = list()
        for cl in classes_list:
            table.append({
                "classID": cl.classessID,
                "name": cl.classessTitle
            })
        return table

    def get_inventory(self):
        inventory_list = Inventory.objects.all()
        table = list()
        for inv in inventory_list:
            table.append({
                "ID": inv.inventoryID,
                "title": inv.inventoryTitle
            })
        return table

    def get_register_table(self, registerID):
        try:
            register = Register.objects.get(registerID= registerID)
            level = register.register_levelID
            course = register.register_courseID
            table = {
                "quarter": course.courseCaption,
                "level": level.levelTitle,
                "date": register.registerCreateTime,
                "fee": register.registerShahrieh,
                "discount": register.registerDiscount,
                "payed": register.registerPayed,
                "remaining": int(register.registerShahrieh) - int(register.registerPayed)
            }
            return table
        except Register.DoesNotExist:
            return 404

    def update_register_class(self, studentID):
        try:
            updated_count= Register.objects.filter(register_studentID= studentID).update(register_classessID= None)
            if updated_count == 0:
                raise ValueError
        except(...):
            return 404
    
    def update_student(self, studentID, data):
        try:
            updated_count = Student.objects.filter(studentID= studentID).update(
                studentName = data["firstname"],
                studentFamily = data["lastname"],
                studentMelli = data["nationalID"],
                studentPedar = data["fathername"],
                studentPedarmobile = data["fatherphone"],
                studentMadarmobile = data["motherphone"],
                studentTell = data["phone"],
                studentShenasnameh = data["shenasnamehID"],
                studentSex = data["gender"],
                studentMadrak = data["certificate"],
                studentSodoor = data["sodoor"],
                studenttavalod = data["birthplace"],
                studentAddress = data["address"],
                studentNaghs = 1 if data["incomplete"] else 0
            )
            if updated_count < 0:
                raise ValueError
        except (Student.DoesNotExist, ValueError):
            return 404

    def update_teacher(self, teacherID, data):
        try:
            updated_count = Teacher.objects.filter(teacherID= teacherID).update(
                teacherName = data["firstname"],
                teacherFamily = data["lastname"],
                teacherMelli = data["nationalID"],
                teacherPedar = data["fathername"],
                teacherTell = data["phone"],
                teacherShenasnameh = data["shenasnamehID"],
                teacherSex = data["gender"],
                teacherMadrak = data["certificate"],
                teacherSodoor = data["sodoor"],
                teacherTavalod = data["birthplace"],
                teacherAddress = data["address"],
                teacherNaghs = 1 if data["incomplete"] else 0
            )
            if updated_count == 0:
                raise ValueError
        except(Teacher.DoesNotExist, ValueError):
            return 404

    def update_level(self, levelID, levelTitle, levelNumber, quiz_list):
        try:
            updated_count = Level.objects.filter(levelID= levelID).update(
                levelTitle = levelTitle,
                levelNumber = levelNumber,
                levelQuiz1 = quiz_list[0],
                levelQuiz2 = quiz_list[1],
                levelQuiz3 = quiz_list[2],
                levelQuiz4 = quiz_list[3],
                levelQuiz5 = quiz_list[4],
                levelQuiz6 = quiz_list[5],
                levelQuiz7 = quiz_list[6],
                levelFinal = quiz_list[7],
            )
            if updated_count == 0:
                raise ValueError
        except (Level.DoesNotExist, ValueError, IntegrityError):
            return 404

    def update_tuition(self, tuitionID, levelID, courseID, price):
        try:
            level = Level.objects.get(levelID= levelID)
            course = Course.objects.get(courseID= courseID)
            updated_count = Tuition.objects.filter(tuitionID= tuitionID).update(
                tuition_courseID= course,
                tuition_levelID = level,
                tuitionPrice = price
            )
            if updated_count == 0:
                raise ValueError

        except (ValueError, ObjectDoesNotExist):
            return 404

    def update_inventory(self, courseID, levelID, inventoryPrice, inventoryAmount, inventoryTitle, inventoryID):
        try:
            level = Level.objects.get(levelID= levelID)
            course = Course.objects.get(courseID= courseID)
            Inventory.objects.filter(inventoryID= inventoryID).update(
                inventory_courseID= course,
                inventory_levelID= level,
                inventoryTitle = inventoryTitle,
                inventoryCount= inventoryAmount,
                inventoryPrice= inventoryPrice,
            )
        except IntegrityError, ObjectDoesNotExist:
            return 404

    def update_register(self, data, registerID):
        try:
            student = Student.objects.get(studentID= data["studentID"])
            course = Course.objects.get(courseID= data["quarterID"])
            level = Level.objects.get(levelID= data["levelID"])
            classID = Classess.objects.get(classessID= data["classID"])
            inventory1ID = Inventory.objects.get(inventoryID= data["inventory1ID"])
            inventory2ID = Inventory.objects.get(inventoryID= data["inventory2ID"])
            inventory3ID = Inventory.objects.get(inventoryID= data["inventory3ID"])

            Register.objects.filter(registerID= registerID).update(
                register_studentID= student,
                register_courseID= course,
                register_levelID= level,
                register_classessID = classID,
                registerShahrieh = data["fee"],
                registerPaymethod = data["paymethod"],
                registerPayed = data["payed"],
                registerMustpay = str(int(data["fee"]) - int(data["payed"])),
                registerInventorysID = inventory1ID,
                registerInventorys2ID = inventory2ID,
                registerInventorys3ID = inventory3ID,
                registerInventorysprice = inventory1ID.inventoryPrice,
                registerInventorys2price = inventory2ID.inventoryPrice,
                registerInventorys3price = inventory3ID.inventoryPrice,
            )
        except (IntegrityError, ObjectDoesNotExist):
            return 404

    def update_class(self, data, classID):
        try:
            level = Level.objects.get(levelID= data["levelID"])
            course = Course.objects.get(courseID= data["courseID"])
            Classess.objects.filter(classessID= classID).update(
                classess_courseID = course,
                classess_levelID = level,
                classessTitle = data["title"],
                classessSex = data["gender"],
                classessStartDate = data["startdate"],
                classessType = data["type"],
                classessEndDate = data["enddate"],
            )
        except (IntegrityError, ObjectDoesNotExist):
            return 404

    def delete_register(self, register_id):
        try:
            Register.objects.get(registerID= register_id).delete()
        except ObjectDoesNotExist:
            return 404

    def delete_calender(self, calenderID):
        try:
            Calender.objects.get(calenderID= calenderID).delete()
        except ObjectDoesNotExist:
            return 404

    def delete_student(self, studentID):
        try:
            Student.objects.get(studentID= studentID).delete()
        except ObjectDoesNotExist:
            return 404
        
    def delete_teacher(self, teacherID):
        try:
            Teacher.objects.get(teacherID= teacherID).delete()
        except ObjectDoesNotExist:
            return 404

    def delete_score(self, scoreID):
        try:
            Score.objects.get(scoreID= scoreID).delete()
        except ObjectDoesNotExist:
            return 404
    

    def set_payment(self, student_id, payAmount_str: str, payMethod_str: str):

        try:
            student = Student.objects.get(studentID = student_id)
        except Student.DoesNotExist:
            return 404
        try:
            payMethod = int(payMethod_str)
            if payMethod <0:
                raise ValueError
        except (ValueError, TypeError):
            return 404
        
        try:
            register = Register.objects.filter(register_studentID= student_id).order_by("registerCreateTime").first()
        except Register.DoesNotExist:
            return 404
        

        Register.objects.create(
            register_studentID = student,
            register_courseID = register.register_courseID,
            register_levelID = register.register_levelID,
            register_classessID = register.register_classessID,
            registerPayed = payAmount_str,
            registerPaymethod = payMethod,
        )
        return 200
    
    def set_student(self, student_details: list):
        try:
            Student.objects.create(
                studentName= student_details[0],
                studentFamily= student_details[1],
                studentMelli= student_details[2],
                studentPedar= student_details[3],
                studentPedarmobile = student_details[4],
                studentMadarmobile= student_details[5],
                studentTell= student_details[6],
                studentShenasnameh= student_details[7],
                studentSex= student_details[8],
                studentMadrak= student_details[9],
                studentSodoor= student_details[12],
                studenttavalod= student_details[13],
                studentAddress= student_details[14],
                studentNaghs= 1 if student_details[15] else 0
            )
        except IntegrityError:
            return 404
        
    def set_teacher(self, teacher_details: list):
        try:
            Teacher.objects.create(
                teacherName= teacher_details[0],
                teacherFamily= teacher_details[1],
                teacherMelli= teacher_details[2],
                teacherPedar= teacher_details[3],
                teacherTell= teacher_details[4],
                teacherShenasnameh= teacher_details[5],
                teacherSex= teacher_details[6],
                teacherMadrak= teacher_details[7],
                teacherSodoor= teacher_details[8],
                teacherTavalod= teacher_details[9],
                teacherAddress= teacher_details[10],
                teacherNaghs= 1 if teacher_details[11] else 0
            )
        except IntegrityError:
            return 404
        
    def set_inventory(self, courseID, levelID, inventoryPrice, inventoryAmount, inventoryTitle):
        try:
            level = Level.objects.get(levelID= levelID)
            course = Course.objects.get(courseID= courseID)
            Inventory.objects.create(
                inventory_courseID= course,
                inventory_levelID= level,
                inventoryTitle = inventoryTitle,
                inventoryCount= inventoryAmount,
                inventoryPrice= inventoryPrice,
            )
        except IntegrityError, ObjectDoesNotExist:
            return 404

    def set_course(self, courseCaption):
        try:
            Course.objects.create(
                courseCaption= courseCaption
            )
        except IntegrityError:
            return 404

    def set_level(self, levelTitle, levelNumber, quiz_list: list):
        try:
            Level.objects.create(
                levelTitle = levelTitle,
                levelNumber = levelNumber,
                levelQuiz1 = quiz_list[0],
                levelQuiz2 = quiz_list[1],
                levelQuiz3 = quiz_list[2],
                levelQuiz4 = quiz_list[3],
                levelQuiz5 = quiz_list[4],
                levelQuiz6 = quiz_list[5],
                levelQuiz7 = quiz_list[6],
                levelFinal = quiz_list[7],
            )
        except IntegrityError:
            return 404

    def set_tuition(self, courseID, levelID, price):
        try:
            level = Level.objects.get(levelID= levelID)
            course = Course.objects.get(courseID= courseID)
            Tuition.objects.create(
                tuition_courseID = course,
                tuition_levelID = level,
                tuitionPrice = price
            )
        except IntegrityError, ObjectDoesNotExist:
            return 404

    def set_user(self, data):
        try:
            User.objects.create(
                user_name = data["username"],
                user_email = data["email"],
                user_password = data["password"],
                user_access = 1,
                user_perm = 1,
            )
        except IntegrityError:
            return 404

    def set_register(self, data):
        try:
            student = Student.objects.get(studentID= data["studentID"])
            course = Course.objects.get(courseID= data["quarterID"])
            level = Level.objects.get(levelID= data["levelID"])
            classID = Classess.objects.get(classessID= data["classID"])
            inventory1ID = Inventory.objects.get(inventoryID= data["inventory1ID"])
            inventory2ID = Inventory.objects.get(inventoryID= data["inventory2ID"])
            inventory3ID = Inventory.objects.get(inventoryID= data["inventory3ID"])

            Register.objects.create(
                register_studentID= student,
                register_courseID= course,
                register_levelID= level,
                register_classessID = classID if classID else None,
                registerShahrieh = data["fee"],
                registerPaymethod = data["paymethod"],
                registerPayed = data["payed"],
                registerMustpay = int(data["fee"]) - int(data["payed"]),
                registerInventorysID = inventory1ID,
                registerInventorys2ID = inventory2ID,
                registerInventorys3ID = inventory3ID,
                registerInventorysprice = inventory1ID.inventoryPrice,
                registerInventorys2price = inventory2ID.inventoryPrice,
                registerInventorys3price = inventory3ID.inventoryPrice,
            )
        except (IntegrityError, ObjectDoesNotExist):
            return 404

    def set_class(self, data):
        try:
            level = Level.objects.get(levelID= data["levelID"])
            course = Course.objects.get(courseID= data["courseID"])
            Classess.objects.create(
                classess_courseID = course,
                classess_levelID = level,
                classessTitle = data["title"],
                classessSex = data["gender"],
                classessStartDate = data["startdate"],
                classessType = data["type"],
                classessEndDate = data["enddate"],
            )
        except (IntegrityError, ValueError):
            return 404

    def set_calender(self, data):
        try:
            level = Level.objects.get(levelID= data["levelID"])
            course = Course.objects.get(courseID= data["courseID"])
            classID = Classess.objects.get(classessID= data["classID"])
            Calender.objects.create(
                calender_courseID= course,
                calender_classessID = classID,
                calender_levelID = level,
                calender_startDate = data["startdate"],
                calender_endDate = data["enddate"],
                calender_day1 = data["shanbe"],
                calender_day2 = data["yekshanbe"],
                calender_day3 = data["doshanbe"],
                calender_day4 = data["seshanbe"],
                calender_day5 = data["chaharshanbe"],
                calender_day6 = data["panjshanbe"],
                calender_day7 = data["jome"],
            )
        except (IntegrityError, ObjectDoesNotExist):
            return 404

    def set_score(self, data):
        # try:
        level = Level.objects.get(levelID = data["levelID"])
        student = Student.objects.get(studentID = data["studentID"])
        course = Course.objects.get(courseID= data["courseID"])
        Score.objects.create(
            score_studentID = student,
            score_courseID= course,
            score_levelID= level,
            scoreCardnumber= data["cardnumber"],
            scoreRoom= data["room"],
            scoreHour= data["hour"],
            scoreDays= data["days"],
            scoreProceed= int(data["proceed"]),
            scoreOral= data["oral"],
            scoreFinal= data["final"],
            scoreTotal= data["total"]
            )
        # except (IntegrityError, ObjectDoesNotExist):
        #     return 404

    def copy_inventory(self, old_courseID, new_courseID, raised_price):
        old_inventory_list = Inventory.objects.filter(inventory_courseID= old_courseID)
        newCourse = Course.objects.get(courseID= new_courseID)
        for inventory in old_inventory_list:
            new_price = int(inventory.inventoryPrice) + (int(inventory.inventoryPrice) * int(raised_price))

            Inventory.objects.create(
                inventoryTitle= inventory.inventoryTitle,
                inventoryCount = inventory.inventoryCount,
                inventoryPrice = new_price,
                inventory_levelID = inventory.inventory_levelID,
                inventory_courseID = newCourse
            )

