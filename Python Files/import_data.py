import pandas as pd
import getpass
import numpy as np

def import_inventory_data(filename):
    '''

    :param filename:
    :return:
    '''

    ''' read csv file to import raw data'''
    df = pd.read_csv(filename, skiprows=5)

    ''' adjust column values to combine the first 2 rows into 1 column structure'''
    df1 = df.iloc[0:1]
    col_name = None
    col_list =[]
    for i, col in enumerate(list(df1.columns)):
        value = str(df1[col].iloc[0]).strip()
        if "Unnamed:" not in col:
            col_name = col.strip()
        if value in ["", 'nan']:
            col_list.append(col_name)
        else:
            col_list.append(f'{col_name} || {value}')

        print(col_name, value)
    df.columns  = col_list

    ''' remove the first 2 rows'''
    df = df.iloc[2:]

    ''' get a list of all the existing warehouses in column names'''
    list_of_warehouses = [x.split("||")[0].strip() for x in col_list if "||" in x]
    list_of_warehouses = list(dict.fromkeys(list_of_warehouses))

    '''create a global dataframe to stack each warehouse dataframe into'''
    df3 = pd.DataFrame()

    '''create a unqiue dataframe for each warehouse'''
    attribute_columns = ['Item', 'Division', 'Brand', 'Product Category', 'Inventory Item: Product Sub-Category', 'Description']
    for each_warehouse in list_of_warehouses:
        '''get the corresponding warehouse columns'''
        current_warehouse_column_set = [x for x in col_list if x.split("||")[0].strip() == each_warehouse]
        '''merge the attribute columns and the warehouse columnd'''
        final_wh_column_list = attribute_columns + current_warehouse_column_set
        # print("Hello", each_warehouse, current_warehouse_column_set)
        '''create a new DF of just the specific columns mapped above'''
        df2 = df[final_wh_column_list]
        '''get the column names of the metric by remove the warehouse from the column name'''
        new_column_values = [x.split("||")[-1].strip() for x in current_warehouse_column_set]
        rename_columns_to = attribute_columns + new_column_values
        df2.columns = rename_columns_to
        '''add a column for the warehouse'''
        df2['warehouse'] = each_warehouse

        '''stack the global dataframe'''
        df3 = df3.append(df2)
    df3.to_csv(f'C:\\Users\\SIMPLE TO WORK\\Desktop\\sample.csv', index=False)

    '''drop all rows that have no numeric data'''
    df3 = df3.dropna(subset=[*new_column_values], how='all')
    print(df3)

    df3.to_csv(f'C:\\Users\\SIMPLE TO WORK\\Desktop\\sample1.csv', index=False)


if __name__ == '__main__':
    filename = f'C:\\Users\\{getpass.getuser()}\\Downloads\\Python_practice.csv'
    import_inventory_data(filename)

