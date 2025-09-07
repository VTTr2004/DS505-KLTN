import cv2
import numpy as np
import os

import create_char
import read_map

def save_img(street_img, chars,c, folder):
    os.makedirs(os.path.join(folder, "0"), exist_ok=True)
    os.makedirs(os.path.join(folder, "1"), exist_ok=True)

    if chars.ndim == 2 and chars.shape[0] > 0:
        pos_chars = chars[chars[:, -1] == 1]
        neg_chars = chars[chars[:, -1] != 1]
        np.random.shuffle(pos_chars)
    else:
        pos_chars = []
        neg_chars = []
    i = 0
    # Vẽ Vật Thể vi phạm
    for char in pos_chars:
        temp = np.copy(street_img)
        x1 = int(char[0])
        y1 = int(char[1])
        x2 = int(x1 + char[2])
        y2 = int(y1 + char[3])
        temp[x1:x1+2, y1:y1+2] = 200
        temp[x2:x2+2, y2:y2+2] = 250
        filename = os.path.join(folder, "1", f"case{c}_{i}.png")
        cv2.imwrite(filename, temp.T)
        i += 1
    count_temp = 0
    # Vẽ Vật Thể không vi phạm
    for char in neg_chars:
        if count_temp >= 3:
            break
        temp = np.copy(street_img)
        x1 = int(char[0])
        y1 = int(char[1])
        x2 = int(x1 + char[2])
        y2 = int(y1 + char[3])
        temp[x1:x1+2, y1:y1+2] = 200
        temp[x2:x2+2, y2:y2+2] = 250
        filename = os.path.join(folder, "0", f"case{c}_{i}.png")
        cv2.imwrite(filename, temp.T)
        i += 1
        count_temp += 1
    return c+1

def type_street(loop, kind = 1):
    if kind==1:
        return (loop//60)%2 if loop%60<= 45 else 2

def run_char(chars, street_feature, points, ways, kind, num_char, max_loop, folder):
    chars = np.array(chars)
    gates = create_char.get_gate(ways)
    loop = 0
    c = 0
    while max_loop == -1 or loop <= max_loop:
        loop += 1
        chars = create_char.update_char(chars, street_feature, ways, type_street(loop, kind))
        if np.random.choice([True, False], p=[0.4, 0.6]):
            if len(chars) < num_char:
                chars = create_char(chars, gates, points, ways)
        # Vẽ frame trắng đen
        temp = np.copy(street_feature).astype(np.uint8)
        temp[temp > 0] = 50
        for char in chars:
            x1 = int(char[0])
            y1 = int(char[1])
            x2 = int(x1 + char[2])
            y2 = int(y1 + char[3])
            temp[x1:x1+2, y1:y1+2] = 100
            temp[x2:x2+2, y2:y2+2] = 150
        if loop % 10 == 0:
            c = save_img(temp, chars,c, f"{folder}/output")
    return chars

def handle(folder_path,size = 64, num_char = 30, max_loop=-1, kind = 1):
    img_path = f'{folder_path}/input/main.png'
    point_path = f'{folder_path}/input/main.txt'
    way_path = f'{folder_path}/input/way.txt'
    street_feature, points, ways = read_map.handle(img_path, point_path, way_path, size)
    chars = run_char(np.array([]), street_feature, points, ways, kind, num_char, max_loop, folder_path)
    return street_feature, points, ways, chars