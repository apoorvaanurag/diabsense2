from PIL import Image

def convert_to_square_image(image_path):
    with Image.open(image_path) as img:
        # get the size of the image
        width, height = img.size
        # find the minimum dimension
        min_dimension = min(width, height)
        # calculate the center of the image
        center_x, center_y = width // 2, height // 2
        # calculate the coordinates of the square
        left = center_x - min_dimension // 2
        upper = center_y - min_dimension // 2
        right = left + min_dimension
        lower = upper + min_dimension
        # crop the image to the square
        img = img.crop((left, upper, right, lower))
        # resize the image to 300x300 (or any desired size)
        img = img.resize((224, 224))
        # save the image
        img.save(image_path)