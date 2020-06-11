function error()
{
    local e
    if [[ -n "$1" ]]; then
            e="$1\n\n"
    fi
    "${GLI_D}" \
        --title 'GLI - Abort!' \
        --backtitle "${GLI_BTITLE}" \
        --yes-label 'Restart' \
        --no-label 'Abort' \
        --yesno "${e}An installation step has been aborted. Would you like to restart the installation or exit the installer?"
    RC=$?
    if [[ $? -eq 0 ]]; then
        gli main
    else
        exit 1
    fi
}
