import json, time, datetime, cv2, os.path
from .crud import *
from .program_third import distance_list

# STANDCAM 과 STAND 사이의 거리: 126cm (캠이 살짝 위로 오도록)
MY_STORE_PORT = 2
area_var_1 = 0.7
area_var_2 = 0.8
area_var_3 = 0.9
dist_var_1 = 20
dist_var_2 = 13
dist_var_3 = 4

def funct(event):
    db = CRUD()
    prev_area_dict = {}
    vs = cv2.VideoCapture(MY_STORE_PORT)
    photo_path = ".\\prevention_theft\\static\\images\\photo\\"
    photo_link = "..\\..\\static\\images\\photo\\photo"
    photo_count = 0 

    if not vs.isOpened:
        print('[ERROR] 매장 카메라를 열 수 없습니다')
        exit(0)

    while(True):
        ret, frame = vs.read()
        frame = cv2.resize(frame, (380, 380))

        if frame is None:
            print("[ERROR] 매장 카메라의 프레임이 없습니다")
            vs.release()
            break

        now = time; hour = str(now.localtime().tm_hour); hour2 = str(int(hour) + 1)
        json_path = ".\\prevention_theft\\static\\json\\" + hour + "-" + hour2 + ".json"
        cv2.imshow("STORE CAMERA", frame)

        with open(json_path, "r") as f:
            json_data = json.load(f)

        json.dumps(json_data)
        json_last_idx = len(json_data) - 1

        for key in prev_area_dict:
            prev_area_dict[key][1] = False

        for i in range(len(json_data['{}'.format(json_last_idx)])):
            name = json_data['{}'.format(json_last_idx)][i]['name']
            width = json_data['{}'.format(json_last_idx)][i]['width']
            height = json_data['{}'.format(json_last_idx)][i]['height']
            area = width * height
            prev_area = 1

            for key in prev_area_dict:
                if name == key:
                    prev_area = prev_area_dict[key][0]
            
            if(area/prev_area <= area_var_1):
                disappeared_count = 3
                disappeared_time = datetime.datetime.now(); disappeared_time = (disappeared_time + datetime.timedelta(hours=9)).strftime("%Y-%m-%d T%H:%M:%S")
                while(True):
                    if os.path.isfile(photo_path + 'photo{}.jpg'.format(photo_count)):
                        photo_count += 1
                    else: break
                cv2.imwrite(photo_path + 'photo{}.jpg'.format(photo_count), frame)
                link = photo_link + str(photo_count) + ".jpg"
                photo_count += 1
                db.insertDB(schema='public', table="prevention_theft_item", colum='name, disappeared_count, disappeared_time, link', data="'{}', '{}', '{}', '{}'".format(name, disappeared_count, disappeared_time, link))
                print("[DB INSERT] name: '{}'   disappeared_count: {}\n\n".format(name, disappeared_count))

            elif(area/prev_area <= area_var_2):
                disappeared_count = 2
                disappeared_time = datetime.datetime.now()
                disappeared_time = (disappeared_time + datetime.timedelta(hours=9)).strftime("%Y-%m-%d T%H:%M:%S")
                while(True):
                    if os.path.isfile(photo_path + 'photo{}.jpg'.format(photo_count)):
                        photo_count += 1
                    else: break
                cv2.imwrite(photo_path + 'photo{}.jpg'.format(photo_count), frame)
                link = photo_link + str(photo_count) + ".jpg"
                photo_count += 1
                db.insertDB(schema='public', table="prevention_theft_item", colum='name, disappeared_count, disappeared_time, link', data="'{}', '{}', '{}', '{}'".format(name, disappeared_count, disappeared_time, link))
                print("[DB INSERT] name: '{}'   disappeared_count: {}\n\n".format(name, disappeared_count))

            elif(area/prev_area <= area_var_3):
                disappeared_count = 1
                disappeared_time = datetime.datetime.now()
                disappeared_time = (disappeared_time + datetime.timedelta(hours=9)).strftime("%Y-%m-%d T%H:%M:%S")
                while(True):
                    if os.path.isfile(photo_path + 'photo{}.jpg'.format(photo_count)):
                        photo_count += 1
                    else: break
                cv2.imwrite(photo_path + 'photo{}.jpg'.format(photo_count), frame)
                link = photo_link + str(photo_count) + ".jpg"
                photo_count += 1
                db.insertDB(schema='public', table="prevention_theft_item", colum='name, disappeared_count, disappeared_time, link', data="'{}', '{}', '{}', '{}'".format(name, disappeared_count, disappeared_time, link))
                print("[DB INSERT] name: '{}'   disappeared_count: {}\n\n".format(name, disappeared_count))
            
            else:
                pass
            
            prev_area_dict['{}'.format(name)] = [area, True]


        for key in prev_area_dict.copy():
            if prev_area_dict[key][1] == False:
                prev_distance = distance_list[-6]
                # print("[TEST] distance_list: ", distance_list)
                # print("[TEST] prev_distance: ", prev_distance)
                
                
                print("[NOTICE]", key, "가 사라진 원인(카메라가 가려짐 OR 사람이 가져감): ", end="")
                time.sleep(5)

                with open(json_path, "r") as f:
                    json_data = json.load(f)

                json.dumps(json_data)
                _json_last_idx = len(json_data) - 1

                for _i in range(len(json_data['{}'.format(_json_last_idx)])):
                    _name = json_data['{}'.format(_json_last_idx)][_i]['name']

                    if _name == key:
                        prev_area_dict[key][1] = True

                if prev_area_dict[key][1] == False:
                    print("사람이 가져감")
                    del prev_area_dict[key]
                    
                    curr_distnace = distance_list[-1]
                    # print("[TEST] distance_list: ", distance_list)
                    # print("[TEST] curr_distnace: ", curr_distnace)
                    

                    if (curr_distnace - prev_distance) > dist_var_1:
                        disappeared_count = 3

                    elif (curr_distnace - prev_distance) > dist_var_2:
                        disappeared_count = 2

                    elif (curr_distnace - prev_distance) > dist_var_3:
                        disappeared_count = 1

                    else:
                        print("[WARNING] 갯수 파악 실패")
                        disappeared_count = 999

                    disappeared_time = (datetime.datetime.now() + datetime.timedelta(hours=9)).strftime("%Y-%m-%d T%H:%M:%S")

                    while(True):
                        if os.path.isfile(photo_path + 'photo{}.jpg'.format(photo_count)):
                            photo_count += 1

                        else: break

                    cv2.imwrite(photo_path + 'photo{}.jpg'.format(photo_count), frame)
                    link = photo_link + str(photo_count) + ".jpg"
                    photo_count += 1
                    db.insertDB(schema='public', table="prevention_theft_item", colum='name, disappeared_count, disappeared_time, link', data="'{}', '{}', '{}', '{}'".format(name, disappeared_count, disappeared_time, link))
                    print("[DB INSERT] name: '{}'   disappeared_count: {}\n\n".format(key, disappeared_count))

                else: print("카메라가 가려짐")
                
        print("[ITEM DICTIONARY]", prev_area_dict)
        time.sleep(5.7)

        if event.is_set():
            return

    vs.release()
    cv2.destroyAllWindows()

        
        

