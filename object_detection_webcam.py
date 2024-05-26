import cv2
import numpy as np

net = cv2.dnn.readNet('yolov3.weights','yolov3.txt')
classes = []
with open('dataset.txt','r') as f:
    classes = f.read().splitlines()

# print(classes)

# img = cv2.imread('ofc1.jpg')
cap = cv2.VideoCapture(0)

while True:
    _, img = cap.read()
    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, 1/255, (416,416),(0,0,0),swapRB=True,crop=False)

    # for b in blob:
    #     for n, img_blob in enumerate(b):
    #         cv2.imshow(str(n),img_blob)

    net.setInput(blob)

    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_id = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_ids = np.argmax(scores)
            confidence = scores[class_ids]
            if confidence > 0.5:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)
                boxes.append([x,y,w,h])
                confidences.append((float(confidence)))
                class_id.append(class_ids)

		

    print(len(boxes))
    indexes = cv2.dnn.NMSBoxes(boxes,confidences,0.5,0.4)

    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0,255,size=(len(boxes),3))

    if len(indexes)>0:
        for i in indexes.flatten():
            x,y,w,h = boxes[i]
            label = str(classes[class_id[i]])
            confidence = str(round(confidences[i],2))
            color = colors[i]
            cv2.rectangle(img,(x,y),(x+w,y+h),color,2)
            cv2.putText(img, label + " " + confidence, (x,y+20),font, 1, (139,0,0),2)

            import pyttsx3
            engine = pyttsx3.init()

            engine.say(label)
            engine.say("is in front of you")
            engine.runAndWait()
	    
    # print(indexes.flatten())

    cv2.imshow('Image',img)
    key = cv2.waitKey(1)
    if key==27:
        break
cap.release()
cv2.waitKey(0)
