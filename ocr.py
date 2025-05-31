import requests
from io import BytesIO
import base64
from tqdm import tqdm
import json

from config import DETECTOR_URL, RECOGNIZER_URL, HEADERS

class OCR:
    def __init__(self):
        self.detector_url = DETECTOR_URL
        self.recognizer_url = RECOGNIZER_URL
        self.headers = HEADERS

    def fetch_ocr(self, image):
        image = image.convert("RGB").resize((583, 424))
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
        image_base64 = "data:image/{};base64,{}".format("png", encoded)

        # Detect text regions
        response = requests.get(self.detector_url, headers=self.headers, json={"img": image_base64})
        bounding_boxes = self.get_boxes(response.json()[0]['horizontal_list'])
        if not bounding_boxes:
            return []
        # Recognize text in detected regions
        results = []
        for box in tqdm(bounding_boxes, total=len(bounding_boxes), desc="Recognizing text"): 
            try:
                response = requests.get(self.recognizer_url, headers=self.headers, json = {"bboxes": [box], "img": image_base64})
                result = response.json()[0][0]
                result['box'] = box
                results.append(result)
            except:
                print("Error in OCR recognition for box:", box)
        with open("ocr_results.json", 'w', encoding='utf-8') as f:
            json.dump(results, f, indent = 4)
        return results
        
    def get_boxes(self, bounding_boxes):
        new_boxes = []
        for item in bounding_boxes:
            new_boxes.append(
                [
                    item[0], 
                    item[2], 
                    item[1], 
                    item[3]
                ]
            )
        return new_boxes
        