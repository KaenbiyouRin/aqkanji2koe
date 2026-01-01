# AqKanji2Koe Python 封装库

用于 AquesTalk AqKanji2Koe 库（日语文本转音素转换器）的 Python 接口。

## 快速开始

```python
from aqkanji2koe import AqKanji2Koe

# 初始化转换器
converter = AqKanji2Koe(dict_dir="D:\\aqk2k_win\\aq_dic")

# 转换日文文本
phonemes = converter.convert("こんにちは")
print(phonemes)