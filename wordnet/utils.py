def merge_synsets(list_of_lists):
    res = set()
    res.update(*list_of_lists)
    return res
