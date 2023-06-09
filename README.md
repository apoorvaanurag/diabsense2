# Welcome to DiabSense

DiabSense helps detect possibilities of various diabetic foot ulcer complications, by letting the user scan an image of the bruise and displaying the results in form of percentage chances.  
The image recognition model comprises of two parts - 
* Part 1 handles validation. Is it actually a foot image?
* Part 2 does the actual classification among infection, ischaemia and/or none. It is comprised of ResNet and Vision Transformer Models in form of an ensemble.

## How it works?
DiabSense is built using the Django-framework. At the backend, the classification problem is solved using an ensemble of ResNets and Vision Transformers, post-processing of the image. 
  
<img src="working/home_mobile.png" width="300"> <img src="working/results_mobile.png" width="300">

## How to use 
<!-- numbered list -->
1. Clone the repository
2. Run virtual environment `[Recommended]`
3. Install the requirements from requirements.txt
4. Setup your .config file. Refer to the .config.example file for reference
5. Run the server using `python manage.py runserver`
6. Open the link in your browser




## Collaborators
* [apoorvaanurag](https://github.com/apoorvaanurag/)
* [idkwhoiam322](https://github.com/idkwhoiam322/)
