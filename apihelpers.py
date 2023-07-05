def check_data(data_type, required_data):
    for data in required_data:
        if(data_type.get(data) == None):
            return f'The {data} parameter is missing.'
