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
    local timestamp=$(date '+%d/%m/%y|%H:%M:%S')
    echo "[${timestamp}] $@" >> ${GLI_LOG_FILE}
}

# Format dialog --menu arguments.
function gli_fmt_d_menu
{
    local ARGS OUT
    ARGS=$1
    OUT=""

    while IFS="|" read -r one two; do
        OUT="${OUT} '$one' '$two'";
    done <<< ${ARGS}

    echo ${OUT}
}
