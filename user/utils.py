# utility functions here

avatar_path = '/avatar/'
def avatar_upload(instance, filename):
    '''uploading avatar to the corresponding user's folder'''
    return f"users/{instance.user.username}{avatar_path}{filename}/"
