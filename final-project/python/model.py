def transform(dist: float, width: float) -> tuple[float, float]:
    return (-dist / 3, (width - 30))

def update(_angle: tuple[float,float], _curAngle: tuple[float, float]) -> tuple[float, float]:
    sAngle = min(max(_curAngle[0] + _angle[0], 0), 30)
    mAngle = min(max(_curAngle[1] + sAngle + _angle[1], sAngle), sAngle + 15)

    return sAngle, mAngle

