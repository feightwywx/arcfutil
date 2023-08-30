# Author: .direwolf <kururinmiracle@outlook.com>
# Licensed under the MIT License.

# 参照了Webkit的贝塞尔缓动实现
# https://trac.webkit.org/browser/trunk/Source/WebCore/platform/graphics/UnitBezier.h
def bezier(percent, p1x: float = 1/3, p1y: float = 0, p2x: float = 2/3, p2y: float = 1) -> float:
    cx = 3.0 * p1x;
    bx = 3.0 * (p2x - p1x) - cx;
    ax = 1.0 - cx -bx;
    cy = 3.0 * p1y;
    by = 3.0 * (p2y - p1y) - cy;
    ay = 1.0 - cy - by;

    def solve_curve_x(x: float) -> float:
        t2 = x
        for i in range(8):
            x2 = ((ax * t2 + bx) * t2 + cx) * t2 - x
            if abs(x2) < 1e-6:
                return t2
            d2 = (3.0 * ax * t2 + 2.0 * bx) * t2 + cx
            if abs(d2) < 1e-6:
                break
            t2 = t2 - x2 / d2
        
        t0 = 0.0
        t1 = 1.0
        t2 = x

        if t2 < t0:
            return t0
        if t2 > t1:
            return t1

        while t0 < t1:
            x2 = ((ax * t2 + bx) * t2 + cx) * t2
            if abs(x2 - x) < 1e-6:
                return t2
            if x > x2:
                t0 = t2
            else:
                t1 = t2
            t2 = (t1 - t0) * 0.5 + t0

        return t2
    
    t = solve_curve_x(percent)
        
    return ((ay * t + by) * t + cy) * t


def make_bezier(b_point: list = [1/3, 0, 2/3, 1]):
    def custom_bezier(x: float) -> float:
        return bezier(x, b_point[0], b_point[1], b_point[2], b_point[3])
    return custom_bezier
