
import os
from sensor.logger import logging
class s3Sync:

    def sync_folder_to_s3(self,folder, aws_bucket_url):
        command = f"aws s3 sync {folder} {aws_bucket_url}"
        logging.info(f"running Command {command}")
        os.system(command=command)

    def sync_folder_from_s3(self, folder, aws_bucket_url):
        command = f"aws s3 sync  {aws_bucket_url} {folder}"
        logging.info(f"running Command {command}")
        os.system(command=command)