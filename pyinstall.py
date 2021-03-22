'''
Author: your name
Date: 2020-09-28 15:41:31
LastEditTime: 2021-03-22 16:47:45
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /qqSsoGather/pyinstall.py
'''
if __name__ == '__main__':
    from PyInstaller.__main__ import run
    opts = ['main_user.py',
            'home.py',
            'login.py',
            'utils.py',
            'HouyiApi.py',
            '-F',
            '-w',
        #     '-D',
            '--icon=icon.ico']
    run(opts)
