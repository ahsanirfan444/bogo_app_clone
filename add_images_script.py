import django
django.setup()
import csv
import datetime
from hubur_apis import models


with open('data.csv', encoding='ISO-8859-1') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for idx,col in enumerate(csv_reader):
        schedules_list = []
        data_dict = dict()
        if idx == 0:
            pass
        else:
            if len(col[0]) != 0:
                business_obj = models.Business.objects.filter(name=col[0],address=col[1])
                if business_obj:
                    business_obj = business_obj.first()
                    business_image = col[15]
                    if business_image:
                        business_image = business_image.split("/media/")[1]
                        business_obj.logo_pic = business_image
                        business_obj.save()
                        business_catalog = col[16]
                        if business_catalog:
                            business_catalog = business_catalog.replace("[","").replace("]","").replace("'","")
                            for cat_image in business_catalog.split(", "):
                                cat_image = cat_image.split("/media/")[1]

                                models.Images.objects.create(type=1,i_business_id=business_obj.id, image=cat_image,i_user_id=2)




# models.Business.objects.all().update(logo_pic='business_images/bag.png')