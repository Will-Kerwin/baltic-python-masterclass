import os

from pygame import image, Surface


def get_image_path(image_name: str) -> str:
    return os.path.join("assets", "images", image_name)


def get_sound_path(sound_name: str) -> str:
    return os.path.join("assets", "sounds", sound_name)


def get_heart_frames(arr_len: int) -> [Surface]:
    arr: [Surface] = []
    for i in range(arr_len):
        arr.append(image.load(os.path.join("assets", "images", "hearts", f"frame-{i + 1}.png")).convert_alpha())
    return arr


def get_font_path(font_name: str) -> str:
    font = os.path.join("assets", "fonts", font_name)
    return font


def load_image(image_name: str, convert_alpha: bool = True) -> Surface:
    if convert_alpha:
        return image.load(get_image_path(image_name)).convert_alpha()
    else:
        return image.load(get_image_path(image_name))


def load_images(image_names: [str], convert_alpha: bool = True) -> [Surface]:
    # arr: [Surface] = [load_image(name, convert_alpha) for name in image_names]
    # for name in image_names:
    #     arr.append(load_image(name, convert_alpha))
    return [load_image(name, convert_alpha) for name in image_names]
