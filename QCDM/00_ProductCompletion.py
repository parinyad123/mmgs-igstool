import os

# module ProductCompletion.py ->> check amount of files and opening

def Product_Comp(address): # address คือ path_UnZipProduct
    
    ext_dict_ref01 = {"JPG":3, 'HTM':1, 'PDF':1, 'TIF':1, 'DIM':1, 'XSL':1} # dict สำหรับอ้างอิง นามสกุล และ จำนวน file
    ext_dict = {} # dict เก็บ นามสกุล กับ จำนวน file ที่อยู่ใน product
    ext_dict_diff = {}
    file_list = [] # เก็บชื่อ file ทั้งหมด ใน path_UnZipProduct
    file_group = []
    root_list = []
    ext_list = []
    incompletion_list = []
    

# step 1: เก็บชื่อ paths และ files ทั้งหมด ใน path_UnZipProduct
    for (root, _, files) in os.walk(address, topdown=True):

        for f in files:
            print(root+"/"+f)
        
        root_list.append(root) # เก็บ path ที่อยู่ใน path_UnZipProduct ไว้ใน root_list สำหรับ step3
        # print("root list -> ",root_list)
        '''
        root ->>> path ของ directory ทั้งหมดที่อยู่ใน path_UnZipProduct

        1st loop: D:\pom\SampleProduct02
        2nd loop: D:\pom\SampleProduct02\TH_CAT_21020208295419_1_1P_GOBI_20210202
        3rd loop: D:\pom\SampleProduct02\TH_CAT_21020208295419_1_1P_GOBI_20210202\TH_CAT_21020208295419_1
        
        3rd loop for root_list ->>>
        ['D:\\pom\\SampleProduct02', 'D:\\pom\\SampleProduct02\\TH_CAT_21020208295419_1_1P_GOBI_20210202', 'D:\\pom\\SampleProduct02\\TH_CAT_21020208295419_1_1P_GOBI_20210202\\TH_CAT_21020208295419_1']

        '''
        
        file_list = file_list + files # เก็บชื่อ file ทั้งหมด ใน path_UnZipProduct ไว้ใน file_list สำหรับ step2
        '''
        file_list ->>>

        1st loop: []
        2nd loop: ['LOGO.JPG', 'README.HTM', 'TH_CAT_21020208295419_1.PDF']
        3rd loop: ['LOGO.JPG', 'README.HTM', 'TH_CAT_21020208295419_1.PDF', 'ICON.JPG', 'IMAGERY.TIF', 'METADATA.DIM', 'PREVIEW.JPG', 'STYLE.XSL']
        
        '''
        
        file_group.append(files) # เก็บชื่อ file โดยแยกตาม directory ใน path_UnZipProduct ไว้ใน file_group สำหรับ step3
        # print('file group : ', file_group)
        '''
        file_group ->>>

        1st loop: [[]]
        2nd loop: [[], ['LOGO.JPG', 'README.HTM', 'TH_CAT_21020208295419_1.PDF']]
        3rd loop: [[], ['LOGO.JPG', 'README.HTM', 'TH_CAT_21020208295419_1.PDF'], ['ICON.JPG', 'IMAGERY.TIF', 'METADATA.DIM', 'PREVIEW.JPG', 'STYLE.XSL']]
        
        '''


# step2: check จำนวน file ใน product ว่าครบ หรือไม่

    # เก็บนามสกุลของ file จาก file_list ไว้ใน ext_list
    for f in file_list:
        ext_list.append(f.split('.')[1])
    
    # print("ext_list = ",ext_list)

    # นับนามสกุล file แล้วเก็บไว้ใน dict: ext_dict
    ext_dict = {"JPG":ext_list.count('JPG'), 'HTM':ext_list.count('HTM'),
    'PDF':ext_list.count('PDF'), 'TIF':ext_list.count('TIF'), 'DIM':ext_list.count('DIM'),
    'XSL':ext_list.count('XSL')}

    # ทำการเปรียบเทียบจำนวนไฟล์ที่ถูกระบุไว้ใน dict อ้างอิง (ext_dict_ref01) กับ dict ext_dict
    for k in ext_dict_ref01: # k คือ key ใน ext_dict_ref01
        # ถ้าจำนวน file ใด ไม่เท่ากันให้ เก็บลง ext_dict_diff
        if ext_dict_ref01[k]!=ext_dict[k]:
            ext_dict_diff[k] = ext_dict_ref01[k]-ext_dict[k]

# step3: check file เปิดได้หรือไม่
    for p_root, p_file in zip(root_list, file_group): 
        '''
        ใช้ zip เพื่อจับคู่ root และ file ที่อยู่ใน root นั้น

        1st loop:
        D:\pom\SampleProduct02\TH_CAT_21020208295419_1_1P_GOBI_20210202
        ['LOGO.JPG', 'README.HTM', 'TH_CAT_21020208295419_1.PDF']

        2nd loop:
        D:\pom\SampleProduct02\TH_CAT_21020208295419_1_1P_GOBI_20210202\TH_CAT_21020208295419_1
        ['ICON.JPG', 'IMAGERY.TIF', 'METADATA.DIM', 'PREVIEW.JPG', 'STYLE.XSL']
        
        '''

        # ทำการ open/close file ถ้า cannot open เก็บชื่อ file ไว้ใน incompletion_list
        for a_file in p_file:
            try:
                (open(p_root+'/'+a_file)).close()
                    # print('ok => ', a_file)
            except IOError:
                    incompletion_list.append(a_file)

    print(ext_dict_diff, incompletion_list, len(ext_dict_diff)==0 and len(incompletion_list)==0)
    return ext_dict_diff, incompletion_list, len(ext_dict_diff)==0 and len(incompletion_list)==0


# Product_Comp('D:\pom\SampleProduct02')