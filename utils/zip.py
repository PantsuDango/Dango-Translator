import gzip
import shutil
import os
import zipfile

def zipFiles(file_list, output_zip_path) :

    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf :
        for file in file_list:
            # 获取文件的绝对路径
            abs_path = os.path.abspath(file)
            # 加入压缩包
            zipf.write(abs_path, os.path.relpath(abs_path, os.path.dirname(abs_path)))