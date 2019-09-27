# how to run?
# you need these 3 files : yolov3-tiny.cfg, coco.names, yolov3-tiny.weights
# 경고 알림창이 뜨면서 현재 loop를 방해하지 않는 녀석이 필요하다

import cv2
import numpy as np
import time
import datetime
import pygame


class Embedded_yolo:
    def __init__(self):
        # Loading camera
        self._init_yolo()
#        self._init_serialCommunication()
        self._init_siren()

    def _init_yolo(self):
        self.cnt = 0
        self.net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
        self.classes = []
        with open("coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))
        self.cap = cv2.VideoCapture(0)  # 웹캠 번호가 0일수도, 1일수도 그 이상일 수도 있다.
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.starting_time = time.time()
        self.frame_id = 0

    def _init_siren(self):
        pygame.init()
        self.audio_volume = 0.2
        self.sound = pygame.mixer.Sound('siren.wav')
        self.sound.set_volume(self.audio_volume)
        self.timeSirenStart = datetime.datetime.now()
        self.timeSirenSecond = 0
        self.FlagSiren = 0

    def _init_serialCommunication(self):
        import serial
        # 포트 설정
        PORT = '/dev/ttyUSB0'
        # 연결
        self.ser = serial.serial_for_url(PORT, baudrate=115200, timeout=1)

    def transmit2cortex(self, data):
        self.ser.write(bytes(data, encoding='ascii'))  # 출력방식1

    def alertEmergency(self):
        if self.cnt > 5:
            #self.transmit2cortex_a('a')

            if self.FlagSiren == 0:
                self.sound.play()
                self.sound.set_volume(self.audio_volume)
                self.timeSirenStart = datetime.datetime.now()
                self.FlagSiren = 1
                import Server_notification
                # mcu로 모터조절용 메시지 전송
                self.transmit2cortex('a')

            from tkinter import messagebox
            messagebox.showwarning("긴급상황", "범죄가 발생하였습니다.")

            self.cnt = 0

    def Loop_main(self):
        while True:
            _, frame = self.cap.read()
            self.frame_id += 1
            height, width, channels = frame.shape

            # Detecting objects
            # 320*320 #416*416 #609*609 <=== 정확도 조절
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
            self.net.setInput(blob)
            outs = self.net.forward(self.output_layers)
            # Showing informations on the screen
            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        # Object detected
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)

                        # print(class_id, center_x , center_y)
                        w = int(detection[2] * width)  # width of object
                        h = int(detection[3] * height)
                        # Rectangle coordinates
                        x = int(center_x - w / 2)  # the starting X position of detected object
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))  # percentage
                        class_ids.append(class_id)  # the name of detected object
                        if class_id == 0:
                            self.cnt += 1
                            print(self.cnt)
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)  # NMS 알고리즘(한 물체를 두개의 물체로 인식하면 이거 조정하면 돼)

            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(self.classes[class_ids[i]])
                    confidence = confidences[i]
                    color = self.colors[class_ids[i]]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + 30), color, -1)
                    cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), self.font, 3, (255, 255, 255),
                                3)

            elapsed_time = time.time() - self.starting_time
            fps = self.frame_id / elapsed_time
            cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), self.font, 3, (0, 0, 0), 3)

            cv2.imshow("Image", frame)

            self.alertEmergency()

            if self.FlagSiren == 1:
                self.timeSirenSecond = int((datetime.datetime.now() - self.timeSirenStart).total_seconds())

            if self.timeSirenSecond > 5:
                self.sound.set_volume(0)
                self.FlagSiren = 0

            key = cv2.waitKey(1)
            if key == ord('q'):
                break


if __name__ == '__main__':
    emb = Embedded_yolo()
    emb.Loop_main()





