"${GLI_D}" \
    --title 'Welcome to GLI!' \
    --backtitle "${GLI_BTITLE}" \
    --yesno 'Welcome to the Gentoo Linux Installer!

GLI simplifies the installation of Gentoo Linux as described
in the Gentoo Linux handbook.

See https://wiki.gentoo.org/wiki/Handbook for further information.

Would you like to begin the installation with GLI?' 0 0
RC=$?

case ${RC} in
    1)
        exit 1
    ;;
    *)
        :
    ;;
esac

# SSHd setup is optional.
# Don't catch SIGINT here.
trap true SIGINT

if ! gli sshd; then
    exec $0
fi

# Hostname is required;
# Restart if configuration fails.
if ! gli hostname; then
    gli error 'Set hostname failed!'
fi

# Networking is required.
# Restart if configuration fails.
if ! gli networking; then
    gli error 'Network configuration failed!'
fi
