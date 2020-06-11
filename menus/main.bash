. ${GLI_MENUSDIR}/error.bash
trap error SIGINT

"${GLI_D}" \
    --title 'Welcome to GLI!' \
    --backtitle "${GLI_BTITLE}" \
    --yes-label 'Install' \
    --no-label 'Exit' \
    --yesno 'Welcome to the Gentoo Linux Installer!

GLI simplifies the installation of Gentoo Linux as described
in the Gentoo Linux handbook. See https://wiki.gentoo.org/wiki/Handbook
for further information.

Would you like to begin the installation?' 0 0
RC=$?

if [[ ${} -eq 1 ]]; then
    exit 0
fi

gli sshd
gli networking
