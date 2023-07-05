import mariadb
import dbcreds
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
            print(FILE SAVE ERROR: , error)
            return error.msg
    # If any conditional is not met or an error occurs, None is returned
def convert_data(cursor, results):
    column_names = [i[0] for i in cursor.description]
    new_results = []
    for row in results:
        new_results.append(dict(zip(column_names, row)))
    return new_results
def run_statement(sql, args=None):
    try:
        results = None
        conn = mariadb.connect(**dbcreds.conn_params)
        cursor = conn.cursor()
        cursor.execute(sql, args)
        results = cursor.fetchall()
        results = convert_data(cursor, results)
    except mariadb.OperationalError as error:
        print('Operational Error', error)
        results = error.msg
    except mariadb.ProgrammingError as error:
        print('SQL Error', error)
        results = error.msg
    except mariadb.IntegrityError as error:
        print('DB Integrity Error', error)
        results = error.msg
    except mariadb.DataError as error:
        print('Data Error', error)
        results = error.msg
    except mariadb.DatabaseError as error:
        print('DB Error', error)
        results = error.msg
    except mariadb.InterfaceError as error:
        print('Interface Error', error)
        results = error.msg
    except mariadb.Warning as error:
        print('Warning', error)
        results = error.msg
    except mariadb.PoolError as error:
        print('Pool Error', error)
        results = error.msg
    except mariadb.InternalError as error:
        print('Internal Error', error)
        results = error.msg
    except mariadb.NotSupportedError as error:
        print('Not Supporter By DB Error', error)
        results = error.msg
    except Exception as error:
        print('Unknown Error', error)
        results = error.msg
    finally:
        if(cursor != None):
            cursor.close()
        if(conn != None):
            conn.close()
        return results
