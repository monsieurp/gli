trap true SIGINT

"${GLI_D}" \
    --title 'Welcome to GLI!' \
    --backtitle "${GLI_BTITLE}" \
    --yesno 'Welcome to the Gentoo Linux Installer!

GLI simplifies the installation of Gentoo Linux as described
in the Gentoo Linux handbook. See https://wiki.gentoo.org/wiki/Handbook
for further information.

Would you like to begin the installation?' 0 0
RC=$?

if [[ ${RC} -eq 1 ]]; then
    exit 1
fi

# SSHd setup is optional.
trap true SIGINT
gli sshd || exit 0

# Networking is required.
trap 'gli error' SIGINT
gli networking || gli error "Networking setup failed!"
