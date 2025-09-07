import numpy as np

def extract_3_channel(img, objs, factor):
    result = []
    for obj in objs:
        box = obj[1:]
        h_img, w_img = img.shape[:2]
        x_min = max(0, int(box[0] - box[2]))
        y_min = max(0, int(box[1] - box[3]))
        x_max = min(w_img, int(box[0] + box[2]))
        y_max = min(h_img, int(box[1]))
        c1 = np.mean(img[y_min:y_max, x_min:x_max, 0])/255*factor
        c2 = np.mean(img[y_min:y_max, x_min:x_max, 1])/255*factor
        c3 = np.mean(img[y_min:y_max, x_min:x_max, 2])/255*factor
        result.append([float(obj)*1000] + [c1, c2, c3] + list(map(float, obj[1:])))
    return np.array(result)