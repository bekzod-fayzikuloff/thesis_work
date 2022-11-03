from common.utils.hooks import include_object


def test_bar(store_data):
    store_include_object = include_object("common.utils.hooks:TEST_OBJECT")
    assert store_data == store_include_object
