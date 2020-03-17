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
orientation_map = []
vertex_map_x = []
vertex_map_y = []

image_path = "./images/right_hand_"
image_index = 1
image_format = ".jpg"

#Number of input images
image_size = 3



def orienation_cal(x,y):
    #   Right +x; Downward +y
    #   Find inclination angle from +x axis (clockwise)
    angle_degree = 0.0

    if(y < 0)and(x > 0):
        y = y * -1
        angle_degree = 360 - math.degrees(math.atan(y/x))
        return angle_degree
   
    if(y > 0)and(x > 0):
        angle_degree = math.degrees(math.atan(y/x))
        return angle_degree

    if(y > 0)and(x < 0):
        x = x * -1
        angle_degree = 180 - math.degrees(math.atan(y/x))
        return angle_degree

    if(y < 0)and(x < 0):
        x = x * -1
        y = y * -1
        angle_degree = 180 + math.degrees(math.atan(y/x))
        return angle_degree

    if(y == 0)and(x > 0):
        return 0
    if(y == 0)and(x < 0):
        return 180
    if(x == 0)and(y > 0):
        return 90
    if(x == 0)and(y < 0):
        return 270

    


def acp_info(event,x,y,flag,param):
    global raw_image,marker_color
    global vertex_num,vertex_x,vertex_y,distance_map,orientation_map,vertex_map_x,vertex_map_y
    global image_path,image_index,image_format
    #When Left is clicked in the mouse
    if event == cv2.EVENT_LBUTTONDOWN:  
        print("Mouse Picker Coorindates: x={} y={}".format(x,y))
        cv2.circle(raw_image,(x,y),3,marker_color,-1)
        i = 0
        distance = 0
        orientation = 0
        while(i<vertex_num):
            distance = math.sqrt((vertex_x[i]-x)**2+(vertex_y[i]-y)**2)
            diff_y = y-vertex_y[i]
            diff_x = x-vertex_x[i]
            orientation = orienation_cal(diff_x,diff_y)         
            print("Mapping Info of vertex #{} --> Mag = {}  Orientation = {}".format(i,distance,orientation))
            distance_map.append(distance)
            orientation_map.append(orientation)
            vertex_map_x.append(vertex_x[i])
            vertex_map_y.append(vertex_y[i])
            cv2.line(raw_image,(vertex_x[i],vertex_y[i]),(x,y),map_color,2)
            img_save_path = "./output_image/"
            img_save_header = "right_hand_map_"
            save_description = img_save_path + img_save_header +str(image_index) + image_format
            cv2.imwrite(save_description,raw_image)
            i+=1
        with open('./output_csv/map_magnitude.csv','a',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([distance_map[0],distance_map[1],distance_map[2],distance_map[3],distance_map[4] \
                            ,distance_map[5],distance_map[6],distance_map[7],distance_map[8],distance_map[9]\
                            ,distance_map[10]])

        with open('./output_csv/map_orientation.csv','a',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([orientation_map[0],orientation_map[1],orientation_map[2],orientation_map[3],orientation_map[4] \
                            ,orientation_map[5],orientation_map[6],orientation_map[7],orientation_map[8],orientation_map[9]\
                            ,orientation_map[10]])

        with open('./output_csv/map_vertex_x.csv','a',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([vertex_map_x[0],vertex_map_x[1],vertex_map_x[2],vertex_map_x[3],vertex_map_x[4] \
                            ,vertex_map_x[5],vertex_map_x[6],vertex_map_x[7],vertex_map_x[8],vertex_map_x[9]\
                            ,vertex_map_x[10]])

        with open('./output_csv/map_vertex_y.csv','a',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([vertex_map_y[0],vertex_map_y[1],vertex_map_y[2],vertex_map_y[3],vertex_map_y[4] \
                            ,vertex_map_y[5],vertex_map_y[6],vertex_map_y[7],vertex_map_y[8],vertex_map_y[9]\
                            ,vertex_map_y[10]])
            
        distance_map = []
        orientation_map = []
        vertex_map_x = []
        vertex_map_y = []
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



