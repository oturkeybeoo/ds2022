/*
 * This is sample code generated by rpcgen.
 * These are only templates and you can use them
 * as a guideline for developing your own functions.
 */

#include "file.h"

int *transfer_file_1_svc(file *argp, struct svc_req *rqstp)
{
	static int  result;
	FILE* file;
    	file = fopen("recieve_file.txt", "a");
    	if (file == NULL) {
    		printf("Cannot open file");
    	} else {
    		printf("Start writing file\n");
    	}
    	
    	fwrite(argp->buffer, 1, argp->buffer_size, file);
    	fprintf(file, "%s", argp->buffer);
	printf("File received!");

	return &result;
}
