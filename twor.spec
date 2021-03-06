# Define help
usage () { 
	printf "Wrapper for $TOOL_NAME $VERSION\\n\\nPlease specify:\n-i\tInput directory with ALL files to read (REQUIRED)\n-o\tOutput directory for the generated files to be stored (REQUIRED)\n-v\tDisplay version\n-h\tDisplay this help\n\nEXAMPLE\t\$$TOOL -i /Path/to/input -o /Path/for/output\"\n\n";
}

# Define update
update () {
	cd $REPO_PATH;
	if git diff origin/master $REPO_PATH/$TOOL/$TOOL | grep -q "git --diff"; then
		printf "Found newer version of $TOOL.\n\nUpdate $TOOL now?[y/n]: ";
		read ANSWER;
		echo $ANSWER;
		if [ $ANSWER == "y" ]; then
			printf "Retrieving changes from git repository\n\n";
			git pull;
			exec bash "$0" "$@";
		fi
	fi
}

# Read flags
while getopts 'i:o:vh' OPTION; do
    case $OPTION in
    i)
	IFLAG=true;
        INPUT="$OPTARG"
	;;
    o)
	OFLAG=true;
        OUTPUT="$OPTARG"
	;;
    v)
	echo $TOOL $VERSION;
	exit
	;;
    h)
	usage;
	exit
	;;
    :)
	echo "Missing option argument for -$OPTARG" >&2;
	exit 1
	;;
    *)
        echo "Incorrect options provided";
	usage;
        exit 1
        ;;
    esac
done

# Check for update
update;

# Check if required options are provided
if ! $IFLAG & ! $OFLAG; then
	echo "Please specify all required options";
	usage;
	exit 1;
fi

# Display info before starting container
printf "Starting $TOOL with $INPUT as input and $OUTPUT as output.\n\n------------\n\nHINT 1\tPlease use the directories /input (mapped to $INPUT) and /output (mapped to $OUTPUT) for your file paths.\n\nHINT 2\tTo Leave $TOOL, simply call \"exit\".\n\n------------\n\n";

# Display version
sudo docker run -it --rm $IMAGE:$VERSION bash -c "$CMD --version";

# Run tool in container
cd $USER_PATH;
sudo docker run -it --rm -v $INPUT:/input -v $OUTPUT:/output -w="/input" $IMAGE:$VERSION;
