import cv2
import numpy as np
import math
import csv

raw_image,gray_image,thres_image = None,None,None

marker_color = (0,0,0)
contour_color = (102,204,0)
polyaprox_color = (0,0,255)
map_color = (255,0,0)

vertex_num = 0
vertex_x = []
vertex_y = []
distance_map = []

image_path = "./images/right_hand_"
image_index = 1
image_format = ".jpg"

#Number of input images
image_size = 3


def acp_info(event,x,y,flag,param):
    global raw_image,marker_color
    global vertex_num,vertex_x,vertex_y,distance_map
    global image_path,image_index,image_format
    #When Left is clicked in the mouse
    if event == cv2.EVENT_LBUTTONDOWN:  
        print("Mouse Picker Coorindates: x={} y={}".format(x,y))
        cv2.circle(raw_image,(x,y),3,marker_color,-1)
        i = 0
        distance = 0
        while(i<vertex_num):
            distance = int(math.sqrt((vertex_x[i]-x)**2+(vertex_y[i]-y)**2))
            print("Mapping Distance of vertex #{} = {}".format(i,distance))
            distance_map.append(distance)
            cv2.line(raw_image,(vertex_x[i],vertex_y[i]),(x,y),map_color,2)
            img_save_path = "./output_image/"
            img_save_header = "right_hand_map_"
            save_description = img_save_path + img_save_header +str(image_index) + image_format
            cv2.imwrite(save_description,raw_image)
            i+=1
        with open('./output_csv/map_single_acp_images.csv','a',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([distance_map[0],distance_map[1],distance_map[2],distance_map[3],distance_map[4] \
                            ,distance_map[5],distance_map[6],distance_map[7],distance_map[8],distance_map[9]\
                            ,distance_map[10]])
        distance_map = []

        cv2.imshow("Acp Picker",raw_image)


def main():
    global raw_image,gray_image,thres_image
    global total_target,target_x,target_y
    global image_path,image_index,image_format
    global vertex_num,vertex_x,vertex_y
    z = 0
    while(z<=image_size):

        vertex_num = 0
        vertex_x = []
        vertex_y = []

        image_desciption = image_path+str(image_index)+image_format
        raw_image = cv2.imread(image_desciption)

        gray_image = cv2.cvtColor(raw_image,cv2.COLOR_BGR2GRAY)
        res,thres_image = cv2.threshold(gray_image,220,255,cv2.THRESH_BINARY)
        cv2.imshow('Threshold',thres_image)
        image,contours,hierarchy = cv2.findContours(thres_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.drawContours(raw_image, contours,-1,(102,204,0),3)
        #Find vertices of contours
        for cnt in contours : 
            approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True) 
  
            # draws boundary of contours. 
            cv2.drawContours(raw_image, [approx], 0, (0,0,255), 3)  
  
            # Used to flatted the array containing 
            # the co-ordinates of the vertices. 
            n = approx.ravel()  
            i = 0
            counter = 0
            for j in n : 
                if(i % 2 == 0): 
                    x = n[i] 
                    y = n[i + 1] 
                    if((counter!=0)and(counter!=1)and(counter!=13)and(counter!=14)):
                        # String containing the co-ordinates. 
                        string = str(x) + " " + str(y)  
                        print("Vertices #{}: x={},y={}".format(vertex_num,x,y))
                        vertex_num +=1
                        vertex_x.append(x)
                        vertex_y.append(y)
                        if(i == 0): 
                            # text on topmost co-ordinate. 
                            cv2.putText(raw_image, "Arrow tip", (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))  
                        else: 
                            # text on remaining co-ordinates. 
                            cv2.putText(raw_image, string, (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))  
                    counter+=1
                i+=1

        #Mouse Pick system         
        cv2.namedWindow('Acp Picker')        
        cv2.imshow('Acp Picker',raw_image)                  
        cv2.setMouseCallback("Acp Picker",acp_info)


        cv2.waitKey(0)
        cv2.destroyAllWindows() 
        print("===============================================")
        z+=1
        image_index+=1 

if __name__ == '__main__':
    main()



