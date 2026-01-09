#include "headers/builtin.h"
#include "headers/utils.h"
#include "headers/history.h"
#include "headers/jobs.h"

// Built-in cd command
int builtin_cd(command_t *cmd) {
    char *dir = NULL;
    
    if (cmd->argc > 1) {
        dir = cmd->args[1];
    } else {
        // Default to home directory
        dir = getenv("HOME");
        if (!dir) {
            print_error("cd: HOME not set");
            return 1;
        }
    }
    
    // Expand tilde if present
    char *expanded_dir = expand_tilde(dir);
    if (!expanded_dir) {
        print_error("cd: Memory allocation failed");
        return 1;
    }
    
    if (chdir(expanded_dir) == -1) {
        print_error_with_errno("cd");
        free(expanded_dir);
        return 1;
    }
    
    free(expanded_dir);
    return 0;
}

// Built-in pwd command
int builtin_pwd(command_t *cmd) {
    (void)cmd;  // Suppress unused parameter warning
    char cwd[1024];
    if (getcwd(cwd, sizeof(cwd)) != NULL) {
        printf("%s\n", cwd);
        return 0;
    } else {
        print_error_with_errno("pwd");
        return 1;
    }
}

// Built-in echo command
int builtin_echo(command_t *cmd) {
    for (int i = 1; i < cmd->argc; i++) {
        printf("%s", cmd->args[i]);
        if (i < cmd->argc - 1) {
            printf(" ");
        }
    }
    printf("\n");
    return 0;
}

// Built-in exit command
int builtin_exit(command_t *cmd) {
    int exit_code = 0;
    
    if (cmd->argc > 1) {
        exit_code = atoi(cmd->args[1]);
    }
    
    // Clean up before exit
    cleanup_shell();
    exit(exit_code);
}

// Built-in history command
int builtin_history(command_t *cmd) {
    int count = MAX_HISTORY;
    
    if (cmd->argc > 1) {
        count = atoi(cmd->args[1]);
        if (count <= 0) {
            print_error("history: Invalid count");
            return 1;
        }
    }
    
    print_history(count);
    return 0;
}

// Built-in jobs command
int builtin_jobs(command_t *cmd) {
    (void)cmd;  // Suppress unused parameter warning
    print_jobs();
    return 0;
}

// Built-in fg command (foreground)
int builtin_fg(command_t *cmd) {
    if (cmd->argc < 2) {
        print_error("fg: job number required");
        return 1;
    }
    
    int job_id = atoi(cmd->args[1]);
    if (job_id <= 0) {
        print_error("fg: Invalid job number");
        return 1;
    }
    
    return resume_job(job_id, 1); // 1 for foreground
}

// Built-in bg command (background)
int builtin_bg(command_t *cmd) {
    if (cmd->argc < 2) {
        print_error("bg: job number required");
        return 1;
    }
    
    int job_id = atoi(cmd->args[1]);
    if (job_id <= 0) {
        print_error("bg: Invalid job number");
        return 1;
    }
    
    return resume_job(job_id, 0); // 0 for background
}

// Built-in mkdir command
int builtin_mkdir(command_t *cmd) {
    if (cmd->argc < 2) {
        fprintf(stderr, "mkdir: missing operand\n");
        fprintf(stderr, "Usage: mkdir DIRECTORY...\n");
        return 1;
    }
    
    int status = 0;
    for (int i = 1; i < cmd->argc; i++) {
        if (mkdir(cmd->args[i], 0755) == -1) {
            fprintf(stderr, "mkdir: cannot create directory '%s': %s\n", 
                    cmd->args[i], strerror(errno));
            status = 1;
        }
    }
    return status;
}

// Built-in rmdir command
int builtin_rmdir(command_t *cmd) {
    if (cmd->argc < 2) {
        fprintf(stderr, "rmdir: missing operand\n");
        fprintf(stderr, "Usage: rmdir DIRECTORY...\n");
        return 1;
    }
    
    int status = 0;
    for (int i = 1; i < cmd->argc; i++) {
        if (rmdir(cmd->args[i]) == -1) {
            fprintf(stderr, "rmdir: failed to remove '%s': %s\n", 
                    cmd->args[i], strerror(errno));
            status = 1;
        }
    }
    return status;
}

// Built-in touch command
int builtin_touch(command_t *cmd) {
    if (cmd->argc < 2) {
        fprintf(stderr, "touch: missing file operand\n");
        fprintf(stderr, "Usage: touch FILE...\n");
        return 1;
    }
    
    int status = 0;
    for (int i = 1; i < cmd->argc; i++) {
        int fd = open(cmd->args[i], O_WRONLY | O_CREAT | O_NOCTTY | O_NONBLOCK, 0666);
        if (fd == -1) {
            fprintf(stderr, "touch: cannot touch '%s': %s\n", 
                    cmd->args[i], strerror(errno));
            status = 1;
        } else {
            close(fd);
        }
    }
    return status;
}

// Built-in rm command
int builtin_rm(command_t *cmd) {
    if (cmd->argc < 2) {
        fprintf(stderr, "rm: missing operand\n");
        fprintf(stderr, "Usage: rm FILE...\n");
        return 1;
    }
    
    int status = 0;
    for (int i = 1; i < cmd->argc; i++) {
        if (unlink(cmd->args[i]) == -1) {
            fprintf(stderr, "rm: cannot remove '%s': %s\n", 
                    cmd->args[i], strerror(errno));
            status = 1;
        }
    }
    return status;
}

// Built-in cp command (simplified version)
int builtin_cp(command_t *cmd) {
    if (cmd->argc < 3) {
        fprintf(stderr, "cp: missing file operand\n");
        fprintf(stderr, "Usage: cp SOURCE DEST\n");
        return 1;
    }
    
    const char *src = cmd->args[1];
    const char *dest = cmd->args[2];
    
    FILE *source = fopen(src, "rb");
    if (!source) {
        fprintf(stderr, "cp: cannot open '%s': %s\n", src, strerror(errno));
        return 1;
    }
    
    FILE *target = fopen(dest, "wb");
    if (!target) {
        fprintf(stderr, "cp: cannot create '%s': %s\n", dest, strerror(errno));
        fclose(source);
        return 1;
    }
    
    char buffer[8192];
    size_t bytes;
    while ((bytes = fread(buffer, 1, sizeof(buffer), source)) > 0) {
        if (fwrite(buffer, 1, bytes, target) != bytes) {
            fprintf(stderr, "cp: error writing to '%s'\n", dest);
            fclose(source);
            fclose(target);
            return 1;
        }
    }
    
    fclose(source);
    fclose(target);
    return 0;
}

// Built-in mv command
int builtin_mv(command_t *cmd) {
    if (cmd->argc < 3) {
        fprintf(stderr, "mv: missing file operand\n");
        fprintf(stderr, "Usage: mv SOURCE DEST\n");
        return 1;
    }
    
    const char *src = cmd->args[1];
    const char *dest = cmd->args[2];
    
    if (rename(src, dest) == -1) {
        fprintf(stderr, "mv: cannot move '%s' to '%s': %s\n", 
                src, dest, strerror(errno));
        return 1;
    }
    
    return 0;
}
