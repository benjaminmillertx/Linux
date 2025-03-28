#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/dcache.h>
#include <linux/namei.h>
#include <linux/dirent.h>

#define MAX_EXTENSIONS 16

static char *extensions[MAX_EXTENSIONS] = {
    ".locked", ".crypto", ".encrypted", ".ransom",
    ".rgss", ".lockedfile", ".encryptedfile",
    ".cerber", ".zzz", ".pay", ".file",
    ".map", ".redu", ".data", ".decrypt"
};

// Check if file has a ransomware-like extension
static bool is_ransomware_file(const char *filename) {
    for (int i = 0; i < MAX_EXTENSIONS; i++) {
        if (strstr(filename, extensions[i])) {
            return true;
        }
    }
    return false;
}

// Scan directory for ransomware files
static void scan_directory(const char *path) {
    struct file *dir;
    struct dir_context *ctx;
    struct linux_dirent64 *dirent;
    char buf[1024];

    dir = filp_open(path, O_RDONLY | O_DIRECTORY, 0);
    if (IS_ERR(dir)) {
        pr_err("Error opening directory: %s\n", path);
        return;
    }

    while (vfs_readdir(dir, ctx, buf, sizeof(buf)) > 0) {
        dirent = (struct linux_dirent64 *)buf;
        if (is_ransomware_file(dirent->d_name)) {
            pr_info("Potential ransomware detected: %s/%s\n", path, dirent->d_name);
        }
    }

    filp_close(dir, NULL);
}

static int __init ransomware_detector_init(void) {
    pr_info("Ransomware detector module loaded. Scanning /home...\n");
    scan_directory("/home");
    return 0;
}

static void __exit ransomware_detector_exit(void) {
    pr_info("Ransomware detector module unloaded.\n");
}

module_init(ransomware_detector_init);
module_exit(ransomware_detector_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Benjamin Miller");
MODULE_DESCRIPTION("Simple Ransomware File Detector Kernel Module");
