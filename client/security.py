from git import Repo
import os
import urllib.request as request
import shutil


class CVE(object):
    """
    Check the kernel against a CVE repository
    """
    def __init__(self):
        self.git_url = "https://github.com/nluedtke/linux_kernel_cves"
        self.repo_dir = "/tmp/kernel_cve/"
        self.cve_patches_dir = "/tmp/patches_cve/"
        pass

    def download(self):
        Repo.clone_from(self.git_url, self.repo_dir)

    def set_repo(self, git_url, repo_dir):
        self.git_url = git_url
        self.repo_dir = repo_dir

    def cve_git_id(self):
        major_version, minor_version, revision_version = _current_kernel_version()
        major_version, minor_version, revision_version = 4,9,25
        security_file = open("/tmp/kernel_cve/"+str(major_version)+"."+str(minor_version)+
                             "/"+str(major_version)+"."+str(minor_version)+"_security.txt", "r")
        security_versions = []
        for line in security_file:
            if "CVEs fixed in" in line:
                security_versions_tmp = line.strip().split(' ')[3][:-1]
                # if there is not revision, set revision as 0
                if len(security_versions_tmp) == 3:
                    security_versions.append(0)
                else:
                    security_versions.append(security_versions_tmp.split('.')[2])
        security_file.close()

        print('[debug] security versions: ' + str(security_versions))

        cve_2d_list = []
        for version in security_versions:
            if int(version) > revision_version:
                cve_2d_list.append(self.cve_id(major_version, minor_version, version))

        cve_outfile_list = []
        patch_index = 0
        if not os.path.exists(self.cve_patches_dir):
            os.mkdir(self.cve_patches_dir)
        for cve_list in cve_2d_list:
            # Remove duplicated cve_id from the cve list for not add the same patch
            cve_list = [ii for n,ii in enumerate(cve_list) if ii not in cve_list[:n]]
            for cve_id in cve_list:
                cve_outfile = self.download_cve_patch(cve_id, str(patch_index))
                cve_outfile_list.append([cve_outfile[0], cve_outfile[1].name])
                patch_index +=1
        return cve_outfile_list

    def download_cve_patch(self, cve_id, patch_index):
        file_name= self.cve_patches_dir + patch_index + '.patch'

        # Download the file from `url` and save it locally under `file_name`:
        with request.urlopen('https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git/patch/?id=' + cve_id[1]) as response, \
                open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        return [cve_id[0],out_file]

    def cve_id(self, major_version, minor_version, revision_version):
        security_file = open("/tmp/kernel_cve/"+str(major_version)+"."+str(minor_version)+
                             "/"+str(major_version)+"."+str(minor_version)+"_security.txt", "r")

        git_security_id = []
        # return cve for a kernel version
        for excluded_line in security_file:
            if ("CVEs fixed in "+str(major_version)+
                    "."+str(minor_version)+
                    "."+str(revision_version)+
                    ":") in excluded_line:
                for included_line in security_file:
                    if not "\n" is included_line:
                        git_security_id.append([included_line.strip().split(' ')[0].replace(':',''),included_line.strip().split(' ')[1]])
                    else:
                        # debug
                        # print('got cve for '+str(major_version)+
                        #       "."+str(minor_version)+
                        #       "."+str(revision_version))
                        break
        security_file.close()
        return git_security_id


def _current_kernel_version():
    kernel_version = os.uname()[2]
    major_version = int(kernel_version.split('.')[0])
    minor_version = int(kernel_version.split('.')[1])
    revision_version = int((kernel_version.split('.')[2]).split('-')[0])
    return major_version, minor_version, revision_version
