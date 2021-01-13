'''
Author: your name
Date: 2020-09-28 15:41:31
LastEditTime: 2021-01-13 15:48:10
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /qqSsoGather/pyinstall.py
'''
if __name__ == '__main__':
    from PyInstaller.__main__ import run
    opts = ['main.py',
            'home.py',
            'login.py',
            'utils.py',
            'UploadData.py',
            'DataGather.py',
            '-F',
            '-w',
        #     '-D',
            '--icon=icon.ico']
    run(opts)
