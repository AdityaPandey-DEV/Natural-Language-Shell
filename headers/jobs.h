#ifndef JOBS_H
#define JOBS_H

#include "shell.h"

// Function prototypes
int add_job(pid_t pid, char *command);
int remove_job(pid_t pid);
job_t* find_job(int job_id);
job_t* find_job_by_pid(pid_t pid);
void update_job_status(pid_t pid, int status);
void print_jobs(void);
int wait_for_job(int job_id);
int resume_job(int job_id, int foreground);
void cleanup_completed_jobs(void);

#endif
