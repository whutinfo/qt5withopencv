# -*- coding:utf-8 -*-

"""
交并比（Intersection over Union）和非极大值抑制是（Non-Maximum Suppression）是目标检测任务中非常重要的两个概念。
例如在用训练好的模型进行测试时，网络会预测出一系列的候选框。这时候我们会用NMS来移除一些多余的候选框。
即移除一些IOU值大于某个阈值的框。然后在剩下的候选框中，分别计算与ground truth的IOU值，
通常会规定当候选框和ground truth的IOU值大于0.5时，认为检测正确。

"""

def union(au, bu, area_intersection):
	area_a = (au[2] - au[0]) * (au[3] - au[1])
	area_b = (bu[2] - bu[0]) * (bu[3] - bu[1])
	area_union = area_a + area_b - area_intersection
	return area_union


def intersection(ai, bi):
	x = max(ai[0], bi[0])
	y = max(ai[1], bi[1])
	w = min(ai[2], bi[2]) - x
	h = min(ai[3], bi[3]) - y
	if w < 0 or h < 0:
		return 0
	return w*h


def iou(a, b):
	# a and b should be (x1,y1,x2,y2)

	if a[0] >= a[2] or a[1] >= a[3] or b[0] >= b[2] or b[1] >= b[3]:
		return 0.0

	area_i = intersection(a, b) #求交集
	area_u = union(a, b, area_i) #求并集

	return float(area_i) / float(area_u + 1e-6)



