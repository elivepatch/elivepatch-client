
import os
import shutil
import tempfile
import subprocess

class ManaGer(object):

    def __init__(self):
        self.tmp_patch_folder = os.path.join('/tmp', 'elivepatch')
        if not os.path.exists(self.tmp_patch_folder):
            os.mkdir(self.tmp_patch_folder)

    def list(self):
        patch_filename = []
        for (dirpath, dirnames, filenames) in os.walk(self.tmp_patch_folder):
            patch_filename.extend(filenames)
            break
        print('List of current patches:')
        print(patch_filename)

    def load(self, patch_fulldir, livepatch_fulldir):
        try:
            command(['sudo','kpatch','load',livepatch_fulldir])
            print('patch_fulldir:' + str(patch_fulldir) + ' livepatch_fulldir: '+ str(livepatch_fulldir))
            self.save(patch_fulldir, livepatch_fulldir)
        except:
            print('failed to load the livepatch')

    def save(self, patch, livepatch):
        i = 0
        while os.path.exists(os.path.join(self.tmp_patch_folder, "elivepatch_%s" % i)):
            i += 1
        path_folder = os.path.join(self.tmp_patch_folder, "elivepatch_%s" % i)
        os.mkdir(path_folder)
        shutil.copy(patch, os.path.join(path_folder, "elivepatch.patch"))
        try:
            shutil.copy(livepatch, os.path.join(path_folder, "elivepatch.ko"))
        except:
            pass


def command(bashCommand, kernel_source_dir=None, env=None):
    """
    Popen override function

    :param bashCommand: List of command arguments to execute
    :param kernel_source_dir: the source directory of the kernel
    :return: void
    """
    # Inherit the parent environment and update the private copy
    if env:
        process_env = os.environ.copy()
        process_env.update(env)
        env = process_env

    if kernel_source_dir:
        print(bashCommand)
        process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE,  cwd=kernel_source_dir, env=env)
        output, error = process.communicate()
        print(output)
    else:
        print(bashCommand)
        process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, env=env)
        output, error = process.communicate()
        print(output)
