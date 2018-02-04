
from azure.storage.file import FileService,ContentSettings

file_service = FileService(account_name='picshare', account_key='etjPn6TajuKFOHofs9FrFFuFFc/hSPA76lj7q3VLkqds/EGibOFIZqepKcRnOVIqMnswBrpaVlpHD/TYGBVZfQ==')
#file_service.create_share('myshare')
#file_service.create_directory('myshare', 'Images')



generator = file_service.list_directories_and_files('Images')

for file_or_dir in generator:
    print(file_or_dir.name)

#file_service.create_file_from_path('myshare', 'Images', 'a.jpg', 'a.jpg', content_settings=ContentSettings(content_type='image/jpg'))