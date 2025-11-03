import requests
import re
import sys

def download_playlist(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=30, headers=headers)
        response.encoding = 'utf-8'
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"下载播放列表失败: {e}")
        return None

def extract_groups(content):
    migu_content = []
    iqiyi_content = []
    
    # 更精确的正则表达式匹配分组
    migu_pattern = r'赛事咪咕,#genre#(.*?)(?=#genre#|\Z)'
    iqiyi_pattern = r'爱奇频道,#genre#(.*?)(?=#genre#|\Z)'
    
    # 提取咪咕内容
    migu_matches = re.findall(migu_pattern, content, re.DOTALL)
    if migu_matches:
        migu_block = migu_matches[0].strip()
        migu_lines = [line.strip() for line in migu_block.split('\n') if line.strip()]
        for line in migu_lines:
            if line and ',' in line and not line.startswith('#'):
                migu_content.append(line)
    
    # 提取爱奇艺内容
    iqiyi_matches = re.findall(iqiyi_pattern, content, re.DOTALL)
    if iqiyi_matches:
        iqiyi_block = iqiyi_matches[0].strip()
        iqiyi_lines = [line.strip() for line in iqiyi_block.split('\n') if line.strip()]
        for line in iqiyi_lines:
            if line and ',' in line and not line.startswith('#'):
                iqiyi_content.append(line)
    
    return migu_content, iqiyi_content

def save_txt_files(migu_content, iqiyi_content):
    try:
        with open('migu.txt', 'w', encoding='utf-8') as f:
            for line in migu_content:
                f.write(line + '\n')
        print(f"已保存 migu.txt，包含 {len(migu_content)} 个项目")
    except Exception as e:
        print(f"保存migu.txt失败: {e}")
    
    try:
        with open('iqiyi.txt', 'w', encoding='utf-8') as f:
            for line in iqiyi_content:
                f.write(line + '\n')
        print(f"已保存 iqiyi.txt，包含 {len(iqiyi_content)} 个项目")
    except Exception as e:
        print(f"保存iqiyi.txt失败: {e}")

def convert_to_m3u():
    # 转换咪咕文件
    try:
        with open('migu.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        valid_channels = 0
        with open('migu.m3u', 'w', encoding='utf-8') as f:
            f.write('#EXTM3U\n')
            for line in lines:
                line = line.strip()
                if line and ',' in line:
                    parts = line.split(',', 1)
                    if len(parts) == 2:
                        name, url = parts
                        if url.startswith(('http://', 'https://')):
                            f.write(f'#EXTINF:-1,{name}\n')
                            f.write(f'{url}\n')
                            valid_channels += 1
        
        print(f"已转换 migu.m3u，包含 {valid_channels} 个有效频道")
    except Exception as e:
        print(f"转换咪咕文件失败: {e}")
    
    # 转换爱奇艺文件
    try:
        with open('iqiyi.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        valid_channels = 0
        with open('iqiyi.m3u', 'w', encoding='utf-8') as f:
            f.write('#EXTM3U\n')
            for line in lines:
                line = line.strip()
                if line and ',' in line:
                    parts = line.split(',', 1)
                    if len(parts) == 2:
                        name, url = parts
                        if url.startswith(('http://', 'https://')):
                            f.write(f'#EXTINF:-1,{name}\n')
                            f.write(f'{url}\n')
                            valid_channels += 1
        
        print(f"已转换 iqiyi.m3u，包含 {valid_channels} 个有效频道")
    except Exception as e:
        print(f"转换爱奇艺文件失败: {e}")

def main():
    url = "http://rihou.cc:555/gggg.nzk/"
    
    print("开始下载播放列表...")
    content = download_playlist(url)
    
    if content:
        print("下载成功，开始处理内容...")
        
        migu_content, iqiyi_content = extract_groups(content)
        
        print(f"找到咪咕频道: {len(migu_content)} 个")
        if migu_content:
            print("前3个咪咕频道:")
            for i, channel in enumerate(migu_content[:3]):
                print(f"  {i+1}. {channel}")
        
        print(f"找到爱奇艺频道: {len(iqiyi_content)} 个")
        if iqiyi_content:
            print("前3个爱奇艺频道:")
            for i, channel in enumerate(iqiyi_content[:3]):
                print(f"  {i+1}. {channel}")
        
        if not migu_content and not iqiyi_content:
            print("警告: 没有找到任何频道内容，请检查源文件格式")
            print("原始内容前500字符:")
            print(content[:500])
        
        save_txt_files(migu_content, iqiyi_content)
        convert_to_m3u()
        
        print("处理完成！")
    else:
        print("处理失败！无法下载内容")
        sys.exit(1)

if __name__ == "__main__":
    main()
