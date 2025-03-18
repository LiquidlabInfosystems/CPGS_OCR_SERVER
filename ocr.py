import cv2
import easyocr
import numpy as np

# Load the image
image_path = "license_plate.jpg"  # Use your image path
image = cv2.imread(image_path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Bilateral Filtering to remove noise while keeping edges sharp
filtered = cv2.bilateralFilter(gray, 11, 17, 17)

# Adaptive Thresholding to enhance contrast
binary = cv2.adaptiveThreshold(
    filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
)

# Sharpen the image
sharpen_kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
sharpened = cv2.filter2D(binary, -1, sharpen_kernel)

# Resize the image to make text more readable
resized = cv2.resize(sharpened, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

# Initialize EasyOCR Reader
reader = easyocr.Reader(["en"])  # Add other languages if needed

# Perform OCR
results = reader.readtext(resized)

# Extract text
detected_text = " ".join([res[1] for res in results])
print("🔹 Detected License Plate Text:", detected_text)

# Show processed image
cv2.imshow("Processed Image", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()

