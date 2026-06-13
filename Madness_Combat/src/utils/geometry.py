def lerp(a, b, t):
    return a + (b - a) * t


def lerp_point(p1, p2, t):
    return (
        lerp(p1[0], p2[0], t),
        lerp(p1[1], p2[1], t)
    )


def point_on_quad(top_left, top_right, bottom_right, bottom_left, u, v):
    """
    u — положение слева направо внутри стены: 0.0 -> левый край, 1.0 -> правый край
    v — положение сверху вниз внутри стены: 0.0 -> верх, 1.0 -> низ
    """

    top = lerp_point(top_left, top_right, u)
    bottom = lerp_point(bottom_left, bottom_right, u)

    return lerp_point(top, bottom, v)


def make_wall_entry(wall_points, u1, u2, v_top, v_bottom):
    """
    Создаёт вход внутри стены.

    wall_points:
        (top_left, top_right, bottom_right, bottom_left)

    u1/u2:
        горизонтальная ширина входа внутри стены

    v_top/v_bottom:
        высота входа внутри стены
    """

    top_left, top_right, bottom_right, bottom_left = wall_points

    return (
        point_on_quad(top_left, top_right, bottom_right, bottom_left, u1, v_top),
        point_on_quad(top_left, top_right, bottom_right, bottom_left, u2, v_top),
        point_on_quad(top_left, top_right, bottom_right, bottom_left, u2, v_bottom),
        point_on_quad(top_left, top_right, bottom_right, bottom_left, u1, v_bottom),
    )