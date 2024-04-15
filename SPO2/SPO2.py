# r'C:\Users\MEDIOT\ABA_project\ABA_project\SPO2\SPO2_data.log', "r"

with open(r'C:\Users\MEDIOT\ABA_project\ABA_project\SPO2\SPO2_data.log', "r+") as file:
   
    data = file.read()

    explodedData=data.split("55AA0604")
    explodedData = [element[:-4] for element in explodedData[1:-1]]
    print(explodedData)
    decimal_values = [int(element, 16) for element in explodedData]
    decimal_values=filter (lambda x:x<=100, decimal_values)
    print(list(decimal_values))




