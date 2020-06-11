# GLI variables definition.

: ${GLI_D="dialog"};
: ${GLI_BTITLE="GLI - Gentoo Linux Installer"};
: ${GLI_DEBUG=0}
: ${GLI_LOG_FILE="/tmp/gli.log"}

export GLI_D GLI_BTITLE GLI_DEBUG GLI_LOG_FILE

# Helper function to print debug messages into log file.
function gli_debug
{
    local timestamp=$(date '+%d/%m/%y|%H:%M:%S')
    echo "[${timestamp}] $@" >> ${GLI_LOG_FILE}
}
