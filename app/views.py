import base64
import os
import tempfile
from bson import ObjectId
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
# from app.models import Spaces
from mongoClient import get_mongo_client
from paddleocr import PaddleOCR
import json

# Initialize PaddleOCR once at module level
ocr = PaddleOCR(use_angle_cls=True, lang='en')

@csrf_exempt
def get_ocr(req):
    print('here')
    if req.method != 'POST':
        return HttpResponse("Method not allowed", status=405)

    try:
       
        base64_string = req.POST.get('frame')
        document_id = req.POST.get('document_id')
        if  base64_string is None or  document_id is None:
            return HttpResponse("Required frame and document_id", status=400)

        # Remove 'data:image/jpeg;base64,' prefix if present
        if ';base64,' in base64_string:
            base64_string = base64_string.split(';base64,')[-1]

        # Decode base64 string
        img_data = base64.b64decode(base64_string)

        # Save to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
            tmp.write(img_data)
            tmp_path = tmp.name

        try:
            # Run OCR
            result = ocr.ocr(tmp_path, cls=True)
            if result and isinstance(result, list) and len(result) > 0 and result[0]:
                # Extract text from the first detected box (safely)
                ocr_output = result[0][0][1][0] if result[0][0][1] else "No text detected"
            else:
                ocr_output = "No text detected"
                
            # update database
            db = get_mongo_client()
            collection = db['spaces']
            result = collection.update_one( {"_id": ObjectId(document_id)}, {"$set": {"licenseNumber": ocr_output}})
            if result:
                return JsonResponse({'status':'ok'})
            return JsonResponse({'status':'Error At Ocr server'})

        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    except base64.binascii.Error:
        return HttpResponse("Invalid base64 string", status=400)
    except json.JSONDecodeError:
        return HttpResponse("Invalid JSON format", status=400)
    except Exception as e:
        return HttpResponse(f"OCR Error: {str(e)}", status=500)

