
class Time:
  def __init__(self):
      pass

  def get_time(self, thisfr, fps):
    rest = int( thisfr%fps / fps * 100 )
    allse = int ( thisfr / fps )
    allmin = int ( allse / 60 )
    allh = int ( allmin / 60 )
    se = allse%60
    min = allmin%60

    if (int(len(str(min))) == 1):
        min = "0{}".format(min)
    if (int(len(str(se))) == 1):
        se = "0{}".format(se)
    if (rest < 10):
        rest = "0{}".format(rest)

    return [allh, min, se, rest]
