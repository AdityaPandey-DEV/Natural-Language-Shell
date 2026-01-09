#include "headers/pipeline.h"
#include "headers/utils.h"
#include "headers/parser.h"
#include "headers/executor.h"

// Execute pipeline commands
int execute_pipeline_commands(char **commands, int count) {
    if (count <= 0) return 1;
    
    pid_t *pids = malloc(count * sizeof(pid_t));
    int **pipes = malloc((count - 1) * sizeof(int*));
    
    if (!pids || !pipes) {
        print_error("Memory allocation failed");
        if (pids) free(pids);
        if (pipes) free(pipes);
        return 1;
    }
    
    // Create pipes
    for (int i = 0; i < count - 1; i++) {
        pipes[i] = malloc(2 * sizeof(int));
        if (!pipes[i] || pipe(pipes[i]) == -1) {
            print_error_with_errno("Pipe creation failed");
            for (int j = 0; j <= i; j++) {
                if (pipes[j]) free(pipes[j]);
            }
            free(pipes);
            free(pids);
            return 1;
        }
    }
    
    // Fork processes for each command
    for (int i = 0; i < count; i++) {
        pids[i] = fork();
        
        if (pids[i] == 0) {
            // Child process
            // Set up input pipe (except for first command)
            if (i > 0) {
                dup2(pipes[i-1][0], STDIN_FILENO);
            }
            
            // Set up output pipe (except for last command)
            if (i < count - 1) {
                dup2(pipes[i][1], STDOUT_FILENO);
            }
            
            // Close all pipes in child
            for (int j = 0; j < count - 1; j++) {
                close(pipes[j][0]);
                close(pipes[j][1]);
            }
            
            // Parse and execute command
            command_t *cmd = parse_command(commands[i]);
            if (cmd) {
                if (is_builtin(cmd->args[0])) {
                    execute_builtin(cmd);
                } else {
                    execvp(cmd->args[0], cmd->args);
                    print_error_with_errno("Command not found");
                }
                free_command(cmd);
            }
            exit(1);
        } else if (pids[i] < 0) {
            print_error_with_errno("Fork failed");
            // Clean up pipes
            for (int j = 0; j < count - 1; j++) {
                close(pipes[j][0]);
                close(pipes[j][1]);
                free(pipes[j]);
            }
            free(pipes);
            free(pids);
            return 1;
        }
    }
    
    // Close all pipes in parent
    for (int i = 0; i < count - 1; i++) {
        close(pipes[i][0]);
        close(pipes[i][1]);
        free(pipes[i]);
    }
    free(pipes);
    
    // Wait for all processes
    int status;
    int exit_code = 0;
    for (int i = 0; i < count; i++) {
        waitpid(pids[i], &status, 0);
        if (i == count - 1) { // Last command's exit code
            exit_code = WEXITSTATUS(status);
        }
    }
    
    free(pids);
    return exit_code;
}

// Create a pipe
int create_pipe(int pipefd[2]) {
    return pipe(pipefd);
}

// Close pipe file descriptors
void close_pipe(int pipefd[2]) {
    close(pipefd[0]);
    close(pipefd[1]);
}

// Set up pipeline redirection
int setup_pipeline_redirection(int pipe_in, int pipe_out, int is_first, int is_last) {
    if (!is_first && pipe_in != -1) {
        if (dup2(pipe_in, STDIN_FILENO) == -1) {
            print_error_with_errno("Cannot redirect stdin");
            return -1;
        }
        close(pipe_in);
    }
    
    if (!is_last && pipe_out != -1) {
        if (dup2(pipe_out, STDOUT_FILENO) == -1) {
            print_error_with_errno("Cannot redirect stdout");
            return -1;
        }
        close(pipe_out);
    }
    
    return 0;
}
