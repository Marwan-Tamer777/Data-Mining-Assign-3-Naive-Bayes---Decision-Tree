def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

def normalise0to100(value,min,max):
    if(max-min == 0):
        return value
    normalisedValue = round( ((value-min)/(max-min)) *100 ,2)
    return normalisedValue

def calcDistance(point,centroid):
    distance = 0
    for key, value in point.items():
        if(key!="status_type" and key != "status_id"):
            distance += abs(int(value)-int(centroid[key]))
        elif(key == "status_type"):
            if(value!=centroid[key]):
                distance+=100
    return distance