from ultralytics import YOLO

# Load local weights
model = YOLO("data/models/yolov8n.pt")

def get_crowd_density(image_path: str) -> float:
    results = model(image_path, verbose=False)
    people_count = 0
    cars_count = 0
    
    for r in results:
        for c in r.boxes.cls:
            cls_id = int(c)
            if cls_id == 0:  # COCO class 0 is person
                people_count += 1
            elif cls_id in [2, 3, 5, 7]:  # car, motorcycle, bus, truck
                cars_count += 1
                
    if (people_count + cars_count) == 0:
        return 0.0
        
    return people_count / (people_count + cars_count)