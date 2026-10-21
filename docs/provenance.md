# 参考与版本

<p class="lead">算法名称相似并不代表代码派生关系相同。版本记录用于区分公开论文、公开实现、内部数值原型和独立实现。</p>

## 建图方法来源

| 方法 | 来源 | 固定版本 | 技术范围 |
| --- | --- | --- | --- |
| 编码器逐点补偿 | 固定轴旋转建图实现；未发现直接对应的公开 SLAM 基线 | `R1_Multiple-encoders_SLAM@1.2.0`；接入提交 `efe065f9...` | 逐点时间、编码器插值、任意轴刚体变换、体素融合 |
| FAST-LIO2 | hku-mars/FAST_LIO、IKFoM、ikd-Tree | FAST_LIO `a4743b09...`；ikd-Tree `e2e3f4e9...` | IMU 传播、扫描去畸变、直接点到平面更新、增量地图 |
| 编码器约束站点优化 | Python 数值原型，随后按数学模型实现 C++ 求解器 | 原型 `4c6acf05...`；C++ 接入 `dbf4c15...` | 停站子图、双向 ICP、共享轴模型、鲁棒 SE(3) 位姿图 |

## FAST-LIO2

- 论文：[FAST-LIO2: Fast Direct LiDAR-inertial Odometry](https://arxiv.org/abs/2107.06829)
- 代码：[hku-mars/FAST_LIO](https://github.com/hku-mars/FAST_LIO)
- 固定代码版本：[`a4743b095409588842a5b30ddfa27e29d2f99164`](https://github.com/hku-mars/FAST_LIO/tree/a4743b095409588842a5b30ddfa27e29d2f99164)

FAST-LIO2 使用原始激光点构造点到局部地图平面的残差，以迭代误差状态卡尔曼滤波联合惯性传播和激光观测。

## ikd-Tree

- 代码：[hku-mars/ikd-Tree](https://github.com/hku-mars/ikd-Tree)
- 固定代码版本：[`e2e3f4e9d3b95a9e66b1ba83dc98d4a05ed8a3c4`](https://github.com/hku-mars/ikd-Tree/tree/e2e3f4e9d3b95a9e66b1ba83dc98d4a05ed8a3c4)

ikd-Tree 支持动态插入、删除、局部范围裁剪、近邻搜索和增量重平衡，用于维护 FAST-LIO2 的局部地图。

## IKFoM

- 论文：[Kalman Filters on Differentiable Manifolds](https://arxiv.org/abs/2102.03804)
- 代码：[hku-mars/IKFoM](https://github.com/hku-mars/IKFoM)

IKFoM 用流形上的加、减运算描述旋转等非欧氏状态，使误差状态滤波可以在局部切空间线性化。

## 许可说明

FAST_LIO 仓库采用 GPL-2.0 许可，ikd-Tree 与 IKFoM 中的文件保留各自许可声明。代码复用时需要按具体文件、固定版本和链接方式核对许可证义务。

内部数值原型没有可公开确认的根许可证，因此只记录算法结构和版本标识，不发布其源代码。
