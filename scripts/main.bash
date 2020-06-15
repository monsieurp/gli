"${GLI_D}" \
    --title 'Welcome to GLI!' \
    --backtitle "${GLI_BTITLE}" \
    --yesno 'Welcome to the Gentoo Linux Installer!

GLI simplifies the installation of Gentoo Linux as described
in the Gentoo Linux handbook.

See https://wiki.gentoo.org/wiki/Handbook for further information.

Would you like to begin the installation with GLI?' 0 0
RC=$?

if [[ ${RC} -eq 1 ]]; then
    exit ${RC}
fi

# SSHd setup is optional.
# Don't catch SIGINT here.
trap true SIGINT
if ! gli sshd; then
    # Restart the installation.
    exec $0
fi

# Networking is required.
# Restart if configuration fails.
if ! gli networking; then
    if ! gli error 'Network configuration failed!'; then
        exit $?
    else
        exec $0
    fi
fi
