import os
import uuid
def save_file(file):
    # Check to see if first, the filename contains a . character. 
    # Then, split the filename around the . characters into an array
    # Then, see if the filename ends with any of the given extensions in the array
    # You can add or remove file types you want or do not want the user to store
    if('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ['gif','png','jpg','jpeg', 'webp', 'pdf']):
        # Create a new filename with a token so we don't get duplicate file names
        # End the filename with . and the original filename extension
        filename = uuid.uuid4().hex + '.' + file.filename.rsplit('.', 1)[1].lower()
        try:
            # Use built-in functions to save the file in the images folder
            # You can put any path you want, in my example I just need them in the images folder right here
            file.save(os.path.join('images', filename))
            # Return the filename so it can be stored in the DB
            return filename
        except Exception as error:
            # If something goes wrong, print out to the terminal and return nothing
            print('FILE SAVE ERROR:' , error)
    # If any conditional is not met or an error occurs, None is returned


def check_data(data_type, required_data):
    for data in required_data:
        if(data_type.get(data) == None):
            return f'The {data} parameter is missing.'
