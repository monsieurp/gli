. "${GLI_SCRIPTSDIR}"/varfunc.bash
_0=$(basename "$0"); _0=${_0%%.bash};

GLI_TITLE='GLI - Disk partitioning'
ERROR=0
DISKS=()
PART_METHODS=$(cat << 'EOF'
Auto(ext4)|Guided disk partitioning using ext4
Auto(XFS)|Guided disk partitioning using XFS
Auto(JFS)|Guided disk partitioning using JFS
Manual|Manual disk partitioning with GLI
Shell|Open a shell
EOF
)

GLI_D_PART_METHODS=$(cat << EOF
${GLI_D} \
    --title "${GLI_TITLE}" \
    --backtitle "${GLI_BTITLE}" \
    --menu "How do you want to partition your disk?" 0 0 0 \
    $(gli_fmt_d_menu "${PART_METHODS}")
EOF
)

exec 3>&1
MY_PART_METHOD=$( eval "${GLI_D_PART_METHODS}" 2>&1 >&3 )
exec 3>&-

while read -r line; do
    mapfile -t -d' ' <<< "${line}"
    [[ ! ${MAPFILE[1]} == 'disk' ]] && continue
    MAPFILE[3]=$(sed -e 's#\\x20# #g;' <<< "${MAPFILE[3]}")
    DISKS="/dev/${MAPFILE[0]}|${MAPFILE[2]} ¬ ${MAPFILE[3]}
${DISKS}"
done < <(lsblk -r -n -i -o KNAME,TYPE,SIZE,MODEL | sort -r)

DISKS=$(awk 'NR > 1 { print prev } { prev=$0 } END { ORS=""; print }' <<< "${DISKS}")

GLI_D_DISKS=$(cat << EOF
${GLI_D} \
    --title "${GLI_TITLE}" \
    --backtitle "${GLI_BTITLE}" \
    --menu "Please select a disk" 0 0 0 \
    $(gli_fmt_d_menu "${DISKS}")
EOF
)

exec 3>&1
MY_DISK=$( eval "${GLI_D_DISKS}" 2>&1 >&3 )
exec 3>&-

echo "${MY_DISK} -> ${MY_PART_METHOD}"
