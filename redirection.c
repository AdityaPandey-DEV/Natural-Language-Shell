#include "headers/redirection.h"
#include "headers/utils.h"

// Global variables to store original file descriptors
static int original_stdin = -1;
static int original_stdout = -1;
static int original_stderr = -1;

// Set up input redirection
int setup_input_redirection(char *filename) {
    if (!filename) return 0;
    
    // Save original stdin
    if (original_stdin == -1) {
        original_stdin = dup(STDIN_FILENO);
    }
    
    int fd = open(filename, O_RDONLY);
    if (fd == -1) {
        print_error_with_errno("Cannot open input file");
        return -1;
    }
    
    if (dup2(fd, STDIN_FILENO) == -1) {
        print_error_with_errno("Cannot redirect stdin");
        close(fd);
        return -1;
    }
    
    close(fd);
    return 0;
}

// Set up output redirection
int setup_output_redirection(char *filename, int append) {
    if (!filename) return 0;
    
    // Save original stdout
    if (original_stdout == -1) {
        original_stdout = dup(STDOUT_FILENO);
    }
    
    int flags = O_WRONLY | O_CREAT;
    if (append) {
        flags |= O_APPEND;
    } else {
        flags |= O_TRUNC;
    }
    
    int fd = open(filename, flags, 0644);
    if (fd == -1) {
        print_error_with_errno("Cannot open output file");
        return -1;
    }
    
    if (dup2(fd, STDOUT_FILENO) == -1) {
        print_error_with_errno("Cannot redirect stdout");
        close(fd);
        return -1;
    }
    
    close(fd);
    return 0;
}

// Set up error redirection
int setup_error_redirection(char *filename) {
    if (!filename) return 0;
    
    // Save original stderr
    if (original_stderr == -1) {
        original_stderr = dup(STDERR_FILENO);
    }
    
    int fd = open(filename, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd == -1) {
        print_error_with_errno("Cannot open error file");
        return -1;
    }
    
    if (dup2(fd, STDERR_FILENO) == -1) {
        print_error_with_errno("Cannot redirect stderr");
        close(fd);
        return -1;
    }
    
    close(fd);
    return 0;
}

// Restore original stdin
void restore_stdin(void) {
    if (original_stdin != -1) {
        dup2(original_stdin, STDIN_FILENO);
        close(original_stdin);
        original_stdin = -1;
    }
}

// Restore original stdout
void restore_stdout(void) {
    if (original_stdout != -1) {
        dup2(original_stdout, STDOUT_FILENO);
        close(original_stdout);
        original_stdout = -1;
    }
}

// Restore original stderr
void restore_stderr(void) {
    if (original_stderr != -1) {
        dup2(original_stderr, STDERR_FILENO);
        close(original_stderr);
        original_stderr = -1;
    }
}
