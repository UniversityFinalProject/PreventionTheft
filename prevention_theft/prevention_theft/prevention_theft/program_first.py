import numpy as np
import cv2, json, time

MY_STAND_PORT = 1

def funct(event):
    now = time
    hour = str(now.localtime().tm_hour)
    hour2 = str(int(hour) + 1)
    file_path = ".\\prevention_theft\\static\\json\\" + hour + "-" + hour2 + ".json"
    data = {}
    frameCount = 0 
    min_confidence = 0.7
    width = 1080
    title_name = "STAND CAMERA"
    weights_path = ".\\yolo_data\\model\\custom-train-yolo_7000.weights"
    cfg_path = ".\\yolo_data\\cfg\\custom-train-yolo.cfg"
    names_path = ".\\yolo_data\\cfg\\classes.names"
    net = cv2.dnn.readNet(weights_path, cfg_path)
    classes = []

    with open(names_path, "r") as f:
        classes = [line.strip() for line in f.readlines()]

    color_lists = np.random.uniform(0, 255, size=(len(classes), 3))
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    def detectAndDisplay(image, file_path, data):
        h, w = image.shape[:2] #
        height = int(h * width / w)
        img = cv2.resize(image, (width, height))
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416),(0,0,0), swapRB=True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        confidences = []
        names = []
        boxes = [] 
        colors = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id] 

                if confidence > min_confidence:
                    center_x = int(detection[0] * width) 
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    names.append(classes[class_id])
                    colors.append(color_lists[class_id])

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, min_confidence, 0.6)
        font = cv2.FONT_HERSHEY_PLAIN
        data[frameCount] = []

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = '{} {:,.2%}'.format(names[i], confidences[i])
                color = colors[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y - 10), font, 1, color, 2)
                info = {"name" : names[i], "width" : w, "height" : h}
                data[frameCount].append(info)

        with open(file_path, 'w') as outfile:
            json.dump(data, outfile, indent=2)

        cv2.imshow(title_name, img)

        
        
    def file_path_change():
        now = time
        hour = str(now.localtime().tm_hour)
        hour2 = str(int(hour) + 1)
        file_path = ".\\prevention_theft\\static\\json\\" + hour + "-" + hour2 + ".json"
        return file_path

    vs = cv2.VideoCapture(MY_STAND_PORT)
    
    if not vs.isOpened:
        print("[ERROR] 진열대 카메라를 열 수 없습니다")
        exit(0)

    data = {}

    while True:
        ret, frame = vs.read()

        if frame is None:
            print('[ERROR] 진열대 카메라의 프레임이 없습니다')
            vs.release()
            break

        if hour != str(now.localtime().tm_hour): 
            hour = str(now.localtime().tm_hour)
            file_path = file_path_change()
            data = {}

        detectAndDisplay(frame, file_path, data)
        frameCount += 1
        time.sleep(5)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        if event.is_set():
            return

    vs.release()
    cv2.destroyAllWindows()