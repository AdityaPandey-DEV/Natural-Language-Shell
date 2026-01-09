#include "headers/executor.h"
#include "headers/builtin.h"
#include "headers/pipeline.h"
#include "headers/jobs.h"
#include "headers/utils.h"

// Execute a single command
int execute_single_command(command_t *cmd) {
    if (!cmd || !cmd->args || cmd->argc == 0) {
        return 1;
    }
    
    // Check if it's a built-in command
    if (is_builtin(cmd->args[0])) {
        return execute_builtin(cmd);
    } else {
        return execute_external(cmd);
    }
}

// Execute pipeline commands
int execute_pipeline(char **commands, int count) {
    if (count <= 0) return 1;
    
    // If only one command, execute normally
    if (count == 1) {
        command_t *cmd = parse_command(commands[0]);
        if (cmd) {
            int result = execute_single_command(cmd);
            free_command(cmd);
            return result;
        }
        return 1;
    }
    
    // Execute pipeline
    return execute_pipeline_commands(commands, count);
}

// Execute built-in command
int execute_builtin(command_t *cmd) {
    if (!cmd || !cmd->args || cmd->argc == 0) {
        return 1;
    }
    
    char *command = cmd->args[0];
    
    if (strcmp(command, "cd") == 0) {
        return builtin_cd(cmd);
    } else if (strcmp(command, "pwd") == 0) {
        return builtin_pwd(cmd);
    } else if (strcmp(command, "echo") == 0) {
        return builtin_echo(cmd);
    } else if (strcmp(command, "exit") == 0) {
        return builtin_exit(cmd);
    } else if (strcmp(command, "history") == 0) {
        return builtin_history(cmd);
    } else if (strcmp(command, "jobs") == 0) {
        return builtin_jobs(cmd);
    } else if (strcmp(command, "fg") == 0) {
        return builtin_fg(cmd);
    } else if (strcmp(command, "bg") == 0) {
        return builtin_bg(cmd);
    }
    
    return 1;
}

// Execute external command
int execute_external(command_t *cmd) {
    if (!cmd || !cmd->args || cmd->argc == 0) {
        return 1;
    }
    
    pid_t pid = fork();
    
    if (pid == 0) {
        // Child process
        // Set up redirection
        setup_redirection(cmd);
        
        // Execute command
        if (execvp(cmd->args[0], cmd->args) == -1) {
            print_error_with_errno("Command not found");
            exit(1);
        }
    } else if (pid > 0) {
        // Parent process
        if (cmd->background) {
            // Background job
            add_job(pid, cmd->args[0]);
            printf("[%d] %d\n", current_job_id, pid);
        } else {
            // Foreground job
            int status;
            waitpid(pid, &status, 0);
            return WEXITSTATUS(status);
        }
    } else {
        // Fork failed
        print_error_with_errno("Fork failed");
        return 1;
    }
    
    return 0;
}

// Set up I/O redirection
void setup_redirection(command_t *cmd) {
    if (!cmd) return;
    
    // Input redirection
    if (cmd->input_file) {
        int fd = open(cmd->input_file, O_RDONLY);
        if (fd == -1) {
            print_error_with_errno("Cannot open input file");
            exit(1);
        }
        dup2(fd, STDIN_FILENO);
        close(fd);
    }
    
    // Output redirection
    if (cmd->output_file) {
        int flags = O_WRONLY | O_CREAT;
        if (cmd->append_output) {
            flags |= O_APPEND;
        } else {
            flags |= O_TRUNC;
        }
        
        int fd = open(cmd->output_file, flags, 0644);
        if (fd == -1) {
            print_error_with_errno("Cannot open output file");
            exit(1);
        }
        dup2(fd, STDOUT_FILENO);
        close(fd);
    }
    
    // Error redirection
    if (cmd->error_file) {
        int fd = open(cmd->error_file, O_WRONLY | O_CREAT | O_TRUNC, 0644);
        if (fd == -1) {
            print_error_with_errno("Cannot open error file");
            exit(1);
        }
        dup2(fd, STDERR_FILENO);
        close(fd);
    }
}
