# GLI variables and helper functions definition.

: ${GLI_D='dialog'};
: ${GLI_BTITLE='GLI - Gentoo Linux Installer'};
: ${GLI_DEBUG=0}
: ${GLI_LOG_FILE='/tmp/gli.log'}
: ${GLI_MOUNT='/mnt/gentoo'}

export GLI_D GLI_BTITLE GLI_DEBUG GLI_LOG_FILE GLI_MOUNT

# Helper function to print debug messages into log file.
function gli_debug
{
    local timestamp
    timestamp=$(date '+%d/%m/%y|%H:%M:%S')
    echo "[${timestamp}] $@" >> ${GLI_LOG_FILE}
}

# Format dialog --menu arguments.
function gli_fmt_d_menu
{
    local args out
    args=$1
    out=""

    while IFS="|" read -r one two; do
        out="${out} '$one' '$two'";
    done <<< ${args}

    echo ${out}
}
