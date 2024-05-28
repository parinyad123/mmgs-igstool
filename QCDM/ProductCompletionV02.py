import os

def Product_Completed(address):
   
    files_list = ['LOGO.JPG', 'README.HTM', 'PRODUCTSHEET.PDF', 'ICON.JPG', 'IMAGERY.TIF', 'METADATA.DIM', 'PREVIEW.JPG', 'STYLE.XSL']
    files_product_list = []
    difference_list = []

    root_product_list = []
    file_group = []
    incompletion_list = []

     # ---------------------- เช็คว่า file ครบมั้ย -------------------------

    for (root, _, files) in os.walk(address, topdown=True):
        root_product_list.append(root)
        # print('root = ', root_product_list)
        file_group.append(files)
        # print("file group = ",file_group)

        files_product_list.extend(files)
        # print("file = ", files_product_list)
    # print("file list = ", files_product_list)

    # convert lowwer string in files_product_list to uppper string
    files_product_list = [u.upper() for u in files_product_list]
    # print("file = ", files_product_list)
    # find index of pdf file
    index_pdf = [i for i, s in enumerate(files_product_list) if '.PDF' in s]
    # print("index = ", index_pdf)
    # change name of pdf file in list become 'PRODUCTSHEET.PDF'
    files_product_list[index_pdf[0]] = 'PRODUCTSHEET.PDF'
    # print("file product list = ", files_product_list)
    # for file in files_list:
    #     if file not in files_product_list:
    #         difference_list.append(file)

    # or 
    difference_list = [file for file in files_list if file not in files_product_list]
    # print("difference_list", difference_list)



    # ------------------------------ เช็คการเปิด file ------------------------------
    for p_root, p_file in zip(root_product_list, file_group):
        for a_file in p_file:
            try:
                (open(p_root+'/'+a_file)).close()
                # print('ok => ', a_file)
            except IOError:
                incompletion_list.append(a_file)



    # -------------------  return for 2 criteria -------------------------------
    return difference_list, incompletion_list, len(difference_list)==0 and len(incompletion_list)==0


# Product_Completed('D:\pom\SampleProduct02')