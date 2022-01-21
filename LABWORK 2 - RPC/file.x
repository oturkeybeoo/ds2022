struct file {
	char filename[1024];
	char buffer[1024];
	int buffer_size;
};

program FILE_TRANSFER_PROG {
	version FILE_TRANSFER_VERS {
		int transfer_file(file) = 1;
	} = 1;
} = 0x20000001;
