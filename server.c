#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>

int main() {
    int ss, cli, pid;
    struct sockaddr_in ad;
    char s[100];
    socklen_t ad_length = sizeof(ad);

    // create the socket
    ss = socket(AF_INET, SOCK_STREAM, 0);

    // bind the socket to port 12345
    memset(&ad, 0, sizeof(ad));
    ad.sin_family = AF_INET;
    ad.sin_addr.s_addr = INADDR_ANY;
    ad.sin_port = htons(12345);
    bind(ss, (struct sockaddr*)&ad, ad_length);

    // then listen
    listen(ss, 0);

    while (1) {
        // an incoming connection
        cli = accept(ss, (struct sockaddr*)&ad, &ad_length);

        pid = fork();
        if (pid == 0) {
            // I'm the son, I'll serve this client
            printf("client connected\n");
            
            FILE* file;
            file = fopen("recieve_file.txt", "w");
            if (file == NULL) {
            	printf("Cannot open file");
            } else {
            	printf("Start writing file");
            }
            
            char buffer[1024];
            while (1) {
                int i = recv(cli, buffer, sizeof(buffer), 0);
                if (i <= 0) {
                	break;
                }
                fprintf(file, "%s", buffer);
                memset(&buffer, 0, sizeof(buffer));
            }
            
            return 0;
        } else {
            // I'm the father, continue the loop to accept more clients
            continue;
        }
    }
    // disconnect
    close(cli);
    close(ss);

}
