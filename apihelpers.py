import os
import uuid
def save_file(file, folder, extensions):
    if('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in extensions):
        filename = uuid.uuid4().hex + '.' + file.filename.rsplit('.', 1)[1].lower()
        try:
            file.save(os.path.join(folder, filename))
            return filename
        except Exception as error:
            print('FILE SAVE ERROR:' , error)



def check_data(data_type, required_data):
    for data in required_data:
        if(data_type.get(data) == None):
            return f'The {data} parameter is missing.'
