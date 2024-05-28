# from config import threshold as th

def find_AngleTrack(root,th):

    # find along and across angle
    angle_along = root.find('Dataset_Sources').find('Source_Information').find('Scene_Source').find('VIEWING_ANGLE_ALONG_TRACK').text
    angle_across = root.find('Dataset_Sources').find('Source_Information').find('Scene_Source').find('VIEWING_ANGLE_ACROSS_TRACK').text
    
    # ประเมินว่า ค่า absolute ของ มุม angle_along และ angle_across อยู่ในช่วงที่กำหนด หรือไม่
    if (abs(float(angle_along)) < th.Angle_limit) and (abs(float(angle_across)) < th.Angle_limit):
        return [float(angle_along), float(angle_across)], True
    else:
        return [float(angle_along), float(angle_across)], False
