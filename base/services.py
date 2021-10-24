def get_path_upload_avatar(instance, file):
    """Построения пути к файлу(avatar), format: (media)/avatar/user_id/photo.jpg"""
    return f'avatar/{instance.id}/{file}'


def get_path_upload_image(instance, file):
    """Построения пути к файлу(avatar), format: (media)/image/user_id/photo.jpg"""
    return f'image/{instance.user.id}/{file}'
