import os, os.path
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
from imageai.Detection import ObjectDetection



IMAGES_FOLDER = 'Images/'

def sizeOfImagesFolder():
    return len(os.listdir(IMAGES_FOLDER))

def saveData(image,target):
    size = sizeOfImagesFolder()

    with open("Images/{num}_{target}.png".format(target=target,num=size), "wb") as file:
        file.write(image)

    return

#Change the name of the images in Data/* to Images{x}.format(x++)
def changeFileNames():
    pass

class CaptchaSolver:
    """
    A image classifer neural network
    """
    def __init__(self):

        #ResNet
        #https://keras.io/api/applications/
        #self.model = ResNet50(weights='imagenet')

        #Need to train a model on top of this
        self.detector = ObjectDetection()
        self.detector.setModelTypeAsYOLOv3()
        self.detector.setModelPath("yolo.h5")
        self.detector.loadModel()


    # https://keras.io/api/applications/
    def resnet(self,image):
        """
        :param image: numpy array of an image with shape (224,224)
        :return: Returns top 5 predictions of image
        """
        x = np.expand_dims(image, axis=0)
        x = preprocess_input(x)

        preds = self.model.predict(x)
        #print('Predicted:', decode_predictions(preds, top=5)[0])

        return decode_predictions(preds, top=5)[0]


    #https://towardsdatascience.com/object-detection-with-10-lines-of-code-d6cb4d86f606
    #https://imageai.readthedocs.io/en/latest/
    #https://imageai.readthedocs.io/en/latest/detection/
    def ImageAI(self,image):
        #Can not detect crosswalks :(
        #Is it faster to have image be file path or as np array? Test maybe?
        #Might have to lower minimum_percentage_probability :\ or train my own NN

        try:
            returned_image, detections = self.detector.detectObjectsFromImage(input_image=image, input_type="array",
                                                                              output_type="array",
                                                                              minimum_percentage_probability=10)
        except:
            size = len(os.listdir("TestImages/"))
            detections = self.detector.detectObjectsFromImage(input_image=image,
                                                              output_image_path="TestImages/testimage{}.png".format(size),
                                                              minimum_percentage_probability=10)


        return detections

    def classify(self,image,target,size,rows):
        """
        :param image: image
        :param target: The target for the captcha solver
        :param height: Width and Height of captcha image, takes integer ie. 390 x 390, size = 390
        :param rows: Amount of rows in captcha, takes integer --> 3x3 Captcha, Size = 3
        :return: Returns the squares to press
        """


        height = size//rows

        print(height,size,rows)

        pred = self.ImageAI(image)

        boxes_to_click = set()

        for eachObject in pred:
            if eachObject["name"] == target:

                #Boxes can be outside of the picture
                X1 = eachObject["box_points"][0] // height + 1 \
                    if eachObject["box_points"][0] < size else eachObject["box_points"][0] // height
                Y1 = eachObject["box_points"][1] // height + 1 \
                    if eachObject["box_points"][1] < size else eachObject["box_points"][1] // height
                X2 = eachObject["box_points"][2] // height + 1 \
                    if eachObject["box_points"][2] < size else eachObject["box_points"][2] // height
                Y2 = eachObject["box_points"][3] // height + 1 \
                    if eachObject["box_points"][3] < size else eachObject["box_points"][3] // height

                print(eachObject["box_points"])
                print(X1,Y1,X2,Y2)

                boxes_to_click.add((Y1, X1))
                boxes_to_click.add((Y1, X2))
                boxes_to_click.add((Y2, X1))
                boxes_to_click.add((Y2, X2))


        print(boxes_to_click)
        return boxes_to_click

if __name__ == "__main__":
    test = CaptchaSolver()

    pic = 'Pictures/249_traffic lights.png'
    x = test.classify(pic,'traffic light',380,4)

    print(x)
    #from PIL import Image

    #img = Image.open('Pictures/21_image.png')
    #print(img)