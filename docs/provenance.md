# 来源与版本记录

## 整理原则

每种算法先固定来源，再描述当前实现。来源分为三类：

1. **公开基线**：提供公开仓库和固定提交；
2. **内部基线**：只记录可核对的提交，不提供无法访问的公开链接；
3. **未找到来源**：明确说明没有证据，不根据相似结构猜测。

## 当前三种方法

| 方法 | 来源性质 | 固定基线 | 当前实现的主要变化 |
| --- | --- | --- | --- |
| 编码器逐点补偿 | 内部固定旋转建图语义；未发现外部开源基线 | `R1_Multiple-encoders_SLAM@1.2.0`，首次接入 `efe065f...` | 任意倾斜轴、三维偏心、多源、可选IMU区间约束、严格时间覆盖、时间与角度预处理增强 |
| FAST-LIO2风格卡尔曼 | 公开FAST-LIO2/IKFoM/ikd-Tree，经内部中间分支迁移 | FAST_LIO `a4743b...`；ikd-Tree `e2e3f4...`；内部 `77e958...` | 无ROS计算核、独立传感器实例、初始化与质量门禁、统一体素输出 |
| 编码器约束站点全局优化 | 内部Python原型，无根许可证；按算法契约独立重写 | Python原型 `4c6acf...`；C++接入 `dbf4c15...` | 真实停站、站内微帧融合、双向ICP、完整测量环、共享轴拟合、soft-l1位姿图和严格终态 |

## 公开引用

### FAST-LIO2

- 论文：[FAST-LIO2: Fast Direct LiDAR-inertial Odometry](https://arxiv.org/abs/2107.06829)
- 代码：[hku-mars/FAST_LIO](https://github.com/hku-mars/FAST_LIO)
- 本次记录的固定提交：[`a4743b095409588842a5b30ddfa27e29d2f99164`](https://github.com/hku-mars/FAST_LIO/tree/a4743b095409588842a5b30ddfa27e29d2f99164)

### ikd-Tree

- 代码：[hku-mars/ikd-Tree](https://github.com/hku-mars/ikd-Tree)
- 本次记录的固定提交：[`e2e3f4e9d3b95a9e66b1ba83dc98d4a05ed8a3c4`](https://github.com/hku-mars/ikd-Tree/tree/e2e3f4e9d3b95a9e66b1ba83dc98d4a05ed8a3c4)

### IKFoM

- 论文：[Kalman Filters on Differentiable Manifolds](https://arxiv.org/abs/2102.03804)
- 代码：[hku-mars/IKFoM](https://github.com/hku-mars/IKFoM)

## 发布边界

- FAST-LIO派生源码使用GPL-2.0许可；公开派生代码前应单独核对完整许可义务。
- 内部Python站点全局优化原型没有根许可证，本网站只整理原理和版本关系，不发布或改写其源代码。
- 编码器逐点补偿尚未找到可靠外部来源，因此只标记为内部实现，不附会到CT-ICP、LOAM或FAST-LIO。

