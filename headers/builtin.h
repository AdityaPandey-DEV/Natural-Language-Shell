#ifndef BUILTIN_H
#define BUILTIN_H

#include "shell.h"

// Function prototypes
int builtin_cd(command_t *cmd);
int builtin_pwd(command_t *cmd);
int builtin_echo(command_t *cmd);
int builtin_exit(command_t *cmd);
int builtin_history(command_t *cmd);
int builtin_jobs(command_t *cmd);
int builtin_fg(command_t *cmd);
int builtin_bg(command_t *cmd);

// File operation commands
int builtin_mkdir(command_t *cmd);
int builtin_rmdir(command_t *cmd);
int builtin_touch(command_t *cmd);
int builtin_rm(command_t *cmd);
int builtin_cp(command_t *cmd);
int builtin_mv(command_t *cmd);

#endif
