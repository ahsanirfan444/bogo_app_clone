import django
django.setup()
import csv
import datetime
from hubur_apis import models



import re

# Define a function to remove special characters
def remove_special_chars(text):
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

# Example usage
business_list = models.Business.objects.all()
for business in business_list:
    business.name = remove_special_chars(business.name)
    business.address = remove_special_chars(business.address)
    business.save()


exit()

# all_day_db_list = list(models.Day.objects.all().values_list('name',flat=True))
# all_buss = models.Business.objects.all()

# for i in all_buss:
#     all_sch = len(models.BusinessSchedule.objects.filter(i_business=i))
#     if all_sch != 7:
#         founded_days = []
#         sch = models.BusinessSchedule.objects.filter(i_business=i)
#         for days in sch:
#             founded_days.append(days.i_day.name)


#         remaining_days = set(all_day_db_list) - set(founded_days)
#         print(remaining_days)

#         for day in list(remaining_days):
#             schedule_dicts = dict()
#             schedule_dicts['i_business'] = i
#             day_insstance = models.Day.objects.get(name=day)
#             schedule_dicts['i_day'] = day_insstance
#             models.BusinessSchedule.objects.create(**schedule_dicts)

    



resturant_list = ['bakery','bar','cafe','casino','restaurant']
service_list = ['beauty_salon','car_rental','car_repair','car_wash','electrician','laundry','painter','plumber']
product_list = ['bicycle_store','book_store','cemetery','clothing_store','convenience_store','electronics_store','furniture_store','florist','hardware_store',
                'home_goods_store','jewelry_store','pet_store','shoe_store','shopping_mall','store','supermarket']
health_care_list = ['dentist', 'department_store', 'doctor', 'drugstore','hair_care','hospital','pharmacy','spa','veterinary_care']

for resturant in resturant_list:
    resturant = resturant.strip().replace(" ","_").lower()
    instance = models.Category.objects.get_or_create(name="Resturant")[0]
    models.SubCategories.objects.update_or_create(name=resturant, i_category=instance)

for service in service_list:
    service = service.strip().replace(" ","_").lower()
    instance = models.Category.objects.get_or_create(name="Services")[0]
    models.SubCategories.objects.update_or_create(name=service, i_category=instance)


for product in product_list:
    product = product.strip().replace(" ","_").lower()
    instance = models.Category.objects.get_or_create(name="Products")[0]
    models.SubCategories.objects.update_or_create(name=product, i_category=instance)

for health_care in health_care_list:
    health_care = health_care.strip().replace(" ","_").lower()
    instance = models.Category.objects.get_or_create(name="Health Care")[0]
    models.SubCategories.objects.update_or_create(name=health_care, i_category=instance)



sub_categories_db_list = list(models.SubCategories.objects.filter(is_active=True).values_list('name',flat=True))
all_day_db_list = list(models.Day.objects.all().values_list('name',flat=True))

with open('data.csv',  encoding='ISO-8859-1') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for idx,col in enumerate(csv_reader):
        schedules_list = []
        data_dict = dict()
        if idx == 0:
            pass
        else:
            if len(col[14]) != 0:
                schedule_data = col[14]
                if 'â' in schedule_data:
                    schedule_data = schedule_data.replace("â","-")
                schedule_data = schedule_data.replace("[","").replace("]","").replace("'","")

                




                for schedule_str in schedule_data.split(", "):
                    
                    # print(schedule_str,"..............")

                    schedules_dict = dict()
                    try:
                        day, time_range = schedule_str.split(": ")
                    except:
                        continue

                    
                    
                    if time_range == 'Open 24 hours':
                        start_time = datetime.datetime.strptime("12:00 AM", "%I:%M %p").time()
                        end_time = datetime.datetime.strptime("11:59 PM".strip(), "%I:%M %p").time()
                    elif time_range == 'Closed':
                        start_time = datetime.datetime.strptime("12:00 AM", "%I:%M %p").time()
                        end_time = datetime.datetime.strptime("11:59 PM".strip(), "%I:%M %p").time()
                        schedules_dict['is_active'] = False
                    else:
                        start_time_str, end_time_str = time_range.strip("[]").split("-")
                        try:
                            start_time = datetime.datetime.strptime(start_time_str, "%I:%M%p").time()
                        except ValueError:
                            start_time_str = start_time_str + 'AM'
                            start_time = datetime.datetime.strptime(start_time_str, "%I:%M%p").time()        
                        try:
                            end_time = datetime.datetime.strptime(end_time_str.strip(), "%I:%M%p").time()
                        except ValueError:
                            if end_time_str.find('AM') != -1:
                                continue
                            elif end_time_str.find('PM') != -1:
                                continue

                            else:
                                end_time_str = end_time_str + 'AM'
                                end_time = datetime.datetime.strptime(end_time_str.strip(), "%I:%M%p").time()
                
                    schedules_dict['start_time'] = start_time
                    schedules_dict['end_time'] = end_time
                    schedules_dict['i_day'] = day
                    schedules_list.append(schedules_dict)

                    # print(schedules_list,"........................................")

                



            
            if len(col[0]) != 0:
                name = col[0].strip()
                data_dict['name'] = name
            else:
                continue

            if len(col[1]) != 0:
                address = col[1].strip()
                data_dict['address'] = address
            else:
                continue

            data_dict['is_claimed'] = 1

            if len(col[10]) != 0:
                lat = col[10]
                data_dict['lat'] = lat
            else:
                continue

            if len(col[11]) != 0:
                long = col[11]
                data_dict['long'] = long
            else:
                continue
            if len(col[12]) != 0:
                website = col[12]
                data_dict['website'] = website

            if len(col[6]) != 0:
                place_id = col[6]
                data_dict['place_id'] = place_id
            else:
                continue
            
            if len(col[4]) !=0:
                contact = col[4].replace(" ","")
                country_code_list = ['+971']
                for code in country_code_list:
                    if contact.find(code) == 0:
                        contact = contact.replace(code,"")
                        country_code = code
                        break
                
                data_dict['contact'] = contact
                data_dict['country_code'] = country_code
            else:
                data_dict['contact'] = ""
                data_dict['country_code'] = ""


            
            if len(col[3]) !=0:
                sub_categories = (col[3]).strip().lower().split(",")
                for sub_category in sub_categories:
                    sub_category = sub_category.strip().replace(" ","_")

                    for sub in sub_categories_db_list:
                        sub_list = []
                        if sub_category.find(sub) != -1:
                            sub_obj = models.SubCategories.objects.get(name=sub)
                            sub_list.append(sub_obj)
                            cat = models.Category.objects.get(id=sub_obj.i_category_id)
                            data_dict['i_category'] = cat
                            data_dict['i_subcategory'] = sub_list
                            break

                        else:
                            continue

            business_image = col[15]

            business_image = business_image.split("/media/")[1]

            data_dict['logo_pic'] = business_image
            
            if 'i_subcategory' in data_dict:
                sub_list = data_dict['i_subcategory']
                del data_dict['i_subcategory']
                instance = models.Business.objects.update_or_create(**data_dict)[0]
                instance.i_subcategory.set(sub_list)

                
                business_catalog = col[16]
                if business_catalog:
                    business_catalog = business_catalog.replace("[","").replace("]","").replace("'","")
                    for cat_image in business_catalog.split(", "):
                        cat_image = cat_image.split("/media/")[1]

                        models.Images.objects.create(type=1,i_business_id=instance.id, image=cat_image,i_user_id=2)

                founded_days = []


                for schedule_dict in schedules_list:
                    schedule_dict['i_business'] = instance

                    if str(schedule_dict['i_day']) in all_day_db_list:
                        day_insstance = models.Day.objects.get(name=schedule_dict['i_day'])
                        schedule_dict['i_day'] = day_insstance
                        exist_data = models.BusinessSchedule.objects.filter(i_business=instance,i_day=schedule_dict['i_day']).exists()
                        if not exist_data:
                            founded_days.append(str(schedule_dict['i_day']))
                    
                    
                remaining_days = set(all_day_db_list) - set(founded_days)



                for day in list(remaining_days):
                    schedule_dicts = dict()
                    schedule_dicts['i_business'] = instance
                    day_insstance = models.Day.objects.get(name=day)
                    schedule_dicts['i_day'] = day_insstance
                    exist_data = models.BusinessSchedule.objects.filter(i_business=instance,i_day=day_insstance).exists()
                    if not exist_data:
                        models.BusinessSchedule.objects.create(**schedule_dicts)
                   





                
                        
                    
                    
                
                
            
