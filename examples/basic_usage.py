from aqkanji2koe import AqKanji2Koe

# 配置路径 - 根据您的实际情况修改
DICT_DIR = r"D:\aqk2k_win\aq_dic"
DLL_PATH = r"D:\aqk2k_win\lib64\AqKanji2Koe.dll"

def main():
    try:
        # 使用上下文管理器（推荐）
        with AqKanji2Koe(DICT_DIR, DLL_PATH) as converter:
            print("✓ 转换器初始化成功")
            
            # 测试转换
            texts = ["こんにちは", "ありがとう", "ゆっくりしていってね"]
            
            for text in texts:
                phonemes = converter.convert(text)
                print(f"文本: {text}")
                print(f"音素: {phonemes}")
                print("-" * 30)
                
    except Exception as e:
        print(f"✗ 错误: {e}")

if __name__ == "__main__":
    main()