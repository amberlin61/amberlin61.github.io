# amberlin61.github.io

Amber Lin 的三维感知与建图算法笔记，内容分为建图、标定、点云处理和感知四个主题。

建图部分包含三种方法：

1. 编码器逐点补偿建图；
2. FAST-LIO2 风格卡尔曼建图；
3. 编码器约束站点子图全局优化。

每篇笔记说明数学模型、观测、优化方法、评价指标与退化条件；公开算法固定论文、仓库和代码版本。

## 本地预览

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdocs serve
```

浏览器打开 `http://127.0.0.1:8000/`。

## 构建

```bash
mkdocs build --strict
```

推送到 `main` 后，GitHub Actions 会自动构建并发布到 `https://amberlin61.github.io/`。

