nodes = [
        {'_id': 1, 'name': 'Fred'},
        {'_id': 2, 'name': 'Bob'},
        {'_id': 3, 'name': 'Tom'},
        {'_id': 4, 'name': 'Dick'},
        {'_id': 5, 'name': 'Harry'},
        {'_id': 6, 'name': 'Lucy'},
    ]
edges = [
    {'_from': 1, '_to': 2, '_type': 'son'},
    {'_from': 2, '_to': 3, '_type': 'son'},
    {'_from': 2, '_to': 4, '_type': 'son'},
    {'_from': 2, '_to': 5, '_type': 'son'},
    {'_from': 2, '_to': 6, '_type': 'daughter'},
    {'_from': 3, '_to': 4, '_type': 'brother', '_backward': 'brother'},
    {'_from': 4, '_to': 5, '_type': 'brother', '_backward': 'brother'},
    {'_from': 5, '_to': 3, '_type': 'brother', '_backward': 'brother'},
    {'_from': 3, '_to': 6, '_type': 'sister', '_backward': 'brother'},
    {'_from': 4, '_to': 6, '_type': 'sister', '_backward': 'brother'},
    {'_from': 5, '_to': 6, '_type': 'sister', '_backward': 'brother'},
]
