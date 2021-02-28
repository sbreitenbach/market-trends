from post import Post


def test_is_thread_true():
    a = Post(1, "foo", 2, "thread")
    assert(a.is_thread())


def test_is_thread_false():
    a = Post(1, "foo", 2, "comment")
    b = a.is_thread()
    assert(b == False)
