# utility functions here

file_path = '/files/'
def file_upload(instance, filename):
    '''uploading file to the corresponding user's folder'''
    return f"users/{instance.user.username}{file_path}{filename}/"
