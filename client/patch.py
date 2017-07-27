
import os


class ManaGer(object):

    def __init__(self):
        self.tmp_patch = os.path.join('/tmp', 'elivepatch')
        if not os.path.exists(self.tmp_patch):
            os.mkdir(self.tmp_patch)

    def list(self):
        patch_filename = []
        for (dirpath, dirnames, filenames) in os.walk(self.tmp_patch):
            patch_filename.extend(filenames)
            break
        print('List of current patches:')
        print(patch_filename)

    def save(self, patch):
        i = 0
        while os.path.exists("elivepatch_%s.patch" % i):
            i += 1
        fh = open("elivepatch_%s.patch" % i, "w")