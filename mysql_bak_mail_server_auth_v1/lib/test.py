from lib.record_log import savelog


def test1():
    s = savelog()

    i = 1
    if i > 2:
        s.info("test1:ok")
    else:
        s.info("test1:no")


def test2():
