"""
    =============================
    =============================
    1.pdf =>     jpg
    2.jpg =ocr=> txt
    3.txt =>     excel
    =============================
    =============================

"""



from aip import AipOcr
from datetime import date, datetime
import PythonMagick
import ghostscript
import PyPDF2
import json
import xlrd
import xlwt
import sys
import os
import re
import urllib.request,urllib.error,urllib.parse,sys,ssl,json
import base64



"""初始化信息"""
# 获得当前目录的规范绝对路径
nowUrl=os.path.abspath(__file__)
# 获取父级目录的绝对路径
fatherUrl=os.path.abspath(os.path.dirname('__file__'))
#初始化接口参数信息
""" 你的 APPID AK SK """
APP_ID = '11333917'
API_KEY = '15GrG4tIZzZLDQUUPAun128v'
SECRET_KEY = '4TGtNMPxNGg8hP6RcMsGveDfxcicwPuF'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
#img识别失败的文件
ocrFalseImg=[]
# 检测中文函数
zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
def contain_zh(word):
    global zh_pattern
    match = zh_pattern.search(word)
    return match
#获取Access_token /// client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=15GrG4tIZzZLDQUUPAun128v&client_secret=4TGtNMPxNGg8hP6RcMsGveDfxcicwPuF'
request1=urllib.request.Request(host)
request1.add_header('Content-Type', 'application/json;charset=UTF-8')
response = urllib.request.urlopen(request1)
content = response.read()
# if (content):
#     print(json.loads(str(content, encoding = "utf-8"))['access_token'])
Access_token=json.loads(str(content, encoding = "utf-8"))['access_token']


api_url = "https://aip.baidubce.com/rest/2.0/solution/v1/iocr/recognise?access_token="+Access_token 




'''
    =============================
    pdf2jpg,def后目录在img文件夹下
    =============================
'''
# 获取pdf目录下的pdf文件信息
pdfName = os.listdir(fatherUrl+'/pdf')
pdfNames = [] #pdf的文件名数组
for index in range(len(pdfName)):
    pdfNames.append(str(pdfName[index]))
imgNames = [] #切割后的img文件名数组

"""将pdf转图片,至当前目录下的img文件夹"""
# 在当前目录创建img文件夹
os.mkdir("img")
# 进入img文件夹
os.chdir(fatherUrl+'/img')

for pdfIndex in range(len(pdfNames)):
    # 第一个参数为拼接的pdf绝对路径,读取单个pdf,
    # PDF名为 ==> fatherUrl+'/pdf/'+pdfNames[i]
    pdf_im = PyPDF2.PdfFileReader(fatherUrl+'/pdf/'+pdfNames[pdfIndex], "rb")
    os.mkdir(str(pdfNames[pdfIndex])[:-4])
    os.chdir(fatherUrl+'/img/'+str(pdfNames[pdfIndex])[:-4])
    # 获取pdf页数
    pdf_num = pdf_im.getNumPages()

    print('fdsfdsfs'+str(pdfIndex+1)+'fsdfsdfsdf'+str(pdf_num)+'fdsfsd,ffsdfsd'+pdfNames[pdfIndex]+'】')
    for p in range(pdf_num):
        try:
            im = PythonMagick.Image()
            im.density('300')  # 设置dpi，不设置估计就96dpi
            im.read(fatherUrl+'//pdf//'+pdfNames[pdfIndex]+'['+str(p)+']')
            # 当前以在img目录下
            im.write(str(pdfNames[pdfIndex])[:-4] +'_'+ str(p+1) + '.jpg')
            imgNames.append(str(pdfNames[pdfIndex])[:-4] +'_'+ str(p+1) + '.jpg')
            print("fdsfdsf"+str(pdfIndex+1)+"fsdfsdfs  >>>   "+str(p+1)+"/"+str(pdf_num)+'fsdfsdfsf')
        except Exception as e:
            print('========================================')
            print('Skip the first page')
            print('========================================')
            continue


    '''
        =============================
        jpg调ocr识别,
        =============================
    '''
    # 选择目录
    os.chdir(fatherUrl+'/img/'+str(pdfNames[pdfIndex])[:-4])
    # 获取img目录下的文件信息
    imgFileName = os.listdir()
    imgFileNames = []
    for index in range(len(imgFileName)):
        imgFileNames.append(str(imgFileName[index])[:-4])
    # 输出img文件夹下的文件名（数组形式）
    # print(imgFileNames)
    #img数量
    imgFileNamesLen=len(imgFileNames)
    #返回根目录=>创建txt文件夹=>进入txt文件夹   （写入前进入目录）
    if pdfIndex==0:
        os.chdir(fatherUrl)
        os.mkdir('txt')
        os.chdir(fatherUrl+'/txt')
        os.mkdir(str(pdfNames[pdfIndex])[:-4])
        os.chdir(fatherUrl+'/txt/'+str(pdfNames[pdfIndex])[:-4])
    else:
        os.chdir(fatherUrl+'/txt')
        os.mkdir(str(pdfNames[pdfIndex])[:-4])
        os.chdir(fatherUrl+'/txt/'+str(pdfNames[pdfIndex])[:-4])
    print('fsdfdsfs'+str(imgFileNamesLen)+'fdsfdsfsf')
    print('------------------')

    for txtIndex in range(len(imgFileName)):
        """ 读取图片 """
        def get_file_content(filePath):
            with open(filePath, 'rb') as fp:
                return base64.b64encode(fp.read())

        image = get_file_content(fatherUrl+'/img/'+str(pdfNames[pdfIndex])[:-4]+'/'+imgFileName[txtIndex])

        print('fdsfsfsfs'+imgFileName[txtIndex]+'】'+'   fsdfsdfs'+str(txtIndex)+'/'+str(imgFileNamesLen))
        """ 如果有可选参数 """
        options = {}
        options["detect_direction"] = "true"
        options["probability"] = "true"
        templateSign = "f3b35f4c3d36db6b89c9608ea288d8b6"
        classifierId = int(1)
        """ 带参数调用通用文字识别, 图片参数为本地图片 """

        try:
            # result = client.custom(image, templateSign)
            postdata = urllib.parse.urlencode({  
                "image":image,  
                # "templateSign":"f3b35f4c3d36db6b89c9608ea288d8b6",
                "classifierId":1
            }).encode("utf-8") #将数据使用urlencode编码后，使用encode（）设置utf-8编码  

            req = urllib.request.Request(api_url,postdata)  
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')

            result = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))
            # result类型
            # print(type(result))
            # result数据
            # print(result)
        except Exception as e: 
            print('fdsfsd,fsdfsdfs')
            print(e)
            continue

        try:
            if result['data']['isStructured']=='False':
                ocrFalseImg.append(imgFileName[txtIndex])
                print('------------------')
                print('【'+str(imgFileName[txtIndex])+'】'+'   fdsfsd,grgrtgdf')
                print('------------------')
                continue
            # print('------------------')
            # print('构化匹配成功！开始进行文件写入...')
            # print('------------------')
        except Exception as e: 
            print("fdsfsdcx")
            print(e)
            continue

        try:
            jump=False
            # 打印报告编号,并直接判断报告编号中的中文
            print(result['data']['ret'][len(result['data']['ret'])-1]['word'])
            if contain_zh(result['data']['ret'][len(result['data']['ret'])-1]['word']):
                jump=True

            if jump==False:
                print('------------------')
                print('dfdsfsfs...')
                print('------------------')
                for i in range(len(result['data']['ret'])):
                    with open(imgFileNames[txtIndex]+r'.txt', 'a') as f:
                        f.write(result['data']['ret'][i]['word']+'\n')
                    print('fdsfdsfs=>'+str(result['data']['ret'][i]['word_name']))
                    print('------------------')

                print('【'+imgFileNames[txtIndex]+r'.txt'+'】'+'   fdsfsdf')
                print('------------------')
            else:
                print('------------------')
                print('fdsfdsfsfds,【break！】...')
                print('------------------')
 

                # if contain_zh(str(result['data']['ret'][i]['word'])):
                #     print('包含中文,跳过本次创建')
                #     continue
                # else:
                #     with open(imgFileNames[txtIndex]+r'.txt', 'a') as f:
                #         f.write(result['data']['ret'][i]['word']+'\n') 
                #     print('成功写入=>'+str(result['data']['ret'][i]['word_name']))
                #     print('------------------')

    
        except Exception as e: 
            print(e)

    print('fdfdsfdsdf,hvnvny:')
    print('==========================================')
    print(ocrFalseImg)



    '''
        =============================
        txt写入excel
        =============================
    '''

    # 选择目录
    os.chdir(fatherUrl+'/txt/'+str(pdfNames[pdfIndex])[:-4])
    # 获取txt目录下的文件信息
    txtFileName = os.listdir()
    txtFileNames = []
    for index in range(len(txtFileName)):
        txtFileNames.append(str(txtFileName[index])[:-4])
    # 输出txt文件夹下的文件名（数组形式）
    # print(txtFileNames)
    #txt数量
    txtFileNamesLen=len(txtFileNames)


    #返回根目录=>创建excel文件夹=>进入excel文件夹   （写入前进入目录）
    if pdfIndex==0:
        os.chdir(fatherUrl)
        os.mkdir('excel')
        os.chdir(fatherUrl+'/excel')
        os.mkdir(str(pdfNames[pdfIndex])[:-4])
        os.chdir(fatherUrl+'/excel/'+str(pdfNames[pdfIndex])[:-4])
    else:
        os.chdir(fatherUrl+'/excel')
        os.mkdir(str(pdfNames[pdfIndex])[:-4])
        os.chdir(fatherUrl+'/excel/'+str(pdfNames[pdfIndex])[:-4])




    print('fdfsdfsf'+str(txtFileNamesLen)+'gfcbgfg')
    print('------------------')
    # 生成对应文件长度的数组
    for arrIndex in range(len(txtFileName)):
        data={'date': [], 'id': [], 'arr': []}
    for fileIndex in range(len(txtFileName)):
        file = open(fatherUrl+'/txt/'+str(pdfNames[pdfIndex])[:-4]+'/'+str(txtFileName[fileIndex]))
        while 1:
            lines = file.readlines()
            if not lines:
                break
            for index in range(len(lines)):
                newLine = ''.join(lines[index]).strip('\n')

                """处理字符串"""
                threeLine=''.join(lines[2]).strip('\n')       
                if threeLine[0:6]:
                    # 截取前六位
                    txtIndex=threeLine[0:6]
                else:
                    break
                # 替换前六位变成 （,*****）
                newTxt=threeLine.replace(txtIndex,','+txtIndex)
                # 字符串转数组
                txtArr=newTxt.split(',')
                # 删除数组第一项
                del txtArr[0]

                


                if str(index) == '0':
                    for dateIndex in range(len(txtArr)):
                        data['date'].append(newLine)
                elif str(index) == '1':
                    for dateIndex in range(len(txtArr)):
                        data['id'].append(newLine)
                elif str(index) == '2':
                    for i in range(len(txtArr)):
                        data['arr'].append(txtArr[i])
        file.close()
    # print(data)

    def set_style(name, height, bold=False):
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = name  # 'Times New Roman'
        font.bold = bold
        font.color_index = 4
        font.height = height
        style.font = font
        return style

    # 写excel
    def write_excel():  
        f = xlwt.Workbook()  # 创建工作簿

        '''
    创建第一个sheet:
        sheet1
    '''
        sheet1 = f.add_sheet(u'sheet2', cell_overwrite_ok=True)  # 创建sheet
        row0 = [u'报告编号', u'焊缝编号', u'检测日期']

        # 生成第一行
        for i in range(0, len(row0)):
            sheet1.write(0, i, row0[i])
        # 为1至3列写入数据库
        for j in range(0, 3):
            if j==0:
                for index_date in range(len(data['date'])):
                    sheet1.write(index_date+1,0,data['id'][index_date])
            if j==1:
                for index_date in range(len(data['date'])):
                    sheet1.write(index_date+1,1,data['arr'][index_date])
            if j==2:
                for index_date in range(len(data['date'])):
                    sheet1.write(index_date+1,2,data['date'][index_date])
        # 保存文件
        f.save(str(pdfNames[pdfIndex])[:-4]+'.xls')  


    if __name__ == '__main__':
        write_excel()

    print('dfsfsdfs'+str(pdfNames[pdfIndex])[:-4]+"fsdfsfsd")


    os.chdir(fatherUrl+'/img')
    
