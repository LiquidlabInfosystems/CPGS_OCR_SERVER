import base64
import os
import tempfile
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
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
        # Assume base64 string is sent in JSON body or form data
        if req.content_type == 'application/json':
            data = json.loads(req.body)
            if 'frame' not in data:
                return HttpResponse("No frame provided", status=400)
            base64_string = data['frame']
        else:
            # Fallback to form data
            base64_string = req.POST.get('frame')
            if not base64_string:
                return HttpResponse("No frame provided", status=400)

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
            return HttpResponse(ocr_output)

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

