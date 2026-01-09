#ifndef HISTORY_H
#define HISTORY_H

#include "shell.h"

// Function prototypes
void init_history(void);
void add_to_history(char *command);
void save_history(void);
void load_history(void);
void print_history(int count);
char* get_history_command(int index);

#endif
