## This file explains the primary functions for results/
### views.py
- `def barchart(request):`
  - The try/except block handles the case of user accessing the results page without uploading an image.
  - If not, the exception raised redirects the user to an error page.
  - If an image has been uploaded, the code pulls the probability values set in upload/views.py and creates a bar chart using matplotlib.
  - 'Both' probability is ignored as requested by the client.
  - The bar chart is saved as a png file and is overriden each time results are generated.
