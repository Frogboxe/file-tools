    File Tools
        A series of ps1 scripts that use Python to do useful things for files.

        sloc: Source Lines Of Code
            Counts the line counts of every file ending with `.py` in and below the CWD
            args:
                1: -s to sort; -r to sort and reverse
                2: -l to use a loose definition of a line (i.e. just count \\n newlines)

        bbf: Binary Build File
            Given a file name, it will reconstruct that file from its constituent parts
            of the form `<name>.<extension>.<number>` where number is 0 padded
            args:
                1: <filename>

        bsf: Binary Split File
            Given a file name, it will deconstruct that file into sub-100 MiB files
            of the same name with a number representing the order to reconstruct
            appended to it.
            args:
                1: <filename>

        wkh: Write Key Here
            Writes a new random encryption key in the CWD

        enc: Encrypt this file
        denc: Decrypt this file

        lf: List Files
            Lists files matching the filter (or all files if no filter given) with
            numerical IDs. Will open any file if filter is `=<number>` where number
            is an indexed file
            args:
                1: <filter>
                2: <index>
        
        ld: List Directories
            Lists directories like `lf` lists files
        
        l: List
            Lists directories and files like `lf` and `ld` combined

        goto: Goto
            Given a mapped name, will change the CWD to that location

        gotol: Goto and Lauch
            Given a mapped name, will call that location (opens files in
            their default application using `Start-Process`)

        gotos: Goto and Start
            Given a mapped name, will call that location (opens files in
            their default application using `start`)

        gotoe: Goto and open with explorer
            Given a mapped name, will open that location in windows
            explorer

        wsn: Wide Search Names
            Given a search term and optional index limit, will find any and
            all files and directories matching the search term via a bredth first 
            search of the CWD

        wsnf: Wide Search Named Files
            wsn for files

        wsnd: Wide Search Named Directories
            wsn for directories

        awp: Add Waypoint
        awd: Delete Waypoint