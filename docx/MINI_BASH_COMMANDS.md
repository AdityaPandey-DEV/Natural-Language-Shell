# 🐚 Mini-Bash Supported Commands

## ✅ Built-in Commands (Work Perfectly in Mini-Bash)

### Navigation Commands
| Command | Description | Example |
|---------|-------------|---------|
| `cd` | Change directory | `cd /home/user` |
| `pwd` | Print working directory | `pwd` |

### Display Commands
| Command | Description | Example |
|---------|-------------|---------|
| `echo` | Print text to screen | `echo "Hello World"` |
| `history` | Show command history | `history` |
| `history N` | Show last N commands | `history 10` |

### Process Management
| Command | Description | Example |
|---------|-------------|---------|
| `jobs` | List background jobs | `jobs` |
| `fg` | Bring job to foreground | `fg 1` |
| `bg` | Resume job in background | `bg 1` |

### System Commands
| Command | Description | Example |
|---------|-------------|---------|
| `exit` | Exit the shell | `exit` |
| `help` | Show built-in commands | `help` |

## ✅ External Commands (Available via System)

Mini-bash can execute ALL external commands through system terminal:

### File Operations
```bash
ls          # List files
ls -la      # List all files with details
cat file    # Display file contents
less file   # View file with paging
more file   # View file page by page
head file   # Show first 10 lines
tail file   # Show last 10 lines
wc file     # Word count
grep text   # Search for text
find .      # Find files
```

### System Info
```bash
uname -a    # System information
whoami      # Current user
hostname    # Computer name
date        # Current date/time
uptime      # System uptime
df -h       # Disk space
du -sh      # Directory size
ps aux      # Running processes
top         # Process monitor
```

### Network
```bash
ping host   # Test connectivity
curl url    # Download/test URLs
wget url    # Download files
ifconfig    # Network interfaces
```

## ⚠️ Commands Using System Terminal (Auto-Redirected)

These commands automatically use system terminal for better support:

### File System Operations
```bash
mkdir folder_name    # Create directory
rmdir folder_name    # Remove directory
touch file.txt       # Create empty file
rm file.txt          # Remove file
rm -r folder         # Remove folder
cp source dest       # Copy file
mv source dest       # Move/rename file
```

### Permissions
```bash
chmod 755 file       # Change permissions
chown user file      # Change owner
```

## 🔥 Advanced Features Supported

### 1. Pipelines
```bash
ls | grep .txt              # List only .txt files
cat file | sort | uniq      # Sort and get unique lines
ps aux | grep python        # Find Python processes
find . -name "*.py" | wc -l # Count Python files
```

### 2. Redirection
```bash
# Output redirection
echo "text" > file.txt      # Write to file (overwrite)
echo "text" >> file.txt     # Append to file
ls > files.txt              # Save listing to file

# Input redirection
sort < input.txt            # Sort from file

# Error redirection
ls nonexistent 2> error.log # Save errors to file
```

### 3. Background Jobs
```bash
sleep 10 &                  # Run in background
python script.py &          # Run script in background
jobs                        # List jobs
fg 1                        # Bring job 1 to foreground
bg 1                        # Resume job 1 in background
```

### 4. Command History
```bash
history                     # Show all history
history 20                  # Show last 20 commands
```

## 🚫 Known Limitations

### Not Directly Supported (Use System Terminal Instead)
- **Environment Variables**: `export VAR=value` (use system terminal)
- **Shell Scripts**: `.sh` files (use system terminal)
- **Advanced Redirection**: `&>` (use simple `>` instead)
- **Job Control**: Complex signals (basic Ctrl+C works)
- **Aliases**: Not supported
- **Tab Completion**: Not supported

## 💡 Smart AI Integration

The AI terminal automatically:
1. **Detects** which commands need system terminal
2. **Redirects** file operations (mkdir, rm, etc.) automatically
3. **Executes** everything else in mini-bash first
4. **Falls back** to system if mini-bash fails

### Example Flow:
```
User: "create folder test"
   ↓
AI: mkdir test
   ↓
System detects: mkdir needs system terminal
   ↓
Auto-redirect: Execute in system terminal
   ↓
✅ Folder created successfully
```

## 📊 Command Categories

### ✅ Perfect in Mini-Bash (Use Directly)
- `cd`, `pwd`, `echo`, `exit`
- `history`, `jobs`, `fg`, `bg`
- Pipelines: `|`
- Redirection: `>`, `>>`, `<`, `2>`
- Background jobs: `&`

### ⚡ Auto-System Terminal (No Worry)
- `mkdir`, `rmdir`, `touch`
- `rm`, `cp`, `mv`
- `chmod`, `chown`

### 🌐 Always System Terminal
- `ls`, `cat`, `grep`, `find`
- `ps`, `top`, `df`, `du`
- All other external commands

## 🎯 Best Practices

### 1. Use Natural Language
Instead of remembering syntax:
```
"show all python files"  → find . -name "*.py"
"list files with details" → ls -la
"create folder test"     → mkdir test
```

### 2. Let AI Handle It
The AI automatically:
- Chooses the right executor
- Handles file operations
- Manages redirections

### 3. Complex Operations
For complex operations, use natural language:
```
"find all files modified today"
"show disk usage of home directory"
"list running python processes"
```

## 🔧 Testing Commands

### Test Built-in Commands
```bash
pwd                         # ✅ Works in mini-bash
echo "Hello"               # ✅ Works in mini-bash
history                    # ✅ Works in mini-bash
```

### Test External Commands
```bash
ls -la                     # ✅ Works via system
mkdir test                 # ✅ Auto-redirected
cat file.txt               # ✅ Works via system
```

### Test Advanced Features
```bash
ls | grep .txt             # ✅ Pipeline works
echo "test" > file.txt     # ✅ Redirection works
sleep 10 &                 # ✅ Background works
```

## 📝 Summary

**Mini-Bash Ko Use Karo For:**
- Navigation (cd, pwd)
- Basic output (echo)
- History management
- Job control (jobs, fg, bg)
- Pipelines and redirection

**System Terminal Auto-Use For:**
- File operations (mkdir, rm, cp, mv)
- External commands (ls, cat, grep)
- System utilities (ps, top, df)

**AI Handles Everything:**
- Natural language commands
- Automatic executor selection
- Fallback management
- File searching

---

**💡 Pro Tip:** Just type in natural language - AI will handle the rest! 🚀

