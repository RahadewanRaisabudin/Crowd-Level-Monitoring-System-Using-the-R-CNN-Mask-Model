import cv2
import numpy as np
import os
import sys
import time
from mrcnn import utils
from mrcnn import model as modellib
import random
ROOT_DIR = os.path.abspath("./")
MODEL_DIR = os.path.join(ROOT_DIR, "logs")
sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))
from samples.coco import coco

COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
print(COCO_MODEL_PATH)
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

class InferenceConfig(coco.CocoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
config.display()

model = modellib.MaskRCNN(
    mode="inference", model_dir=MODEL_DIR, config=config
)
model.load_weights(COCO_MODEL_PATH, by_name=True)
class_names = ['BG', 'person']

def apply_mask(image, mask, color, alpha=0.5):
    """apply mask to image"""
    for n, c in enumerate(color):
        image[:, :, n] = np.where(
            mask == 1,
            image[:, :, n] * (1 - alpha) + alpha * c,
            image[:, :, n]
        )
    return image

def display_person_instances(image, boxes, masks, ids, names, scores):
    """
        take the image and results and apply the mask, box, and Label
    """
    n_instances = boxes.shape[0]
    if not n_instances:
        print('NO INSTANCES TO DISPLAY')
    else:
        assert boxes.shape[0] == masks.shape[-1] == ids.shape[0]

    for i in range(n_instances):
        if not np.any(boxes[i]):
            continue

        if names[ids[i]] == 'person':
            y1, x1, y2, x2 = boxes[i]
            caption = '{} {:.2f}'.format(names[ids[i]], scores[i]) if scores is not None else names[ids[i]]
            mask = masks[:, :, i]

            # Generate a random color for each person instance
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            # Update the caption position to be above the bounding box
            caption_position = (x1, max(y1 - 10, 0))

            image = apply_mask(image, mask, color)
            image = cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
            image = cv2.putText(
                image, caption, caption_position, cv2.FONT_HERSHEY_COMPLEX, 0.7, color, 2
            )

    return image
def count_person_in_roi(boxes, class_ids, roi_start_x, roi_start_y, roi_end_x, roi_end_y):
    count = 0
    for i in range(len(boxes)):
        if class_ids[i] == class_names.index('person'):
            y1, x1, y2, x2 = boxes[i]  # Perhatikan urutan koordinat kotak (y1, x1, y2, x2)
            # Memeriksa apakah kotak terletak di dalam ROI box
            if x1 >= roi_start_x and x2 <= roi_end_x and y1 >= roi_start_y and y2 <= roi_end_y:
                count += 1
    return count

if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        print("run command: python demo.py 0 or video file name")
        sys.exit(0)
    name = args[1]
    if len(args[1]) == 1:
        name = int(args[1])

    stream = cv2.VideoCapture(name)
    width, height = stream.get(cv2.CAP_PROP_FRAME_WIDTH), stream.get(cv2.CAP_PROP_FRAME_HEIGHT)
    out = cv2.VideoWriter('file name.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, (int(width), int(height)))

    frame_count = 0
    start_time = time.time()
    # Create a red ROI box in the middle of the frame
    roi_box_width = 700
    roi_box_height = 550
    roi_box_color = (0, 0, 255)
    roi_box_thickness = 2

    roi_start_x = int((width - roi_box_width) / 2)
    roi_start_y = int((height - roi_box_height) / 2)
    roi_end_x = roi_start_x + roi_box_width
    roi_end_y = roi_start_y + roi_box_height

    total_count = 0
    frames_since_last_count = 0
    last_count = 0

    # Variables for resetting count
    frame_threshold_for_reset = 900
    frames_since_last_reset = 0

    while True:
        ret, frame = stream.read()

        results = model.detect([frame], verbose=0)
        r = results[0]
        person_indices = np.where(r['class_ids'] == class_names.index('person'))[0]
        person_rois = r['rois'][person_indices]
        person_masks = r['masks'][:, :, person_indices]
        person_class_ids = r['class_ids'][person_indices]
        person_scores = r['scores'][person_indices]
        masked_image = display_person_instances(
            frame, person_rois, person_masks, person_class_ids, class_names, person_scores
        )

        # Draw the ROI box
        cv2.rectangle(masked_image, (roi_start_x, roi_start_y), (roi_end_x, roi_end_y), roi_box_color, roi_box_thickness)

        # Menghitung jumlah orang dalam ROI box
        count = count_person_in_roi(person_rois, person_class_ids, roi_start_x, roi_start_y, roi_end_x, roi_end_y)


        frames_since_last_count += 1
        frames_since_last_reset += 1
        
        # Check if it's time to reset the count 
        if frames_since_last_reset >= frame_threshold_for_reset:
            total_count = 0  # Reset the count
            last_count = 0   # Reset the last count as well
            frames_since_last_reset = 0

        # Jika sudah 55 frame sejak total count terakhir diupdate, update total count
        if frames_since_last_count >= 55:
            total_count = last_count + count
            last_count = total_count
            frames_since_last_count = 0

        # Check if it's time to reset the count
        if frames_since_last_reset >= frame_threshold_for_reset:
            total_count = 0  # Reset the count
            frames_since_last_reset = 0

        # Menampilkan total count dan status pada frame
        status = ""
        if total_count <= 5:
            status = "Sepi"
            status_color = (0, 0, 255)
        elif total_count <= 12:
            status = "Sedang"
            status_color = (0, 255, 255)
        else:
            status = "Ramai"
            status_color = (0, 255, 0)
        
        #show the information
        cv2.putText(masked_image, "Poeple: {}".format(total_count), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(masked_image, "Status: {}".format(status), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
        

        # Calculate FPS every frame
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time
        fps_text = f"FPS: {fps:.2f}"
        cv2.putText(masked_image, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Draw black boxes behind FPS, visitor count, and status
        cv2.rectangle(frame, (0, 0), (200, 100), (0, 0, 0), -1)
        cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"Jumlah Orang: {total_count}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"Status: {status}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)

        cv2.namedWindow("masked_image", cv2.WINDOW_NORMAL)
        cv2.imshow("masked_image", frame)
        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    stream.release()
    out.release()
    cv2.destroyWindow("masked_image")