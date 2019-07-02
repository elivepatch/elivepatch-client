import git
import os
import urllib.request as request
from elivepatch_client import log
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

    def git_download(self):
        git.Repo.clone_from(self.git_url, self.repo_dir)

    def git_update(self):
        cve_repository = git.cmd.Git(self.repo_dir)
        cve_repository.pull()

    def set_repo(self, git_url, repo_dir):
        self.git_url = git_url
        self.repo_dir = repo_dir

    def cve_git_id(self, kernel_version):
        major_version, minor_version, revision_version = kernel_version.split('.')
        print(major_version, minor_version, revision_version)
        security_file = open(self.repo_dir+str(major_version)+"."+str(minor_version)+
                             "/"+str(major_version)+"."+str(minor_version)+"_security.txt", "r")
        security_versions = []
        for line in security_file:
            if "CVEs fixed in" in line:
                security_versions_tmp = line.strip().split(' ')[3][:-1]
                # if there is not revision, set revision as 0
                sv_split_tmp = security_versions_tmp.split('.')
                if len(sv_split_tmp) == 2:
                    security_versions.append(0)
                else:
                    security_versions.append(security_versions_tmp.split('.')[2])
        security_file.close()

        log.notice('[debug] security versions: ' + str(security_versions))

        cve_2d_list = []
        for version in security_versions:
            if int(version) > int(revision_version):
                cve_2d_list.append(self.cve_id(major_version, minor_version, version))

        cve_outfile_list = []
        patch_index = 0
        if not os.path.exists(self.cve_patches_dir):
            os.mkdir(self.cve_patches_dir)
        for cve_list in cve_2d_list:
            # Remove duplicated cve_id from the cve list for not add the same patch
            cve_list = [ii for n,ii in enumerate(cve_list) if ii not in cve_list[:n]]
            for cve_id in cve_list:
                cve_outfile = self.download_cve_patch(cve_id, str(patch_index).zfill(5))
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
        security_file = open(self.repo_dir+str(major_version)+"."+str(minor_version)+
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
                        break
        security_file.close()
        return git_security_id

