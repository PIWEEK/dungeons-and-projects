
from collections import namedtuple

Map = namedtuple('Map', 'image_path, thumbnail_path, placeholders')
Placeholder = namedtuple('Placeholder', 'image_path, x, y')


_maps = [
    Map(
        image_path = 'images/maps/world-1.jpg',
        thumbnail_path = 'images/maps/world-1-thumbnail.jpg',
        placeholders = [
            Placeholder('images/maps/city-1.png', 162, 188),
            Placeholder('images/maps/city-2.png', 852, 323),
            Placeholder('images/maps/city-3.png', 270, 640),
            Placeholder('images/maps/city-4.png', 595, 31),
            Placeholder('images/maps/city-1.png', 369, 407),
            Placeholder('images/maps/city-2.png', 564, 175),
            Placeholder('images/maps/city-3.png', 374, 540),
            Placeholder('images/maps/city-4.png', 396, 170),
            Placeholder('images/maps/city-1.png', 755, 478),
            Placeholder('images/maps/city-2.png', 404, 640),
        ],
    ),
    Map(
        image_path = 'images/maps/world-2.jpg',
        thumbnail_path = 'images/maps/world-2-thumbnail.jpg',
        placeholders = [
            Placeholder('images/maps/city-1.png', 178, 615),
            Placeholder('images/maps/city-2.png', 677, 413),
            Placeholder('images/maps/city-3.png', 165, 61),
            Placeholder('images/maps/city-4.png', 595, 31),
            Placeholder('images/maps/city-1.png', 369, 407),
            Placeholder('images/maps/city-2.png', 564, 175),
            Placeholder('images/maps/city-3.png', 374, 540),
            Placeholder('images/maps/city-4.png', 396, 170),
            Placeholder('images/maps/city-1.png', 755, 478),
            Placeholder('images/maps/city-2.png', 404, 640),
        ],
    ),    Map(
        image_path = 'images/maps/world-3.jpg',
        thumbnail_path = 'images/maps/world-3-thumbnail.jpg',
        placeholders = [
        ],
    ),    Map(
        image_path = 'images/maps/world-4.jpg',
        thumbnail_path = 'images/maps/world-4-thumbnail.jpg',
        placeholders = [
        ],
    ),
]


def get_map_for_project(project):
    # TODO: create a model for project visualization options, and let the user choose the map.
    return _maps[(project.id - 1) % len(_maps)]

