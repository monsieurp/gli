. "${GLI_SCRIPTSDIR}"/varfunc.bash
_0=$(basename "$0"); _0=${_0%%.bash};

GLI_TITLE='GLI - Disk partitioning'
ERROR=0
DISKS=()

while read -r line; do
    mapfile -t -d' ' <<< "${line}"
    [[ ! ${MAPFILE[1]} == 'disk' ]] && continue
    MAPFILE[3]=$(sed -e 's#\\x20# #g;' <<< "${MAPFILE[3]}")
    DISKS="/dev/${MAPFILE[0]}|${MAPFILE[3]} -> ${MAPFILE[2]}
${DISKS}"
done < <(lsblk -r -n -i -o KNAME,TYPE,SIZE,MODEL)

DISKS=$(awk 'NR > 1 { print prev } { prev=$0 } END { ORS=""; print }' <<< "${DISKS}")

GLI_D_DISKS=$(cat << EOF
${GLI_D} \
    --title "${GLI_TITLE}" \
    --backtitle "${GLI_BTITLE}" \
    --menu "Please select a disk:" 0 0 0 \
    $(gli_fmt_d_menu "${DISKS}")
EOF
)

exec 3>&1
MY_DISK=$( eval "${GLI_D_DISKS}" 2>&1 >&3 )
exec 3>&-

echo "${MY_DISK}"
