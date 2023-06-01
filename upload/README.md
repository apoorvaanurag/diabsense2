## This file explains the primary functions for upload/
### Setup
- The three required models are:
    - model1.pt
    - model2.pt
    - validate.pt
### views.py
- Configure firebase credentials.
- `def image_request(request)`
    - When a user uploads an image, a form is created and the img file name is saved.
    - The image is validated to confirm if it is a DFU image.
    - If the image is valid, it is uploaded to firebase cloud storage and a download url is generated.
    - The image is resized to a square image of 224x224 pixels and SLIC algorithm is applied to segment the image to recreate model's training image conditions.
    - The modified image is sent to the model and the probability values are returned.
    - The probability values are saved in a list and passed to results/views.py.
    - The modified image is not stored.

### convert_to_square_image.py
- Resizes the image to a square image of 224x224 pixels.

### dfuc.py
- Takes image as an input and generates a list of probability values.

### footValid.py
- Validates if the image is a DFU image.

### slic_apply.py
- Applies SLIC algorithm to segment the image.
