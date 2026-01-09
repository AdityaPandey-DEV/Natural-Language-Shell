#ifndef SHELL_H
#define SHELL_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <signal.h>
#include <errno.h>
#include <time.h>
#include <limits.h>
#include <termios.h>

// Maximum command length
#define MAX_CMD_LEN 1024
#define MAX_ARGS 64
#define MAX_JOBS 32
#define MAX_HISTORY 1000

// Command structure
typedef struct {
    char **args;
    int argc;
    char *input_file;
    char *output_file;
    char *error_file;
    int append_output;
    int background;
} command_t;

// Job structure
typedef struct {
    pid_t pid;
    int job_id;
    char *command;
    int status; // 0: running, 1: stopped, 2: completed
    time_t start_time;
} job_t;

// Global variables
extern job_t jobs[MAX_JOBS];
extern int job_count;
extern int current_job_id;
extern char *history_file;

// Function prototypes
void init_shell(void);
void cleanup_shell(void);
void signal_handler(int sig);
void print_prompt(void);
int read_command(char *cmd);
void execute_command(char *cmd);
void cleanup_jobs(void);

#endif
