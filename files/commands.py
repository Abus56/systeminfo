system_state_commands = (
            "ps -aux",
            ("ps -eo pcpu,pid,user,args", "sort -r -k1 ", "head"),
            ("ps -eo user,pcpu,pmem,pid,cmd", "sort -r -n -k3",  "head"),
            "free -m",
            "df -h",
            "iostat -m",
            )

ss_state_commands = ("ss -ltusxw", "ss state connected -tu")
