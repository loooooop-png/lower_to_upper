import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
import pyperclip
import time
import win32clipboard
import win32con
import json
import os
import threading

class TextToUpperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文本转大写工具")
        self.root.geometry("400x350")
        
        # 加载配置
        self.config_file = "hotkey_config.json"
        self.hotkey = self.load_config()
        
        # 录制状态
        self.is_recording = False
        self.recorded_keys = []
        self.hotkey_thread = None
        self.is_running = True
        
        # 创建UI元素
        self.create_widgets()
        
        # 启动热键监听
        self.start_hotkey_listener()
        
        # 程序关闭时清理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        # 热键设置框架
        hotkey_frame = ttk.LabelFrame(self.root, text="热键设置", padding="10")
        hotkey_frame.pack(fill="x", padx=10, pady=5)
        
        # 热键显示标签
        self.hotkey_label = ttk.Label(hotkey_frame, text=f"当前热键: {self.hotkey}")
        self.hotkey_label.pack(pady=5)
        
        # 录制按钮
        self.record_btn = ttk.Button(hotkey_frame, text="开始录制", command=self.toggle_recording)
        self.record_btn.pack(pady=5)
        
        # 录制状态标签
        self.recording_label = ttk.Label(hotkey_frame, text="")
        self.recording_label.pack(pady=5)
        
        # 状态标签
        self.status_label = ttk.Label(self.root, text="程序正在运行中...")
        self.status_label.pack(pady=10)
        
        # 使用说明
        instruction_frame = ttk.LabelFrame(self.root, text="使用说明", padding="10")
        instruction_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        instructions = """
1. 点击"开始录制"按钮
2. 按下你想要设置的热键组合
3. 再次点击按钮停止录制
4. 选择要转换的文本
5. 按下设置的热键进行转换
6. 程序会自动将选中的文本转换为大写
        """
        ttk.Label(instruction_frame, text=instructions, justify="left").pack()
    
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('hotkey', 'f2')
        except:
            pass
        return 'f2'
    
    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump({'hotkey': self.hotkey}, f)
        except:
            messagebox.showerror("错误", "保存配置失败")
    
    def start_hotkey_listener(self):
        def hotkey_listener():
            while self.is_running:
                try:
                    if keyboard.is_pressed(self.hotkey):
                        self.convert_to_upper()
                        time.sleep(0.3)  # 防止重复触发
                except Exception as e:
                    print(f"热键监听错误: {str(e)}")
                time.sleep(0.1)
        
        self.hotkey_thread = threading.Thread(target=hotkey_listener, daemon=True)
        self.hotkey_thread.start()
    
    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self):
        self.is_recording = True
        self.recorded_keys = []
        self.record_btn.config(text="停止录制")
        self.recording_label.config(text="请按下你想要设置的热键组合...")
        
        def on_key_event(event):
            if event.event_type == keyboard.KEY_DOWN:
                if event.name not in self.recorded_keys:
                    self.recorded_keys.append(event.name)
                    self.recording_label.config(text=f"已记录: {'+'.join(self.recorded_keys)}")
        
        keyboard.hook(on_key_event)
    
    def stop_recording(self):
        self.is_recording = False
        self.record_btn.config(text="开始录制")
        keyboard.unhook_all()
        
        if self.recorded_keys:
            new_hotkey = '+'.join(self.recorded_keys)
            self.hotkey = new_hotkey
            self.hotkey_label.config(text=f"当前热键: {new_hotkey}")
            self.save_config()
            self.recording_label.config(text="热键设置成功！")
            messagebox.showinfo("成功", f"热键已更新为: {new_hotkey}")
        else:
            self.recording_label.config(text="未检测到按键")
    
    def convert_to_upper(self):
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
            time.sleep(0.3)
            
            # 获取选中的文本
            win32clipboard.OpenClipboard()
            try:
                selected_text = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                print(f"获取到文本: {selected_text}")
            except:
                selected_text = ""
                print("未获取到文本")
            win32clipboard.CloseClipboard()
            
            if selected_text:
                # 将文本转换为大写
                upper_text = selected_text.upper()
                print(f"转换后文本: {upper_text}")
                
                # 将转换后的文本放回剪贴板
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(upper_text, win32con.CF_UNICODETEXT)
                win32clipboard.CloseClipboard()
                
                # 模拟 Ctrl+V 粘贴
                keyboard.send('ctrl+v')
                time.sleep(0.2)
                
                # 恢复原始剪贴板内容
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(original_clipboard, win32con.CF_UNICODETEXT)
                win32clipboard.CloseClipboard()
                
                self.status_label.config(text="转换完成！")
                print("转换完成！")
            else:
                self.status_label.config(text="未检测到选中的文本")
                print("未检测到选中的文本")
                
        except Exception as e:
            error_msg = f"发生错误: {str(e)}"
            self.status_label.config(text=error_msg)
            print(error_msg)
    
    def on_closing(self):
        self.is_running = False
        if self.hotkey_thread:
            self.hotkey_thread.join(timeout=1)
        self.root.destroy()

def main():
    root = tk.Tk()
    app = TextToUpperApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 