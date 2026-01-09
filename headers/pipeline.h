#ifndef PIPELINE_H
#define PIPELINE_H

#include "shell.h"

// Function prototypes
int execute_pipeline_commands(char **commands, int count);
int create_pipe(int pipefd[2]);
void close_pipe(int pipefd[2]);
int setup_pipeline_redirection(int pipe_in, int pipe_out, int is_first, int is_last);

#endif
