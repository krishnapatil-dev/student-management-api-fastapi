def row_to_dict(row):
    return{
        "id" : row[0],
        "name" : row[1],
        "age" : row[2],
        "marks" : row[3]
    }