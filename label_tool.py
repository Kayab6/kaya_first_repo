import cv2
import os

# ===== SETTINGS =====
IMAGE_FOLDER = "data"
LABEL_FOLDER = "labels"

# YOUR UNIFIED CLASSES
CLASSES = [
    "TANK",
    "ARMOURED_VEHICLE",
    "SUPPORT_VEHICLE",
    "UNARMOURED_VEHICLE",
    "AIRCRAFT",
    "HELICOPTER",
    "WARSHIP",
    "LIGHT_ATTACK_BOAT"
]

#  COLORS for each class
COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (128, 0, 128),
    (0, 128, 255)
]

os.makedirs(LABEL_FOLDER, exist_ok=True)

images = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith((".jpg", ".png"))]
current_image_index = 0

drawing = False
x_start, y_start = -1, -1
boxes = []
current_class = 0

def draw_boxes(img, boxes):
    for cls, x1, y1, x2, y2 in boxes:
        color = COLORS[cls]
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, CLASSES[cls], (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return img

def draw_rectangle(event, x, y, flags, param):
    global x_start, y_start, drawing, boxes

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        x_start, y_start = x, y

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        img_copy = base_img.copy()
        img_copy = draw_boxes(img_copy, boxes)
        cv2.rectangle(img_copy, (x_start, y_start), (x, y), (255, 255, 255), 2)
        cv2.imshow("Image", img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        x_end, y_end = x, y
        boxes.append((current_class, x_start, y_start, x_end, y_end))

def save_labels(filename, boxes, img_shape):
    h, w, _ = img_shape
    label_path = os.path.join(LABEL_FOLDER, filename.replace(".jpg", ".txt").replace(".png", ".txt"))

    with open(label_path, "w") as f:
        for cls, x1, y1, x2, y2 in boxes:
            x_center = ((x1 + x2) / 2) / w
            y_center = ((y1 + y2) / 2) / h
            width = abs(x2 - x1) / w
            height = abs(y2 - y1) / h
            f.write(f"{cls} {x_center} {y_center} {width} {height}\n")

while current_image_index < len(images):
    img_path = os.path.join(IMAGE_FOLDER, images[current_image_index])
    base_img = cv2.imread(img_path)
    boxes = []

    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", draw_rectangle)

    while True:
        display = base_img.copy()
        display = draw_boxes(display, boxes)

        cv2.putText(display, f"Class: {CLASSES[current_class]}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, COLORS[current_class], 2)

        cv2.putText(display, "N: Next | C: Change | U: Undo | R: Reset | Q: Quit",
                    (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        cv2.imshow("Image", display)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('n'):
            save_labels(images[current_image_index], boxes, base_img.shape)
            current_image_index += 1
            break

        elif key == ord('c'):
            current_class = (current_class + 1) % len(CLASSES)

        elif key == ord('u'):
            if boxes:
                boxes.pop()

        elif key == ord('r'):
            boxes = []

        elif key == ord('q'):
            exit()

cv2.destroyAllWindows()
