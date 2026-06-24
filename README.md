# 树木学 期末复习助手 v1.5.1

福建农林大学林学院树木学期末复习闪卡应用。

## 使用方式

浏览器直接打开 `index.html`，或用 Chrome 打开后选择"添加到主屏幕"。

## 功能

- 239道精选试题，覆盖全部36科
- 题型：名词解释(31)、填空题(69)、单选题(65)、判断题(40)、问答题(34)
- 选择题/判断题点击选项自动判对错
- 填空题输入框 + 关键词核对
- 问答题输入框 + 核心知识点打分
- 需复习错题库
- 侧边导航栏：题型筛选、36科独立入口、课本页码对照表、检索表练习
- PWA支持：Chrome添加到桌面，离线可用

## 文件说明

| 文件 | 说明 |
|------|------|
| `index.html` | 完整应用（单文件，含全部数据） |
| `manifest.json` | PWA 配置 |
| `sw.js` | Service Worker（离线缓存） |
| `icon-192.png` / `icon-512.png` | 应用图标 |

## 开发

修改题目后重建 HTML：

```bash
pip install pypdf python-docx   # 首次需安装依赖
python3 build.py                 # 读取 questions.json 生成 index.html
```

生成复习提纲 DOCX：

```bash
python3 make_dendro_docx.py      # 树木学
python3 make_bio_docx.py         # 生物统计学
```

| 文件 | 说明 |
|------|------|
| `build.py` | 构建脚本：读取 questions.json → 生成 index.html |
| `questions.json` | 239道题目数据（JSON） |
| `make_dendro_docx.py` | 生成树木学复习提纲 DOCX |
| `make_bio_docx.py` | 生成生物统计学复习提纲 DOCX |

## 来源

- 课本：祁承经、汤庚国《树木学（南方本）》
- 题库：来自4份期末复习思考题及参考答案
