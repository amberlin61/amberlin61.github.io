#!/usr/bin/env python3
"""Generate the static SVG diagrams used by the algorithm notes."""

from __future__ import annotations

import html
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "diagrams"

INK = "#17324d"
MUTED = "#64778c"
BLUE = "#2f6feb"
CYAN = "#0891b2"
GREEN = "#198754"
AMBER = "#b45309"
PURPLE = "#7657c8"
RED = "#c24156"
SURFACE = "#ffffff"
SOFT = "#f5f8fc"
BORDER = "#cfdae7"


def text(x: float, y: float, value: str, *, size: int = 20, weight: int = 500,
         anchor: str = "middle", color: str = INK, css: str = "") -> str:
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'font-size="{size}" font-weight="{weight}" fill="{color}" class="{css}">'
        f'{html.escape(value)}</text>'
    )


def box(x: float, y: float, w: float, h: float, title: str, lines: list[str],
        *, color: str = BLUE, fill: str = SURFACE) -> str:
    items = [
        f'<g filter="url(#shadow)">',
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{BORDER}"/>',
        f'<rect x="{x}" y="{y}" width="7" height="{h}" rx="3.5" fill="{color}"/>',
        text(x + 22, y + 34, title, size=20, weight=700, anchor="start"),
    ]
    for i, line in enumerate(lines):
        items.append(text(x + 22, y + 63 + i * 25, line, size=15, anchor="start", color=MUTED))
    items.append("</g>")
    return "".join(items)


def pill(x: float, y: float, w: float, label: str, *, color: str = BLUE) -> str:
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="38" rx="19" fill="{color}" opacity="0.10"/>'
        + text(x + w / 2, y + 25, label, size=15, weight=650, color=color)
    )


def arrow(x1: float, y1: float, x2: float, y2: float, *, color: str = "#8ca1b7",
          dashed: bool = False, label: str | None = None) -> str:
    dash = ' stroke-dasharray="8 7"' if dashed else ""
    result = (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="2.5" marker-end="url(#arrow)"{dash}/>'
    )
    if label:
        result += text((x1 + x2) / 2, (y1 + y2) / 2 - 9, label, size=13, color=MUTED)
    return result


def save(name: str, title: str, subtitle: str, parts: list[str], *, width: int = 1200,
         height: int = 560) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    doc = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{html.escape(title)}</title>
  <desc id="desc">{html.escape(subtitle)}</desc>
  <defs>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
      <feDropShadow dx="0" dy="4" stdDeviation="7" flood-color="#17324d" flood-opacity="0.09"/>
    </filter>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L9,3 z" fill="#8ca1b7"/>
    </marker>
    <style>
      text {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans CJK SC', 'PingFang SC', 'Microsoft YaHei', sans-serif; }}
    </style>
  </defs>
  <rect width="100%" height="100%" fill="#fbfdff"/>
  {text(52, 54, title, size=26, weight=760, anchor="start")}
  {text(52, 82, subtitle, size=15, anchor="start", color=MUTED)}
  {''.join(parts)}
</svg>'''
    (OUT / name).write_text(doc, encoding="utf-8")


def algorithm_landscape() -> None:
    parts = [
        box(55, 130, 250, 150, "建图 Mapping", ["运动补偿", "状态估计与全局一致性"], color=BLUE, fill="#f7faff"),
        box(335, 130, 250, 150, "标定 Calibration", ["空间外参", "时间偏移与运动学参数"], color=CYAN, fill="#f6fcfd"),
        box(615, 130, 250, 150, "点云 Point Cloud", ["滤波、配准、分割", "几何拟合与质量评价"], color=GREEN, fill="#f7fcf9"),
        box(895, 130, 250, 150, "感知 Perception", ["目标检测与聚类", "中心定位和多帧跟踪"], color=PURPLE, fill="#faf8ff"),
        arrow(180, 310, 460, 310, dashed=True, label="坐标与时间"),
        arrow(460, 350, 740, 350, dashed=True, label="规范点云"),
        arrow(740, 390, 1020, 390, dashed=True, label="空间特征"),
        text(600, 455, "统一的坐标系、时间轴和不确定性描述连接四类算法", size=20, weight=650),
        pill(340, 485, 165, "模型与假设", color=BLUE),
        pill(520, 485, 165, "观测与残差", color=CYAN),
        pill(700, 485, 165, "优化与评价", color=GREEN),
    ]
    save("algorithm-landscape.svg", "三维算法知识结构", "从标定和点云处理到建图与感知的关系", parts, height=560)


def mapping_taxonomy() -> None:
    parts: list[str] = []
    rows = [
        (130, "编码器逐点补偿", ["LiDAR + 编码器"], ["固定轴运动模型"], ["逐点刚体变换"], ["体素地图"], BLUE),
        (280, "FAST-LIO2", ["LiDAR + IMU"], ["惯性传播"], ["迭代误差状态更新"], ["局部增量地图"], CYAN),
        (430, "站点全局优化", ["停站子图 + 编码器"], ["相对位姿测量"], ["共享轴 + 位姿图"], ["一圈全局地图"], PURPLE),
    ]
    for y, name, a, b, c, d, color in rows:
        parts.append(text(55, y + 58, name, size=18, weight=720, anchor="start", color=color))
        xs = [270, 505, 740, 975]
        labels = [a[0], b[0], c[0], d[0]]
        for idx, (x, label) in enumerate(zip(xs, labels)):
            parts.append(box(x, y, 180, 105, label, [], color=color, fill=SOFT))
            if idx < 3:
                parts.append(arrow(x + 180, y + 52, xs[idx + 1], y + 52))
    save("mapping-taxonomy.svg", "三类建图问题", "不同传感器先验对应不同的状态与优化范围", parts, height=580)


def encoder_pipeline() -> None:
    parts = [
        box(50, 140, 210, 118, "激光点", ["坐标 pᴸ", "逐点时刻 tₚ"], color=BLUE),
        box(50, 320, 210, 118, "编码器", ["时刻 tₖ", "角度 θₖ、角速度 ωₖ"], color=CYAN),
        box(325, 220, 205, 128, "统一时间轴", ["t = a·t_device + b", "检查覆盖与采样间隔"], color=AMBER, fill="#fffaf4"),
        box(595, 220, 205, 128, "角度插值", ["Hermite θ(tₚ)", "端点位置与速度连续"], color=GREEN, fill="#f7fcf9"),
        box(865, 140, 255, 118, "轴线刚体变换", ["任意轴 a、轴心 c", "外参 Tᴬ←ᴸ 与零角"], color=PURPLE, fill="#faf8ff"),
        box(865, 320, 255, 118, "确定性体素融合", ["floor(pᴹ / v)", "sum / count 输出均值"], color=BLUE, fill="#f7faff"),
        arrow(260, 199, 325, 265),
        arrow(260, 379, 325, 307),
        arrow(530, 284, 595, 284),
        arrow(800, 284, 865, 199),
        arrow(992, 258, 992, 320),
        pill(410, 410, 255, "单自由度运动已知", color=AMBER),
        pill(680, 410, 165, "无需 ICP", color=GREEN),
    ]
    save("encoder-pipeline.svg", "编码器逐点补偿", "利用时间对齐后的编码器轨迹恢复每个激光点的机械姿态", parts, height=540)


def fast_lio_pipeline() -> None:
    parts = [
        box(55, 140, 210, 120, "IMU 序列", ["角速度、加速度", "噪声与零偏模型"], color=CYAN),
        box(55, 330, 210, 120, "LiDAR 扫描", ["点坐标与相对时间", "LiDAR–IMU 外参"], color=BLUE),
        box(325, 140, 215, 120, "状态传播", ["R、p、v、bɢ、bₐ、g", "协方差传播"], color=AMBER, fill="#fffaf4"),
        box(325, 330, 215, 120, "扫描去畸变", ["查询点时刻姿态", "统一到参考时刻"], color=GREEN, fill="#f7fcf9"),
        box(605, 220, 220, 140, "直接几何观测", ["ikd-Tree 邻域搜索", "局部平面拟合", "点到平面残差"], color=PURPLE, fill="#faf8ff"),
        box(890, 140, 245, 120, "迭代误差状态更新", ["流形上线性化", "状态与协方差修正"], color=RED, fill="#fff7f8"),
        box(890, 330, 245, 120, "增量局部地图", ["插入、删除、裁剪", "树内降采样"], color=BLUE, fill="#f7faff"),
        arrow(265, 200, 325, 200),
        arrow(265, 390, 325, 390),
        arrow(432, 260, 432, 330),
        arrow(540, 390, 605, 320),
        arrow(825, 270, 890, 220),
        arrow(1012, 260, 1012, 330),
        arrow(890, 390, 825, 330, dashed=True, label="下一帧地图"),
    ]
    save("fast-lio-pipeline.svg", "FAST-LIO2 直接 LiDAR–IMU 估计", "惯性传播提供连续轨迹，点到地图平面残差修正状态", parts, height=560)


def station_graph() -> None:
    parts: list[str] = []
    cx, cy, radius = 260, 310, 145
    for i in range(12):
        angle = -math.pi / 2 + 2 * math.pi * i / 12
        x, y = cx + radius * math.cos(angle), cy + radius * math.sin(angle)
        j = (i + 1) % 12
        next_angle = -math.pi / 2 + 2 * math.pi * j / 12
        nx, ny = cx + radius * math.cos(next_angle), cy + radius * math.sin(next_angle)
        parts.append(f'<line x1="{x}" y1="{y}" x2="{nx}" y2="{ny}" stroke="#a9b8c8" stroke-width="2"/>')
        parts.append(f'<circle cx="{x}" cy="{y}" r="15" fill="#ffffff" stroke="{PURPLE}" stroke-width="4"/>')
        parts.append(text(x, y + 5, str(i), size=12, weight=700, color=PURPLE))
    parts.extend([
        f'<circle cx="{cx}" cy="{cy}" r="27" fill="{PURPLE}" opacity="0.13"/>',
        text(cx, cy + 5, "轴", size=18, weight=750, color=PURPLE),
        text(260, 500, "站点图：相邻边 + 首尾闭合边", size=16, weight=650),
        box(500, 140, 190, 110, "站内融合", ["微帧粗到细 ICP", "门禁异常微帧"], color=BLUE),
        box(755, 140, 190, 110, "站间测量", ["编码器初值", "双向点到面 ICP"], color=CYAN),
        box(1010, 140, 150, 110, "测量图", ["连通", "完整一圈"], color=GREEN),
        box(625, 345, 220, 125, "共享旋转轴模型", ["轴向 a、轴心 c", "比例 s、角度修正 δθ"], color=AMBER, fill="#fffaf4"),
        box(910, 345, 230, 125, "鲁棒 SE(3) 位姿图", ["固定首站 gauge", "soft-L1 抑制异常边"], color=RED, fill="#fff7f8"),
        arrow(690, 195, 755, 195),
        arrow(945, 195, 1010, 195),
        arrow(1085, 250, 1030, 345),
        arrow(845, 408, 910, 408),
        arrow(755, 250, 735, 345, dashed=True, label="相对位姿"),
    ])
    save("station-graph.svg", "编码器约束站点全局优化", "离散停站子图通过相对位姿边、共享轴模型与位姿图形成闭环", parts, height=570)


def calibration_graph() -> None:
    parts = [
        box(55, 150, 220, 120, "观测", ["点、平面、标靶", "IMU、编码器、时间戳"], color=BLUE),
        box(55, 340, 220, 120, "先验", ["刚体结构", "轴约束、单位与范围"], color=CYAN),
        box(345, 235, 225, 140, "参数模型", ["外参 T", "时钟 a、b", "轴线 a、c、零位 θ₀"], color=AMBER, fill="#fffaf4"),
        box(640, 235, 225, 140, "非线性优化", ["几何残差", "稳健核与参数约束", "可观测性检查"], color=PURPLE, fill="#faf8ff"),
        box(935, 150, 215, 120, "残差验证", ["均值、RMSE、P95", "空间与时间分层"], color=GREEN, fill="#f7fcf9"),
        box(935, 340, 215, 120, "独立复测", ["未参与拟合的数据", "重复安装与不同距离"], color=RED, fill="#fff7f8"),
        arrow(275, 210, 345, 275),
        arrow(275, 400, 345, 335),
        arrow(570, 305, 640, 305),
        arrow(865, 275, 935, 210),
        arrow(865, 335, 935, 400),
    ]
    save("calibration-graph.svg", "时空与运动学标定", "用同一组观测约束空间外参、时间映射和机械参数", parts, height=560)


def pointcloud_graph() -> None:
    labels = [
        (55, "原始点", ["x, y, z, intensity", "逐点时间"], BLUE),
        (285, "有效性过滤", ["距离、视场", "NaN 与离群点"], CYAN),
        (515, "采样与法向", ["体素代表点", "局部协方差"], GREEN),
        (745, "配准与分割", ["ICP / 图优化", "平面与连通域"], PURPLE),
        (975, "几何结果", ["表面、边界", "厚度与体积"], AMBER),
    ]
    parts: list[str] = []
    for idx, (x, title, lines, color) in enumerate(labels):
        parts.append(box(x, 210, 170, 135, title, lines, color=color))
        if idx < len(labels) - 1:
            parts.append(arrow(x + 170, 278, labels[idx + 1][0], 278))
    parts.extend([
        pill(300, 390, 180, "保持坐标与时间语义", color=BLUE),
        pill(500, 390, 180, "记录参数与损失", color=CYAN),
        pill(700, 390, 180, "量化覆盖与误差", color=GREEN),
    ])
    save("pointcloud-graph.svg", "点云处理链", "每一步改变点的数量、几何结构或统计含义", parts, height=520)


def perception_graph() -> None:
    parts = [
        box(55, 205, 180, 130, "点云输入", ["坐标、强度", "时间与传感器位姿"], color=BLUE),
        box(290, 205, 180, 130, "候选生成", ["ROI、地面分离", "强度与密度门限"], color=CYAN),
        box(525, 205, 180, 130, "对象聚类", ["欧式 / DBSCAN", "连通与尺寸约束"], color=GREEN),
        box(760, 205, 180, 130, "位置估计", ["质心、稳健中心", "包围盒与置信度"], color=PURPLE),
        box(995, 205, 150, 130, "多帧跟踪", ["数据关联", "状态滤波"], color=RED),
        arrow(235, 270, 290, 270),
        arrow(470, 270, 525, 270),
        arrow(705, 270, 760, 270),
        arrow(940, 270, 995, 270),
        arrow(1070, 335, 850, 415, dashed=True, label="预测约束下一帧搜索"),
        pill(380, 425, 180, "检测率与误检率", color=BLUE),
        pill(575, 425, 180, "中心位置误差", color=GREEN),
        pill(770, 425, 180, "时延与轨迹连续性", color=PURPLE),
    ]
    save("perception-graph.svg", "点云目标中心定位", "从候选点到稳定空间中心的处理链", parts, height=540)


def main() -> None:
    algorithm_landscape()
    mapping_taxonomy()
    encoder_pipeline()
    fast_lio_pipeline()
    station_graph()
    calibration_graph()
    pointcloud_graph()
    perception_graph()
    print(f"generated {len(list(OUT.glob('*.svg')))} diagrams in {OUT}")


if __name__ == "__main__":
    main()
