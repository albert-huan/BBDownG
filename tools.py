import os
import json
import sys
import platform
import time

# 判断系统类型
system = 'Windows' if platform.system() == 'Windows' else 'Linux'

# 获取当前工作路径
def get_workdir():
    workdir = os.path.dirname(os.path.abspath(sys.argv[0]))
    return workdir


# 获取BBDown的路径
def get_bbdown():
    h = '.exe' if system == 'Windows' else ''
    bbdown = os.path.join(get_workdir(), "BBDown" + h)
    return bbdown


workdir = get_workdir()
bbdown_path = get_bbdown()
# 配置文件路径
config_path = os.path.join(get_workdir(), 'config.json')


# 保存配置文件
def save_config(obj):
    old_config = {}
    # 判断是否有配置文件
    if os.path.isfile(config_path):
        with open(config_path, 'r') as f:
            old_config = json.loads(f.read())

    config = {}
    for i in dir(obj):
        if i[:9] == "checkBox_":
            exec(f"config[i] = obj.{i}.isChecked()")
        elif i[:12] == "radioButton_":
            exec(f"config[i] = obj.{i}.isChecked()")
        elif i[:9] == "lineEdit_":
            exec(f"config[i] = obj.{i}.text()")
        elif i[:9] == "comboBox_":
            exec(f"config[i] = obj.{i}.currentIndex()")

    old_config.update(config)
    with open(config_path, 'w') as f:
        f.write(json.dumps(old_config, indent=4))


# 加载配置文件
def load_config(obj):
    # 判断是否有配置文件

    with open(config_path, 'r') as f:
        config = json.loads(f.read())
    # 按照配置文件设置
    for i in config:
        try:
            if type(config[i]) is type(True):
                exec(f'obj.{i}.setChecked({config[i]})')
            elif type(config[i]) is type(''):
                exec(f'obj.{i}.setText(r"{config[i]}")')
            elif type(config[i]) is type(0):
                exec(f'obj.{i}.setCurrentIndex({config[i]})')
        except:
            continue


# 读取配置文件
def read_config():
    """读取配置文件，如果缺少必要的键则使用默认值"""
    # 默认配置
    exe_suffix = '.exe' if system == 'Windows' else ''
    default_config = {
        'lineEdit_bbdown': os.path.join(workdir, f'BBDown{exe_suffix}'),
        'lineEdit_ffmpeg': os.path.join(workdir, 'ffmpeg', 'bin', f'ffmpeg{exe_suffix}'),
        'lineEdit_aria2c_path': os.path.join(workdir, 'aria2', f'aria2c{exe_suffix}'),
        'checkBox_ffmpeg': True,
        'checkBox_use_aria2c': False,
        'checkBox_aria2c_path': False,
        'checkBox_audio_only': False,
        'checkBox_video_only': False,
        'checkBox_sub_only': False,
        'checkBox_danmaku': False,
        'checkBox_ia': False,
        'checkBox_info': False,
        'checkBox_hs': False,
        'checkBox_debug': False,
        'checkBox_token': False,
        'checkBox_c': False,
        'checkBox_skip_subtitle': False,
        'checkBox_skip_cover': False,
        'checkBox_skip_mux': False,
        'checkBox_skip_ai': False,
        'checkBox_mp4box': False,
        'checkBox_mp4box_path': False,
        'checkBox_mt': False,
        'checkBox_force_http': False,
        'checkBox_language': False,
        'checkBox_p': False,
        'checkBox_p_delay': False,
        'checkBox_F': False,
        'checkBox_M': False,
        'checkBox_enable_proxy': False,
        'checkBox_host': False,
        'checkBox_ep_host': False,
        'checkBox_area': False,
        'checkBox_ua': False,
        'checkBox_archives': False,
    }
    
    try:
        with open(config_path, 'r') as f:
            config = json.loads(f.read())
            # 合并默认配置，确保所有必要的键都存在
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
            return config
    except (FileNotFoundError, json.JSONDecodeError):
        # 如果配置文件不存在或损坏，返回默认配置
        return default_config


def log():
    t = time.time()
    return f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))}.{int(t * 1000) % 1000}]'
