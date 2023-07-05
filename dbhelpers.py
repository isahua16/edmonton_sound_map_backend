import mariadb
import dbcreds

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
