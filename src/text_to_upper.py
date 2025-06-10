import keyboard
import pyperclip
import time
import win32clipboard
import win32con

def convert_to_upper():
    print("热键被触发！")
    try:
        # 保存当前剪贴板内容
        win32clipboard.OpenClipboard()
        try:
            original_clipboard = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        except:
            original_clipboard = ""
        win32clipboard.CloseClipboard()
        
        # 清空剪贴板
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()
        
        # 模拟 Ctrl+C 复制选中的文本
        keyboard.send('ctrl+c')
        time.sleep(0.2)  # 增加等待时间
        
        # 获取选中的文本
        win32clipboard.OpenClipboard()
        try:
            selected_text = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        except:
            selected_text = ""
        win32clipboard.CloseClipboard()
        
        if selected_text:
            # 将文本转换为大写
            upper_text = selected_text.upper()
            
            # 将转换后的文本放回剪贴板
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(upper_text, win32con.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            
            # 模拟 Ctrl+V 粘贴
            keyboard.send('ctrl+v')
            time.sleep(0.1)
            
            # 恢复原始剪贴板内容
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(original_clipboard, win32con.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            
            print("转换完成！")
        else:
            print("未检测到选中的文本")
            
    except Exception as e:
        print(f"发生错误: {str(e)}")

def main():
    print("文本转大写工具已启动...")
    print("按下 F2 将选中的文本转换为大写")
    print("按 Ctrl+C 退出程序")
    print("--------------------------------")
    
    # 注册热键
    keyboard.add_hotkey('f2', convert_to_upper)
    print("热键已注册，请选择文本后按 F2 进行转换")
    
    # 等待退出命令
    keyboard.wait('ctrl+c')

if __name__ == "__main__":
    main() 