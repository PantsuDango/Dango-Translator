import gzip
import shutil
import os
import zipfile

# 打包指定文件列表
def zipFiles(file_list, output_zip_path) :

    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf :
        for file in file_list:
            # 获取文件的绝对路径
            abs_path = os.path.abspath(file)
            # 加入压缩包
            zipf.write(abs_path, os.path.relpath(abs_path, os.path.dirname(abs_path)))


# 打包指定目录
def zipDirectory(directory_path, zip_path) :
    # 创建压缩文件
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历目录下的所有文件和子目录
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                # 获取文件的绝对路径
                file_path = os.path.join(root, file)
                # 将文件添加到压缩文件中
                zipf.write(file_path, os.path.relpath(file_path, directory_path))