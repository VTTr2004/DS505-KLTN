import cv2

class Draw:
    # export img and draw bounding box
    color = {
        1 : (255, 255, 0),
        2 : (255, 200, 0),
        3 : (255, 150, 0),
        4 : (255, 100, 0),
        5 : (255, 50, 0),
        6 : (255, 0, 0)
    }

    lb_dict = {
        0 : 'den do',
        1 : 'den xanh',
        2 : 'vach di bo',
        3 : 'nguoi di bo',
        4 : 'xe may',
        5 : 'Oto',
        6 : 'Xe cho hang nho',
        7 : 'Xe cho hang nho',
        8 : 'Xe khach'
    }

    def Convertxyxy(self, data):
        x_1 = data[0] - data[2] / 2
        y_1 = data[1] - data[3] / 2
        x_2 = data[0] + data[2] / 2
        y_2 = data[1] + data[3] / 2

        return list(map(int, [x_1, y_1, x_2, y_2]))
    
    def DrawFromModel(self, img, results):
        for r in results[0].boxes:
            x_1, y_1, x_2, y_2 = map(int, r.xyxy[0])
            cv2.rectangle(img, (x_1, y_1), (x_2, y_2), color = (0, 255, 0), thickness=2)

        return img   

    def DrawFromMap(self, img, char):
        # [cls_id, ft_color_1, ft_color_2, ft_color_3, X_cen, Y_cen, w, h, <speed>]
        cls_id = char[0]
        box = self.Convertxyxy(char[4:8])

        name = f'{Draw.lb_dict.get(cls_id, -1)}'

        cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color = Draw.color.get(cls_id, (0, 255, 0)), thickness=2)
        cv2.line(img, char[4:6], char[8:10], (255, 255, 255), 3)
        cv2.putText(img, name, (box[0], box[1] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return img