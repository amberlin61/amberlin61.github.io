# amberlin61.github.io

Amber Lin 的算法学习笔记，当前先整理三种激光雷达建图方法：

1. 编码器逐点补偿建图；
2. FAST-LIO2 风格卡尔曼建图；
3. 编码器约束站点子图全局优化。

文档遵循“先写来源与固定基线，再写当前实现变化”的原则。未找到可靠来源时会明确标注，不根据相似算法猜测出处。

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

