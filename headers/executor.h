#ifndef EXECUTOR_H
#define EXECUTOR_H

#include "shell.h"
#include "parser.h"

// Function prototypes
int execute_single_command(command_t *cmd);
int execute_pipeline(char **commands, int count);
int execute_builtin(command_t *cmd);
int execute_external(command_t *cmd);
void setup_redirection(command_t *cmd);

#endif
