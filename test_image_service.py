from app.services.image_service import ImageService

temp_file = ImageService.save_temp_image("app/storage/images/Sandeep.jpg")
print(temp_file)
ImageService.delete_image(temp_file)
print("Deleted Successfully")
