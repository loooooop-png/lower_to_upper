import PyInstaller.__main__
import os

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    os.path.join(current_dir, 'src', 'text_to_upper_gui.py'),
    '--name=文本转大写工具',
    '--windowed',
    '--onefile',
    '--icon=NONE',
    '--add-data=' + os.path.join(current_dir, 'src', 'hotkey_config.json') + ';.',
    '--clean',
    '--noconfirm'
]) 