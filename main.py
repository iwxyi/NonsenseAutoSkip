import time
import pyautogui
import cv2
import numpy as np
import pytesseract
import sounddevice as sd

# 废话列表
waste_phrases = [
    "大家好",
    "投币",
    "废话不多说",
    "请点赞",
    "关注我",
    "谢谢观看",
    "欢迎回来",
    "今天我们来",
    "如果你喜欢",
    "记得订阅",
    "感谢你的",
    "别忘了评论",
    "让我们开始吧",
    "接下来要",
    "这集我们将讨论",
    "希望你们喜欢",
    "再次感谢",
    "请不要跳过",
    "我会在下方留言",
    "这就是我的",
    "感谢大家的耐心",
    "如果你有任何",
    "请让我知道你",
    "视频开始前",
    "让我们先",
    "视频希望能",
    "希望这段视频",
    "请继续观看",
    "希望你们喜欢",
    "在评论区",
    "非常感谢你",
    "我很高兴能和",
    "让我们一起",
    "今天的主题是",
    "你们准备好了吗",
    "希望大家能够",
    "感谢你们的",
    "让我知道你们的",
    "给我一个赞",
    "会很有趣",
    "我们来看看",
    "感谢大家的支持",
    "希望你们能喜欢",
    "请务必看完",
    "马上开始",
    "在这里我想",
    "你觉得有用",
    "感谢大家",
    "接下来有个",
    "别忘了打开通知",
    "这次的内容",
    "准备了很久",
    "让我们一起深入",
    "今天的内容",
    "希望你们能",
    "请告诉我",
    "分享给",
    "小小的请求",
    "在评论区",
    "给我反馈",
    "开始今天的",
    "今天分享",
    "我会尽量",
    "参与讨论",
    "继续关注",
    "特别感谢",
    "要开始一个",
    "这次的内容",
    "别走开",
    "感谢你的",
    "请让我知道你",
    "下次再见",
    "度过愉快的一天",
    "继续支持我",
    "期待你们的",
    "别忘了点赞",
    "我们来聊聊",
    "我第一次",
    "感谢大家",
    "精彩继续",
    "我会在下方",
    "就是我今天想",
    "就是我想",
    "就是我这次想",
    "这是我为大家准备的",
    "请和我一起",
    "我会持续更新",
    "大家期待的",
    "今天的主题非常重要",
    "最后总结",
    "今天的分享",
    "我们下次再见",
    "欢迎收看"
]

# 定义截屏和识别的时间间隔（秒）
interval = 1

# 检查是否有媒体正在播放
def is_media_playing(duration=1, threshold=0.01):
    try:
        with sd.InputStream(callback=lambda *args: None):
            data = sd.rec(int(duration * 44100), samplerate=44100, channels=1, blocking=True)
        
        # 计算音频数据的均方根（RMS）值
        rms = np.sqrt(np.mean(data**2))
        
        # 如果 RMS 值超过阈值，认为有媒体在播放
        return rms > threshold
    except sd.PortAudioError:
        print("无法访问音频设备")
        return False

try:
    while True:
        # 检查是否有媒体正在播放
        if not is_media_playing():
            print("没有媒体播放，跳过当前循环")
            time.sleep(interval)
            continue

        # 截取屏幕的指定区域
        # *这里要根据自己的实际屏幕大小，获取到字幕通常出现的区域范围
        reg = (700, 800, 600, 100)  # (x, y, width, height)
        screenshot = pyautogui.screenshot(region=reg)
        
        # 将截图转换为 NumPy 数组
        screenshot_np = np.array(screenshot)

        # 保存截图到当前路径
        screenshot.save(f"screenshot.png")
        
        # 使用 Pytesseract 进行 OCR 识别
        try:
            recognized_text = pytesseract.image_to_string(screenshot, lang='chi_sim')  # 使用简体中文识别
            if recognized_text:
                print("识别成功:\"", recognized_text, "\"")
            else:
                print("未识别到文字")
        except Exception as e:
            print("识别失败 -", e)
            continue
        
        # 检查识别结果是否包含废话
        if any(phrase in recognized_text for phrase in waste_phrases):
            print("检测到废话:", recognized_text, "-", time.strftime("%H:%M:%S", time.localtime()))
            pyautogui.press('right')  # 模拟按右箭头键快进
        else:
            print("未检测到废话 -", time.strftime("%H:%M:%S", time.localtime()))
        
        time.sleep(interval)

except KeyboardInterrupt:
    print("程序已停止。")
