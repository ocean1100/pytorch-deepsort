import cv2
import os


def camera_init(demo,store,channel,resolution):
        file = demo
        if demo == 'camera':
                if store == "racing":
                        ip='200.148.68.170'
                if store == "newera":
                        ip='186.225.97.198'
                print(store)
                part1="rtsp://admin:trop001818@"
                part2=':554/Streaming/channels/'
                part3= '/?transportmode=unicast'
                url ="{}{}{}{}0{}{}".format(part1,ip,part2,channel,resolution,part3)
                file = url
        else:
                assert os.path.isfile(demo), \
                'file {} does not exist'.format(demo)

        if demo == 0:
                self.say('Press [ESC] to quit video')
                file = 0
        camera = cv2.VideoCapture(file)
        if demo == 0: #camera window
                cv2.namedWindow('', 0)
                _, frame = camera.read()
                height, width, _ = frame.shape
                cv2.resizeWindow('', width, height)
        else:
                _, frame = camera.read()
                height, width, _ = frame.shape

        assert camera.isOpened(), \
        'Cannot capture source'
        return camera
