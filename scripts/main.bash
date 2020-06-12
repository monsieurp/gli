trap 'gli error' SIGINT

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
gli sshd || exec $0

# Networking is required.
# Restart if configuration fails.
gli networking || gli error 'Networking setup failed!'
