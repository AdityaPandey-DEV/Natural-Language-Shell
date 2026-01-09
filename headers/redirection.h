#ifndef REDIRECTION_H
#define REDIRECTION_H

#include "shell.h"

// Function prototypes
int setup_input_redirection(char *filename);
int setup_output_redirection(char *filename, int append);
int setup_error_redirection(char *filename);
void restore_stdin(void);
void restore_stdout(void);
void restore_stderr(void);

#endif
